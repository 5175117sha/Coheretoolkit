from unittest.mock import MagicMock

import pytest
from fastapi.testclient import TestClient

from backend.config.deployments import ModelDeploymentName
from backend.database_models.user import User
from backend.schemas.cohere_chat import CohereChatRequest
from backend.tests.model_deployments.mock_deployments import MockAzureDeployment


def test_streamed_chat(
    session_client_chat: TestClient,
    user: User,
    mock_azure_deployment,
    mock_available_model_deployments,
):
    deployment = mock_azure_deployment.return_value
    deployment.invoke_chat_stream = MagicMock()
    response = session_client_chat.post(
        "/v1/chat-stream",
        headers={
            "User-Id": user.id,
            "Deployment-Name": ModelDeploymentName.Azure,
        },
        json={"message": "Hello", "max_tokens": 10},
    )

    assert response.status_code == 200
    assert type(deployment) is MockAzureDeployment
    deployment.invoke_chat_stream.assert_called_once_with(
        CohereChatRequest(
            message="Hello",
            chat_history=[],
            conversation_id="",
            documents=[],
            model="command-r",
            temperature=None,
            k=None,
            p=None,
            preamble=None,
            file_ids=None,
            tools=[],
            search_queries_only=False,
            deployment=None,
            max_tokens=10,
            seed=None,
            stop_sequences=None,
            presence_penalty=None,
            frequency_penalty=None,
            prompt_truncation="AUTO_PRESERVE_ORDER",
        )
    )


def test_non_streamed_chat(
    session_client_chat: TestClient,
    user: User,
    mock_azure_deployment,
    mock_available_model_deployments,
):
    deployment = mock_azure_deployment.return_value
    deployment.invoke_chat = MagicMock()
    response = session_client_chat.post(
        "/v1/chat",
        headers={
            "User-Id": user.id,
            "Deployment-Name": ModelDeploymentName.Azure,
        },
        json={"message": "Hello", "max_tokens": 10},
    )

    assert response.status_code == 200
    assert type(deployment) is MockAzureDeployment
    deployment.invoke_chat.assert_called_once_with(
        CohereChatRequest(
            message="Hello",
            chat_history=[],
            conversation_id="",
            documents=[],
            model="command-r",
            temperature=None,
            k=None,
            p=None,
            preamble=None,
            file_ids=None,
            tools=[],
            search_queries_only=False,
            deployment=None,
            max_tokens=10,
            seed=None,
            stop_sequences=None,
            presence_penalty=None,
            frequency_penalty=None,
            prompt_truncation="AUTO_PRESERVE_ORDER",
        )
    )
