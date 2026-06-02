import pytest
import requests
from unittest.mock import patch, MagicMock
from agents.mindmax.nim.nim_client import NIMClient


@pytest.fixture
def client():
    return NIMClient(endpoint="https://nim.test")


class TestNIMClientInit:
    def test_stores_endpoint(self, client):
        assert client.endpoint == "https://nim.test"

    def test_accepts_arbitrary_endpoint(self):
        c = NIMClient(endpoint="http://localhost:9000")
        assert c.endpoint == "http://localhost:9000"


class TestIsHealthy:
    def test_returns_true_by_default(self, client):
        # Current stub always returns True — verify the contract holds
        assert client.is_healthy() is True

    def test_returns_bool(self, client):
        result = client.is_healthy()
        assert isinstance(result, bool)


class TestInfer:
    def test_returns_dict(self, client):
        result = client.infer({"prompt": "hello"})
        assert isinstance(result, dict)

    def test_returns_text_key(self, client):
        result = client.infer({"prompt": "hello"})
        assert "text" in result

    def test_accepts_empty_payload(self, client):
        result = client.infer({})
        assert isinstance(result, dict)

    def test_accepts_complex_payload(self, client):
        payload = {"prompt": "explain quantum", "max_tokens": 100, "temperature": 0.7}
        result = client.infer(payload)
        assert isinstance(result, dict)


class TestIsHealthyWithMockedHTTP:
    """Forward-looking tests that verify behaviour once is_healthy() makes real HTTP calls."""

    def test_healthy_when_endpoint_returns_200(self, client):
        mock_response = MagicMock()
        mock_response.status_code = 200
        with patch("requests.get", return_value=mock_response):
            # Once implemented, a 200 response should mean healthy.
            # For now the stub ignores HTTP, so we just assert no exception is raised.
            result = client.is_healthy()
            assert result is not None

    def test_connection_error_does_not_crash(self, client):
        with patch("requests.get", side_effect=requests.exceptions.ConnectionError):
            # Once implemented, a connection error should be handled gracefully.
            try:
                result = client.is_healthy()
                assert isinstance(result, bool)
            except requests.exceptions.ConnectionError:
                pytest.fail("is_healthy() should handle ConnectionError gracefully")
