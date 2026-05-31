import time
import pytest
from session import runAgentSession


class TestRunAgentSession:
    def test_returns_dict(self):
        result = runAgentSession("wealthbridge", {"query": "credit check"})
        assert isinstance(result, dict)

    def test_contains_session_id(self):
        result = runAgentSession("wealthbridge", {"query": "credit check"})
        assert "session_id" in result
        assert len(result["session_id"]) > 0

    def test_session_id_is_unique(self):
        r1 = runAgentSession("mindmax", {"query": "simulate"})
        r2 = runAgentSession("mindmax", {"query": "simulate"})
        assert r1["session_id"] != r2["session_id"]

    def test_capsule_is_preserved(self):
        result = runAgentSession("argus-prime", {"query": "quantum run"})
        assert result["capsule"] == "argus-prime"

    def test_status_is_dispatched(self):
        result = runAgentSession("deepagent", {"query": "unknown task"})
        assert result["status"] == "dispatched"

    def test_query_is_echoed(self):
        result = runAgentSession("wealthbridge", {"query": "invoice me"})
        assert result["query"] == "invoice me"

    def test_timestamp_is_recent(self):
        before = time.time()
        result = runAgentSession("mindmax", {"query": "test"})
        after = time.time()
        assert before <= result["timestamp"] <= after

    def test_empty_payload_does_not_raise(self):
        result = runAgentSession("deepagent", {})
        assert result["status"] == "dispatched"
        assert result["query"] == ""
