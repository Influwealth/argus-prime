import os
import logging
from mcp.clients.web_llm import WebLLMMCPClient
from mcp.clients.cbi_insights import CBIInsightsMCPClient

_ICP_CAFFEINE_ENDPOINT = os.environ.get("ICP_CAFFEINE_ENDPOINT", "")


class PredictionEngineCapsule:
    """
    Prediction Engine — routes analytical queries through WebLLM and CBI Insights,
    with an ICP Caffeine Agent stub for on-chain context.
    """

    def __init__(self):
        self.web_llm = WebLLMMCPClient()
        self.cbi = CBIInsightsMCPClient()
        logging.info("PredictionEngineCapsule initialized")

    def predict_outcome(self, context: dict) -> dict:
        llm_result = self.web_llm.infer(
            prompt=f"Predict outcome for context: {context}",
            model="default",
        )
        return {
            "capsule": "prediction_engine",
            "action": "predict_outcome",
            "context": context,
            "prediction": llm_result.get("text", ""),
            "confidence": 0.0,
            "status": "stub",
        }

    def score_risk(self, context: dict) -> dict:
        sector = context.get("sector", "general")
        market_data = self.cbi.get_market_data(sector)
        return {
            "capsule": "prediction_engine",
            "action": "score_risk",
            "context": context,
            "risk_score": 0.0,
            "market_data": market_data,
            "status": "stub",
        }

    def suggest_action(self, context: dict) -> dict:
        llm_result = self.web_llm.infer(
            prompt=f"Suggest best action for context: {context}",
            model="default",
        )
        icp_context = {"endpoint": _ICP_CAFFEINE_ENDPOINT, "query": context}
        return {
            "capsule": "prediction_engine",
            "action": "suggest_action",
            "context": context,
            "suggestion": llm_result.get("text", ""),
            "icp_context": icp_context,
            "status": "stub",
        }
