import pytest
from backend.main import app
from fastapi.testclient import TestClient


@pytest.fixture
def error_client():
    """
    Fixture used to test global error handler
    """

    @app.get("/error")
    def test_error():
        raise Exception("Test exception")

    yield TestClient(app, raise_server_exceptions=False)
