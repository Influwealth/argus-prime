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
        assert resp.json()["service"] == "Argus Prime"

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


class TestAgentEndpoint:
    def test_returns_200(self, client):
        resp = client.post("/agent", json={"query": "run credit analysis"})
        assert resp.status_code == 200

    def test_routes_credit_to_wealthbridge(self, client):
        resp = client.post("/agent", json={"query": "run credit analysis"})
        assert resp.json()["capsule"] == "wealthbridge"

    def test_routes_unknown_to_deepagent(self, client):
        resp = client.post("/agent", json={"query": "something completely unknown"})
        assert resp.json()["capsule"] == "deepagent"

    def test_routes_predict_to_prediction_engine(self, client):
        resp = client.post("/agent", json={"query": "predict my outcome"})
        assert resp.json()["capsule"] == "prediction_engine"

    def test_status_is_dispatched(self, client):
        resp = client.post("/agent", json={"query": "simulate portfolio"})
        assert resp.json()["status"] == "dispatched"

    def test_session_id_is_present(self, client):
        resp = client.post("/agent", json={"query": "quantum optimize"})
        assert "session_id" in resp.json()

    def test_missing_query_returns_422(self, client):
        resp = client.post("/agent", json={})
        assert resp.status_code == 422

    def test_context_field_is_optional(self, client):
        resp = client.post("/agent", json={"query": "invoice needed"})
        assert resp.status_code == 200


class TestDeepFlexEndpoints:
    def test_dispatch_returns_200(self, client):
        resp = client.post("/deepflex/dispatch", json={
            "command_id": "cmd-test-1",
            "capsule": "deepagent",
            "payload": {"query": "test"},
        })
        assert resp.status_code == 200

    def test_dispatch_returns_command_id(self, client):
        resp = client.post("/deepflex/dispatch", json={
            "command_id": "cmd-test-2",
            "capsule": "wealthbridge",
            "payload": {"query": "credit analysis"},
        })
        assert resp.json()["command_id"] == "cmd-test-2"

    def test_dispatch_status_is_accepted(self, client):
        resp = client.post("/deepflex/dispatch", json={
            "command_id": "cmd-test-3",
            "capsule": "deepagent",
            "payload": {},
        })
        assert resp.json()["status"] == "accepted"

    def test_dispatch_capsule_is_echoed(self, client):
        resp = client.post("/deepflex/dispatch", json={
            "command_id": "cmd-test-4",
            "capsule": "prediction_engine",
            "payload": {},
        })
        assert resp.json()["capsule"] == "prediction_engine"

    def test_dispatch_missing_command_id_returns_422(self, client):
        resp = client.post("/deepflex/dispatch", json={"capsule": "deepagent"})
        assert resp.status_code == 422

    def test_dispatch_missing_capsule_returns_422(self, client):
        resp = client.post("/deepflex/dispatch", json={"command_id": "x"})
        assert resp.status_code == 422

    def test_status_returns_200(self, client):
        resp = client.get("/deepflex/status")
        assert resp.status_code == 200

    def test_status_role_is_executor(self, client):
        resp = client.get("/deepflex/status")
        assert resp.json()["role"] == "offline-it-executor"

    def test_status_supervisor_is_deepflex(self, client):
        resp = client.get("/deepflex/status")
        assert resp.json()["supervisor"] == "deepflex"


class TestArgusNodeMetadata:
    def test_api_title_reflects_argus_role(self, app):
        assert app.title == "Argus Prime — Execution Node API"

    def test_api_version(self, app):
        assert app.version == "1.0.0"
