"""
HTTP client for calling the DeepFlex Supervisor from Argus.
Replaces the boundary-violating agents/deepagent/ local copy.
"""
from __future__ import annotations

import uuid
from typing import Any

import requests

DEEPFLEX_BASE_URL = "http://localhost:8000"
NODE_ID = "argus-prime"


def call_deepflex(task: str, context: dict[str, Any] | None = None) -> dict[str, Any]:
    """Send a task to the DeepFlex supervisor and return its response."""
    trace_id = str(uuid.uuid4())
    headers = {
        "x-sap-node-id": NODE_ID,
        "x-sap-trace-id": trace_id,
        "x-sap-version": "1.0",
        "x-sap-capsule": "argus-router",
        "Content-Type": "application/json",
    }
    payload = {"task": task, "source": NODE_ID, "context": context or {}}
    try:
        resp = requests.post(f"{DEEPFLEX_BASE_URL}/task", json=payload, headers=headers, timeout=30)
        resp.raise_for_status()
        return resp.json()
    except requests.RequestException as exc:
        return {"status": "error", "error": str(exc), "trace_id": trace_id, "node_id": NODE_ID}
