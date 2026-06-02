import time
import uuid
import logging
from handoff import AgentHandoff

_handoff = AgentHandoff()


def runAgentSession(capsule: str, payload: dict) -> dict:
    session_id = str(uuid.uuid4())
    logging.info(f"[Session {session_id}] Dispatching to capsule: {capsule}")
    _handoff.delegate("argus-prime", capsule, payload.get("query", ""))
    return {
        "session_id": session_id,
        "capsule": capsule,
        "status": "dispatched",
        "query": payload.get("query", ""),
        "timestamp": time.time(),
    }
