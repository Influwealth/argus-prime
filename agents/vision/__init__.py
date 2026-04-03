import logging
from typing import Any

LOGGER = logging.getLogger("argus.agents.vision")


def capture_screenshot(context: dict[str, Any]) -> dict[str, Any]:
    LOGGER.info("Vision capture_screenshot invoked with context=%s", context)
    return {"status": "ok", "action": "capture_screenshot", "image_path": "memory://vision/screenshot.png"}


def ocr(image_path: str, context: dict[str, Any]) -> dict[str, Any]:
    LOGGER.info("Vision ocr invoked for image_path=%s context=%s", image_path, context)
    return {"status": "ok", "action": "ocr", "image_path": image_path, "text": "Stub OCR text"}


def describe_screen(context: dict[str, Any]) -> dict[str, Any]:
    LOGGER.info("Vision describe_screen invoked with context=%s", context)
    return {
        "status": "ok",
        "action": "describe_screen",
        "description": "Stubbed screen description from the NIMS/NEMO interface.",
    }


def detect_elements(context: dict[str, Any]) -> dict[str, Any]:
    LOGGER.info("Vision detect_elements invoked with context=%s", context)
    return {
        "status": "ok",
        "action": "detect_elements",
        "elements": [{"type": "button", "label": "Submit"}, {"type": "input", "label": "Search"}],
    }
