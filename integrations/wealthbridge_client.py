import logging
from typing import Any

LOGGER = logging.getLogger("argus.integrations.wealthbridge")


def emit_sap_signal(code: str, payload: dict[str, Any], context: dict[str, Any]) -> dict[str, Any]:
    LOGGER.info(
        "WealthBridge emit_sap_signal invoked for code=%s payload=%s context=%s",
        code,
        payload,
        context,
    )
    return {"status": "ok", "action": "emit_sap_signal", "code": code, "payload": payload}


def receive_os_tasks(context: dict[str, Any]) -> dict[str, Any]:
    LOGGER.info("WealthBridge receive_os_tasks invoked with context=%s", context)
    return {"status": "ok", "action": "receive_os_tasks", "tasks": []}
