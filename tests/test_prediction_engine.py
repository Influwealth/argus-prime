import pytest
from agents.prediction_engine.capsule import PredictionEngineCapsule


@pytest.fixture
def engine():
    return PredictionEngineCapsule()


class TestPredictOutcome:
    def test_returns_dict(self, engine):
        result = engine.predict_outcome({"user": "test"})
        assert isinstance(result, dict)

    def test_capsule_field(self, engine):
        result = engine.predict_outcome({})
        assert result["capsule"] == "prediction_engine"

    def test_action_field(self, engine):
        result = engine.predict_outcome({})
        assert result["action"] == "predict_outcome"

    def test_context_is_echoed(self, engine):
        ctx = {"user": "alice", "income": 50000}
        result = engine.predict_outcome(ctx)
        assert result["context"] == ctx

    def test_status_is_stub(self, engine):
        result = engine.predict_outcome({})
        assert result["status"] == "stub"


class TestScoreRisk:
    def test_returns_dict(self, engine):
        result = engine.score_risk({"sector": "housing"})
        assert isinstance(result, dict)

    def test_capsule_field(self, engine):
        result = engine.score_risk({})
        assert result["capsule"] == "prediction_engine"

    def test_action_field(self, engine):
        result = engine.score_risk({})
        assert result["action"] == "score_risk"

    def test_risk_score_is_float(self, engine):
        result = engine.score_risk({})
        assert isinstance(result["risk_score"], float)

    def test_market_data_present(self, engine):
        result = engine.score_risk({"sector": "fintech"})
        assert "market_data" in result


class TestSuggestAction:
    def test_returns_dict(self, engine):
        result = engine.suggest_action({"goal": "save"})
        assert isinstance(result, dict)

    def test_capsule_field(self, engine):
        result = engine.suggest_action({})
        assert result["capsule"] == "prediction_engine"

    def test_action_field(self, engine):
        result = engine.suggest_action({})
        assert result["action"] == "suggest_action"

    def test_icp_context_present(self, engine):
        result = engine.suggest_action({})
        assert "icp_context" in result
