import logging
from typing import Any

try:
    import revenue_flow
except Exception:  # pragma: no cover - optional legacy module
    revenue_flow = None

LOGGER = logging.getLogger("argus.capsules.financials")


def run_daily_report(context: dict[str, Any]) -> dict[str, Any]:
    LOGGER.info("Financials run_daily_report invoked with context=%s", context)
    return {
        "status": "ok",
        "action": "run_daily_report",
        "report": {"revenue_usd": 12500, "expenses_usd": 3100, "net_usd": 9400},
        "revenue_flow_loaded": revenue_flow is not None,
    }


def sync_balances(context: dict[str, Any]) -> dict[str, Any]:
    LOGGER.info("Financials sync_balances invoked with context=%s", context)
    return {
        "status": "ok",
        "action": "sync_balances",
        "balances": {"treasury_usd": 42000, "operating_usd": 11800, "reserves_usd": 90500},
    }


def generate_funding_snapshot(context: dict[str, Any]) -> dict[str, Any]:
    LOGGER.info("Financials generate_funding_snapshot invoked with context=%s", context)
    return {
        "status": "ok",
        "action": "generate_funding_snapshot",
        "snapshot": {
            "runway_months": 14,
            "cash_on_hand_usd": 132500,
            "pipeline_usd": 480000,
            "burn_rate_usd": 9500,
        },
    }
