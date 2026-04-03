import logging
from typing import Any

LOGGER = logging.getLogger("argus.integrations.deepflex")


def register_agent(name: str, context: dict[str, Any]) -> dict[str, Any]:
    LOGGER.info("DeepFlex register_agent invoked for name=%s context=%s", name, context)
    return {"status": "ok", "action": "register_agent", "agent": name}


def send_health(status: dict[str, Any], context: dict[str, Any]) -> dict[str, Any]:
    LOGGER.info("DeepFlex send_health invoked for status=%s context=%s", status, context)
    return {"status": "ok", "action": "send_health", "payload": status}


def receive_tasks(context: dict[str, Any]) -> dict[str, Any]:
    LOGGER.info("DeepFlex receive_tasks invoked with context=%s", context)
    return {"status": "ok", "action": "receive_tasks", "tasks": []}
