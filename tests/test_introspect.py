import pytest
from introspect import list_capsules, list_agents, health_summary


class TestListCapsules:
    def test_returns_list(self):
        assert isinstance(list_capsules(), list)

    def test_returns_strings(self):
        assert all(isinstance(c, str) for c in list_capsules())

    def test_includes_known_yaml_capsules(self):
        result = list_capsules()
        assert "wealthbridge" in result or "prediction_engine" in result

    def test_no_yaml_extension_in_names(self):
        for name in list_capsules():
            assert not name.endswith(".yaml")

    def test_sorted_result(self):
        result = list_capsules()
        assert result == sorted(result)


class TestListAgents:
    def test_returns_list(self):
        assert isinstance(list_agents(), list)

    def test_returns_strings(self):
        assert all(isinstance(a, str) for a in list_agents())

    def test_includes_mindmax_agent(self):
        assert "mindmax" in list_agents()

    def test_includes_argus_agent(self):
        assert "argus" in list_agents()


class TestHealthSummary:
    def test_returns_dict(self):
        assert isinstance(health_summary(), dict)

    def test_has_agents_key(self):
        assert "agents" in health_summary()

    def test_has_capsules_key(self):
        assert "capsules" in health_summary()

    def test_agents_is_ok(self):
        assert health_summary()["agents"] == "OK"

    def test_capsules_is_ok(self):
        assert health_summary()["capsules"] == "OK"

    def test_all_values_are_strings(self):
        for v in health_summary().values():
            assert isinstance(v, str)
