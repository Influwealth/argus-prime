import logging
from typing import Any

LOGGER = logging.getLogger("argus.integrations.quantum")


def connect(context: dict[str, Any]) -> dict[str, Any]:
    LOGGER.info("Quantum connect invoked with context=%s", context)
    return {"status": "ok", "action": "connect", "backend": "quantum_stub"}


def run_experiment(context: dict[str, Any]) -> dict[str, Any]:
    LOGGER.info("Quantum run_experiment invoked with context=%s", context)
    return {"status": "ok", "action": "run_experiment", "experiment_id": "q-exp-001"}


def status(context: dict[str, Any]) -> dict[str, Any]:
    LOGGER.info("Quantum status invoked with context=%s", context)
    return {"status": "ok", "action": "status", "system": "quantum", "state": "idle"}
