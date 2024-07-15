import asyncio
import json
import logging
import os
import time
import uuid
from functools import wraps
from typing import Any, Callable, Dict, Generator, Union
from fastapi import BackgroundTasks

from cohere.core.api_error import ApiError
from httpx import AsyncHTTPTransport
from httpx._client import AsyncClient
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request
from starlette.responses import Response

from backend.chat.collate import to_dict
from backend.chat.enums import StreamEvent
from backend.schemas.cohere_chat import CohereChatRequest
from backend.schemas.metrics import (
    MetricsAgent,
    MetricsData,
    MetricsMessageType,
    MetricsSignal,
    MetricsUser,
)
from backend.services.auth.utils import get_header_user_id
from backend.services.generators import AsyncGeneratorContextManager
from starlette.background import BackgroundTask

REPORT_ENDPOINT = os.getenv("REPORT_ENDPOINT", None)
REPORT_SECRET = os.getenv("REPORT_SECRET", None)
METRICS_LOGS_CURLS = os.getenv("METRICS_LOGS_CURLS", None)
NUM_RETRIES = 0
HEALTH_ENDPOINT = "health"
HEALTH_ENDPOINT_USER_ID = "health"

logger = logging.getLogger(__name__)


# TODO: update middleware to not have to do this mapping at all
# signals can simply specify event type
ROUTE_MAPPING: Dict[str, MetricsMessageType] = {
    "post /v1/users true": MetricsMessageType.USER_CREATED,
    "put /v1/users/:user_id true": MetricsMessageType.USER_UPDATED,
    "delete /v1/users/:user_id true": MetricsMessageType.USER_DELETED,
}


def event_name_of(
    method: str, endpoint_name: str, is_success: bool
) -> MetricsMessageType:
    key = f"{method} {endpoint_name} {is_success}"
    key = key.lower()
    if key in ROUTE_MAPPING:
        return ROUTE_MAPPING[key]
    return MetricsMessageType.UNKNOWN_SIGNAL


def preprocess_event_data(data: MetricsData | None) -> MetricsSignal | None:
    if not data:
        return None
    data_with_secret = attach_secret(data)
    try:
        signal = MetricsSignal(signal=data)
        return signal
    except Exception as e:
        logger.warning(f"Failed to preprocess event data: {e}")
        return None


class MetricsMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next: Callable):
        if not REPORT_SECRET:
            logger.warning("No report secret set")
        if not REPORT_ENDPOINT:
            logger.warning("No report endpoint set")

        request.state.trace_id = str(uuid.uuid4())
        request.state.agent = None
        request.state.user = None
        request.state.event_type = None

        start_time = time.perf_counter()
        response = await call_next(request)
        duration_ms = time.perf_counter() - start_time
        data = self.get_event_data(request.scope, response, request, duration_ms)
        signal = preprocess_event_data(data)
        should_send_event = request.state.event_type and data and signal
        if should_send_event:
            response.background = BackgroundTask(report_metrics, signal)
        return response

    def get_event_data(
        self, scope, response, request, duration_ms
    ) -> MetricsData | None:
        data = {}
        if scope["type"] != "http":
            return None
        message_type = request.state.event_type
        if not message_type:
            return None
        try:
            user_id = get_header_user_id(request)
        except:
            logger.warning(f"Failed to get user id - {endpoint_name}")
            return None

        agent = self.get_agent(request)
        agent_id = agent.id if agent else None
        user = self.get_user(request)
        object_ids = self.get_object_ids(request)
        event_id = str(uuid.uuid4())

        try:
            data = MetricsData(
                id=event_id,
                user_id=user_id,
                user=user,
                message_type=message_type,
                trace_id=request.state.trace_id,
                object_ids=object_ids,
                assistant=agent,
                assistant_id=agent_id,
                duration_ms=duration_ms,
            )
            return data
        except Exception as e:
            logger.warning(f"Failed to process event data: {e}")
            return None

    def get_method(self, scope: dict) -> str:
        try:
            return scope["method"].lower()
        except KeyError:
            return "unknown"
        except Exception as e:
            logger.warning(f"Failed to get method:  {e}")
            return "unknown"

    def get_endpoint_name(self, scope: dict, request: Request) -> str:
        try:
            path = scope["path"]
            # Replace path parameters with their names
            for key, value in request.path_params.items():
                path = path.replace(value, f":{key}")

            path = path[:-1] if path.endswith("/") else path
            return path.lower()
        except KeyError:
            return "unknown"
        except Exception as e:
            logger.warning(f"Failed to get endpoint name: {e}")
            return "unknown"

    def get_success(self, response: Response) -> bool:
        try:
            return 200 <= response.status_code < 300
        except Exception as e:
            logger.warning(f"Failed to get success: {e}")
            return False

    def get_user_id(self, request: Request) -> Union[str, None]:
        try:
            user_id = request.headers.get("User-Id", None)

            if not user_id:
                user_id = (
                    request.state.user.id
                    if hasattr(request.state, "user") and request.state.user
                    else None
                )

            # Health check does not have a user id - use a placeholder
            if not user_id and HEALTH_ENDPOINT in request.url.path:
                return HEALTH_ENDPOINT_USER_ID

            return user_id
        except Exception as e:
            logger.warning(f"Failed to get user id: {e}")
            return None

    def get_user(self, request: Request) -> Union[MetricsUser, None]:
        if not hasattr(request.state, "user") or not request.state.user:
            return None

        try:
            return MetricsUser(
                id=request.state.user.id,
                fullname=request.state.user.fullname,
                email=request.state.user.email,
            )
        except Exception as e:
            logger.warning(f"Failed to get user: {e}")
            return None

    def get_object_ids(self, request: Request) -> Dict[str, str]:
        object_ids = {}
        try:
            for key, value in request.path_params.items():
                object_ids[key] = value

            for key, value in request.query_params.items():
                object_ids[key] = value

            return object_ids
        except Exception as e:
            logger.warning(f"Failed to get object ids: {e}")
            return {}

    def get_agent(self, request: Request) -> Union[MetricsAgent, None]:
        if not hasattr(request.state, "agent") or not request.state.agent:
            return None
        return request.state.agent


async def report_metrics(signal: MetricsSignal) -> None:
    if not REPORT_SECRET:
        logger.error("No report secret set")
        return

    if not REPORT_ENDPOINT:
        logger.error("No report endpoint set")
        return
    if METRICS_LOGS_CURLS == "true":
        log_signal_curl(signal)
    if not isinstance(signal, dict):
        signal = to_dict(signal)
    transport = AsyncHTTPTransport(retries=NUM_RETRIES)
    try:
        async with AsyncClient(transport=transport) as client:
            await client.post(REPORT_ENDPOINT, json=signal)
    except Exception as e:
        logger.error(f"Failed to report metrics: {e}")


def attach_secret(data: MetricsData) -> MetricsData:
    if not REPORT_SECRET:
        return data
    data.secret = REPORT_SECRET
    return data


# TODO: remove the logging once metrics are configured correctly
def log_signal_curl(signal: MetricsSignal) -> None:
    s = to_dict(signal)
    s["signal"]["secret"] = "'$SECRET'"
    json_signal = json.dumps(s)
    # just general curl commands to test the endpoint for now
    logger.info(
        f"\n\ncurl -X POST -H \"Content-Type: application/json\" -d '{json_signal}' $ENDPOINT\n\n"
    )
