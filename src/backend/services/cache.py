import os
from typing import Any

from redis import Redis

from backend.services.logger import get_logger

logger = get_logger()


def get_client() -> Redis:
    redis_url = os.getenv("REDIS_URL")

    if not redis_url:
        error = "Tried retrieving Redis client but REDIS_URL environment variable is not set."
        logger.error(error)
        raise ValueError(error)

    client = Redis.from_url(redis_url, decode_responses=True)

    return client


def cache_put(key: str, value: Any) -> None:
    client = get_client()

    client.set(key, value)


def cache_get(key: str) -> Any:
    client = get_client()

    return client.get(key)


def cache_del(key: str) -> None:
    client = get_client()

    client.delete(key)
