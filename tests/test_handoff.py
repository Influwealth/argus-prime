import time
import pytest
from handoff import AgentHandoff


@pytest.fixture
def handoff():
    return AgentHandoff()


class TestAgentHandoffInit:
    def test_log_starts_empty(self, handoff):
        assert handoff.log == []


class TestDelegate:
    def test_delegate_appends_entry_to_log(self, handoff):
        handoff.delegate("argus", "bridgebuilder", "follow-up task")
        assert len(handoff.log) == 1

    def test_delegate_entry_contains_correct_from_agent(self, handoff):
        handoff.delegate("argus", "bridgebuilder", "task")
        assert handoff.log[0]["from"] == "argus"

    def test_delegate_entry_contains_correct_to_agent(self, handoff):
        handoff.delegate("argus", "bridgebuilder", "task")
        assert handoff.log[0]["to"] == "bridgebuilder"

    def test_delegate_entry_contains_correct_task(self, handoff):
        handoff.delegate("argus", "bridgebuilder", "contact nonprofit")
        assert handoff.log[0]["task"] == "contact nonprofit"

    def test_delegate_entry_contains_timestamp(self, handoff):
        before = time.time()
        handoff.delegate("a", "b", "t")
        after = time.time()
        ts = handoff.log[0]["timestamp"]
        assert before <= ts <= after

    def test_multiple_delegates_preserve_order(self, handoff):
        handoff.delegate("a", "b", "first")
        handoff.delegate("b", "c", "second")
        handoff.delegate("c", "d", "third")
        assert [e["task"] for e in handoff.log] == ["first", "second", "third"]

    def test_multiple_delegates_accumulate_entries(self, handoff):
        for i in range(5):
            handoff.delegate("agent-a", "agent-b", f"task-{i}")
        assert len(handoff.log) == 5

    def test_each_entry_has_all_required_fields(self, handoff):
        handoff.delegate("src", "dst", "work")
        entry = handoff.log[0]
        assert set(entry.keys()) == {"from", "to", "task", "timestamp"}

    def test_timestamps_are_non_decreasing(self, handoff):
        handoff.delegate("a", "b", "first")
        handoff.delegate("b", "c", "second")
        assert handoff.log[0]["timestamp"] <= handoff.log[1]["timestamp"]
