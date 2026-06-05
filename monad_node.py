"""
Argus Prime — MONAD NODE_ALPHA Port Member

Argus Prime runs on port 7700, registered under NODE_ALPHA (Sovereign Control Hub,
ports 8000–8099). It receives task dispatches from the DeepFlex Supervisor and
executes device-layer operations (capsule execution, agent dispatch, integration calls).

Sync: Argus participates in MONAD v3.7 sync as a subordinate of NODE_ALPHA.
It does NOT run the full Pentagon sync — only DeepFlex Supervisor does.
"""

from __future__ import annotations

import json
import logging
import time
import uuid
from dataclasses import dataclass, field
from typing import Any

log = logging.getLogger(__name__)

MONAD_VERSION = "3.7"
NODE_ID = "NODE_ALPHA"
ARGUS_PORT = 7700
DEEPFLEX_PORT = 8000


@dataclass
class MONADRegistration:
    """Argus Prime registration record sent to DeepFlex Supervisor on startup."""
    service_id: str = "argus-prime"
    node_id: str = NODE_ID
    port: int = ARGUS_PORT
    capabilities: list[str] = field(default_factory=lambda: [
        "device_ops",
        "capsule_execution",
        "agent_dispatch",
        "integration_calls",
        "security_audit",
    ])
    monad_version: str = MONAD_VERSION
    registered_at: float = field(default_factory=time.time)
    trace_id: str = field(default_factory=lambda: str(uuid.uuid4()))

    def as_sap_headers(self) -> dict[str, str]:
        return {
            "x-sap-node-id": self.node_id,
            "x-sap-trace-id": self.trace_id,
            "x-sap-version": self.monad_version,
            "x-sap-capsule": f"argus-{self.registered_at:.0f}",
        }

    def to_dict(self) -> dict[str, Any]:
        return {
            "service_id": self.service_id,
            "node_id": self.node_id,
            "port": self.port,
            "capabilities": self.capabilities,
            "monad_version": self.monad_version,
            "registered_at": self.registered_at,
            "trace_id": self.trace_id,
        }


class ArgusNodeHandler:
    """
    Handles MONAD mesh registration and heartbeat for Argus Prime.
    Called by api_server.py on startup and every 30s.
    """

    HEARTBEAT_INTERVAL = 30
    TTL = {"critical": 0.5, "standard": 5.0, "background": 60.0}

    def __init__(self):
        self.registration = MONADRegistration()
        self._registered = False
        self._last_heartbeat: float = 0.0

    def register(self, deepflex_client: Any) -> bool:
        """
        POST registration to DeepFlex Supervisor at /services/register.
        deepflex_client is the existing deepflex_client.py module.
        """
        try:
            result = deepflex_client.call_deepflex(
                task="service.register",
                context=self.registration.to_dict(),
            )
            self._registered = True
            self._last_heartbeat = time.time()
            log.info(
                "[MONAD] Argus Prime registered with NODE_ALPHA trace=%s",
                self.registration.trace_id,
            )
            return True
        except Exception as exc:
            log.warning("[MONAD] Registration failed (DeepFlex not yet up): %s", exc)
            return False

    def heartbeat(self, deepflex_client: Any) -> bool:
        """Send 30s heartbeat to DeepFlex Supervisor."""
        if time.time() - self._last_heartbeat < self.HEARTBEAT_INTERVAL:
            return True
        try:
            deepflex_client.call_deepflex(
                task="service.heartbeat",
                context={"service_id": "argus-prime", "node_id": NODE_ID, "port": ARGUS_PORT},
            )
            self._last_heartbeat = time.time()
            return True
        except Exception as exc:
            log.warning("[MONAD] Heartbeat failed: %s", exc)
            return False

    def status(self) -> dict[str, Any]:
        return {
            "service_id": "argus-prime",
            "node_id": NODE_ID,
            "monad_version": MONAD_VERSION,
            "port": ARGUS_PORT,
            "registered": self._registered,
            "last_heartbeat": self._last_heartbeat,
            "capabilities": self.registration.capabilities,
        }


_handler = ArgusNodeHandler()


def get_handler() -> ArgusNodeHandler:
    return _handler
