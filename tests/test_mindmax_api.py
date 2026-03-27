import pytest
from unittest.mock import patch
from fastapi.testclient import TestClient
from agents.mindmax.api import MindMaxAPI


@pytest.fixture
def app():
    return MindMaxAPI()


@pytest.fixture
def client(app):
    return TestClient(app)


@pytest.fixture
def unhealthy_app():
    instance = MindMaxAPI()
    instance.nim_client.is_healthy = lambda: False
    return instance


@pytest.fixture
def unhealthy_client(unhealthy_app):
    return TestClient(unhealthy_app)


class TestHealthEndpoint:
    def test_returns_200(self, client):
        resp = client.get("/health")
        assert resp.status_code == 200

    def test_returns_status_ok(self, client):
        resp = client.get("/health")
        assert resp.json()["status"] == "ok"

    def test_returns_service_name(self, client):
        resp = client.get("/health")
        assert resp.json()["service"] == "MindMax Core"

    def test_health_is_always_available_regardless_of_nim(self, unhealthy_client):
        resp = unhealthy_client.get("/health")
        assert resp.status_code == 200


class TestGenerateEndpoint:
    def test_returns_200_when_nim_healthy(self, client):
        resp = client.post("/generate", params={"prompt": "hello world"})
        assert resp.status_code == 200

    def test_response_contains_nim_processed_when_healthy(self, client):
        resp = client.post("/generate", params={"prompt": "hello world"})
        assert "NIM processed" in resp.json()["response"]

    def test_prompt_is_truncated_to_20_chars_in_response(self, client):
        long_prompt = "a" * 50
        resp = client.post("/generate", params={"prompt": long_prompt})
        assert long_prompt[:20] in resp.json()["response"]

    def test_returns_unhealthy_message_when_nim_down(self, unhealthy_client):
        resp = unhealthy_client.post("/generate", params={"prompt": "test"})
        assert resp.json()["response"] == "Service unhealthy."

    def test_missing_prompt_returns_422(self, client):
        resp = client.post("/generate")
        assert resp.status_code == 422

    def test_empty_prompt_is_accepted(self, client):
        resp = client.post("/generate", params={"prompt": ""})
        assert resp.status_code == 200


class TestMindMaxAPIMetadata:
    def test_api_title(self, app):
        assert app.title == "MindMax Core API"

    def test_api_version(self, app):
        assert app.version == "1.0.0"
