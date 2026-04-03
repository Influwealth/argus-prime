import logging
from typing import Any

LOGGER = logging.getLogger("argus.agents.llm_tools.claude")


def _response(action: str, payload: str, context: dict[str, Any]) -> dict[str, Any]:
    LOGGER.info("Claude client action=%s payload=%s context=%s", action, payload, context)
    return {"status": "ok", "tool": "claude", "action": action, "output": f"Claude stub response for: {payload}"}


def run(prompt: str, context: dict[str, Any]) -> dict[str, Any]:
    return _response("run", prompt, context)


def generate(prompt: str, context: dict[str, Any]) -> dict[str, Any]:
    return _response("generate", prompt, context)


def summarize(text: str, context: dict[str, Any]) -> dict[str, Any]:
    return _response("summarize", text, context)


def classify(text: str, context: dict[str, Any]) -> dict[str, Any]:
    return _response("classify", text, context)


def code(instruction: str, context: dict[str, Any]) -> dict[str, Any]:
    return _response("code", instruction, context)
