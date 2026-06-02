import pytest
import requests
from unittest.mock import patch, MagicMock
from mobile.client import sendToArgusPrime


class TestSendToArgusPrime:
    def test_returns_dict_on_success(self):
        mock_response = MagicMock()
        mock_response.json.return_value = {"status": "dispatched", "capsule": "wealthbridge"}
        mock_response.raise_for_status.return_value = None
        with patch("requests.post", return_value=mock_response):
            result = sendToArgusPrime({"query": "credit check"})
        assert isinstance(result, dict)

    def test_returns_dispatched_status_on_success(self):
        mock_response = MagicMock()
        mock_response.json.return_value = {"status": "dispatched", "capsule": "wealthbridge"}
        mock_response.raise_for_status.return_value = None
        with patch("requests.post", return_value=mock_response):
            result = sendToArgusPrime({"query": "credit check"})
        assert result["status"] == "dispatched"

    def test_returns_error_dict_after_max_retries(self):
        with patch("requests.post", side_effect=requests.exceptions.ConnectionError("refused")):
            result = sendToArgusPrime({"query": "test"}, retries=0)
        assert result["status"] == "error"

    def test_retries_on_connection_error(self):
        mock_response = MagicMock()
        mock_response.json.return_value = {"status": "dispatched"}
        mock_response.raise_for_status.return_value = None
        side_effects = [requests.exceptions.ConnectionError("fail"), mock_response]
        with patch("requests.post", side_effect=side_effects):
            with patch("time.sleep"):
                result = sendToArgusPrime({"query": "test"}, retries=1)
        assert result["status"] == "dispatched"

    def test_http_error_returns_error_dict_immediately(self):
        mock_response = MagicMock()
        mock_response.raise_for_status.side_effect = requests.exceptions.HTTPError("404")
        with patch("requests.post", return_value=mock_response):
            result = sendToArgusPrime({"query": "test"}, retries=2)
        assert result["status"] == "error"
        assert "error" in result

    def test_max_retries_exceeded_message(self):
        with patch("requests.post", side_effect=requests.exceptions.ConnectionError):
            with patch("time.sleep"):
                result = sendToArgusPrime({"query": "fail"}, retries=1)
        assert "Max retries exceeded" in result["error"]
