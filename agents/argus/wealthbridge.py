import os
import logging
from agents.prediction_engine.capsule import PredictionEngineCapsule
from agents.vaultgemma.secure_comm import VaultGemmaSecureComm
from quantum_internet.quantum_adapter import QuantumAdapter


class WealthBridgeCapsule:
    """
    WealthBridge OS — matches users to credit cards, grants, contracts, and housing aid.
    Integrates the Prediction Engine for risk scoring and action suggestions.
    """

    def __init__(self):
        self.prediction_engine = PredictionEngineCapsule()
        self.vault = VaultGemmaSecureComm()
        self.quantum = QuantumAdapter()
        self.google_api_key = self.vault.get_secret("GOOGLE_DATA_COMMONS_API_KEY")
        logging.info("WealthBridgeCapsule initialized")

    # --- Trigger handlers (defined in wealthbridge.yaml) ---

    def credit_analysis(self, client: dict) -> dict:
        risk = self.prediction_engine.score_risk({"sector": "consumer_credit", **client})
        tensor_result = self.quantum.run_tensor_logic({"mode": "credit", "input": client})
        return {
            "capsule": "wealthbridge",
            "trigger": "credit_analysis",
            "client": client,
            "risk_score": risk.get("risk_score", 0.0),
            "tensor_result": tensor_result,
            "recommendations": [],
            "status": "stub",
        }

    def grant_match(self, client: dict) -> dict:
        suggestion = self.prediction_engine.suggest_action({"mode": "grant_match", **client})
        return {
            "capsule": "wealthbridge",
            "trigger": "grant_match",
            "client": client,
            "matches": [],
            "suggestion": suggestion.get("suggestion", ""),
            "status": "stub",
        }

    def housing_aid(self, client: dict) -> dict:
        risk = self.prediction_engine.score_risk({"sector": "housing", **client})
        return {
            "capsule": "wealthbridge",
            "trigger": "housing_aid",
            "client": client,
            "programs": [],
            "risk_score": risk.get("risk_score", 0.0),
            "status": "stub",
        }

    # --- WealthBridge OS models ---

    def generate_invoice(self, client: dict, line_items: list) -> dict:
        subtotal = sum(item.get("amount", 0.0) for item in line_items)
        tax_rate = float(os.environ.get("INVOICE_TAX_RATE", "0.0"))
        return {
            "capsule": "wealthbridge",
            "action": "generate_invoice",
            "client": client,
            "line_items": line_items,
            "subtotal": subtotal,
            "tax": round(subtotal * tax_rate, 2),
            "total": round(subtotal * (1 + tax_rate), 2),
            "status": "stub",
        }

    def cashflow_projection(self, client: dict, months: int = 12) -> dict:
        prediction = self.prediction_engine.predict_outcome(
            {"mode": "cashflow", "months": months, **client}
        )
        return {
            "capsule": "wealthbridge",
            "action": "cashflow_projection",
            "client": client,
            "months": months,
            "projected_monthly": [0.0] * months,
            "prediction": prediction.get("prediction", ""),
            "status": "stub",
        }
