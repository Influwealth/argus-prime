import logging
from typing import Any

LOGGER = logging.getLogger("argus.integrations.intraflow")


def start_core(context: dict[str, Any]) -> dict[str, Any]:
    LOGGER.info("InfraFlow start_core invoked with context=%s", context)
    return {"status": "ok", "action": "start_core", "service": "core"}


def start_ran(context: dict[str, Any]) -> dict[str, Any]:
    LOGGER.info("InfraFlow start_ran invoked with context=%s", context)
    return {"status": "ok", "action": "start_ran", "service": "ran"}


def status(context: dict[str, Any]) -> dict[str, Any]:
    LOGGER.info("InfraFlow status invoked with context=%s", context)
    return {"status": "ok", "action": "status", "system": "intraflow", "state": "ready"}
