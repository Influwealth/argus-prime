import pytest
from router import CapsuleRouter


@pytest.fixture
def router():
    return CapsuleRouter()


class TestPredictRoute:
    def test_credit_keyword_routes_to_wealthbridge(self, router):
        assert router.predict_route("run credit analysis for federal worker") == "wealthbridge"

    def test_simulation_keyword_routes_to_mindmax(self, router):
        assert router.predict_route("run simulation for portfolio") == "mindmax"

    def test_outreach_keyword_routes_to_bridgebuilder(self, router):
        assert router.predict_route("send outreach to nonprofit partners") == "bridgebuilder"

    def test_quantum_keyword_routes_to_argus_prime(self, router):
        assert router.predict_route("start quantum optimization") == "argus-prime"

    def test_unknown_query_falls_back_to_deepagent(self, router):
        assert router.predict_route("do something completely unknown") == "deepagent"

    def test_empty_string_falls_back_to_deepagent(self, router):
        assert router.predict_route("") == "deepagent"

    def test_keyword_matching_is_case_insensitive(self, router):
        assert router.predict_route("CREDIT check needed") == "wealthbridge"
        assert router.predict_route("Run SIMULATION now") == "mindmax"
        assert router.predict_route("QUANTUM leap") == "argus-prime"

    def test_first_matching_keyword_wins_on_multi_keyword_query(self, router):
        # "credit" is the first key in self.routes, so it should win over "quantum"
        assert router.predict_route("credit quantum analysis") == "wealthbridge"

    def test_keyword_embedded_in_word_still_matches(self, router):
        # "outreach" contains "credit" at position 3 — should NOT match credit
        # but "outreach" itself contains the "outreach" key
        assert router.predict_route("outreach campaign") == "bridgebuilder"

    def test_none_input_raises_attribute_error(self, router):
        with pytest.raises(AttributeError):
            router.predict_route(None)

    def test_routes_dict_contains_expected_mappings(self, router):
        assert router.routes["credit"] == "wealthbridge"
        assert router.routes["simulation"] == "mindmax"
        assert router.routes["outreach"] == "bridgebuilder"
        assert router.routes["quantum"] == "argus-prime"
