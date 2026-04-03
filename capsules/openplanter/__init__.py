import logging
from typing import Any

LOGGER = logging.getLogger("argus.capsules.openplanter")


def sync_environment(context: dict[str, Any]) -> dict[str, Any]:
    LOGGER.info("OpenPlanter sync_environment invoked with context=%s", context)
    return {"status": "ok", "action": "sync_environment", "context": context}


def get_status(context: dict[str, Any]) -> dict[str, Any]:
    LOGGER.info("OpenPlanter get_status invoked with context=%s", context)
    return {
        "status": "ok",
        "action": "get_status",
        "environment": {"temperature_c": 23, "humidity_percent": 58, "lights": "scheduled"},
    }


def run_scene(name: str, context: dict[str, Any]) -> dict[str, Any]:
    LOGGER.info("OpenPlanter run_scene invoked for name=%s context=%s", name, context)
    return {"status": "ok", "action": "run_scene", "scene": name, "context": context}
