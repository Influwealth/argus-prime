import os
import time
import logging
from dataclasses import dataclass, field
from session import runAgentSession

NODE_ID = os.environ.get("ARGUS_NODE_ID", "argus-prime")


@dataclass
class DeepFlexCommand:
    """
    A unit of work dispatched from the DeepFlex supervisor to this Argus node.
    Argus never self-initiates — it only acts on commands it receives.
    """
    command_id: str
    capsule: str
    payload: dict = field(default_factory=dict)
    command_type: str = "execute_capsule"
    priority: int = 0
    issued_by: str = "deepflex"


@dataclass
class ArgusReport:
    """Result returned from Argus to DeepFlex after executing a command."""
    command_id: str
    capsule: str
    status: str
    result: dict = field(default_factory=dict)
    node_id: str = field(default_factory=lambda: NODE_ID)
    timestamp: float = field(default_factory=time.time)

    def to_dict(self) -> dict:
        return {
            "command_id": self.command_id,
            "capsule": self.capsule,
            "status": self.status,
            "result": self.result,
            "node_id": self.node_id,
            "timestamp": self.timestamp,
        }


class ArgusDeepFlexInterface:
    """
    The boundary between DeepFlex (supervisor/brain) and Argus (offline IT/ops executor).

    DeepFlex sends DeepFlexCommand objects; Argus executes and returns ArgusReport.
    Argus does not orchestrate — it executes capsules, MCP calls, and device-level
    operations on behalf of DeepFlex.
    """

    def __init__(self):
        self._command_log: list[dict] = []
        logging.info(f"[Argus] DeepFlex interface ready. Node: {NODE_ID}. Supervisor: deepflex")

    def receive_command(self, command: DeepFlexCommand) -> ArgusReport:
        logging.info(
            f"[Argus] Command {command.command_id} received from {command.issued_by}: "
            f"type={command.command_type} capsule={command.capsule}"
        )
        try:
            result = runAgentSession(command.capsule, command.payload)
            status = "accepted"
        except Exception as e:
            logging.error(f"[Argus] Command {command.command_id} failed: {e}")
            result = {"error": str(e)}
            status = "failed"

        report = ArgusReport(
            command_id=command.command_id,
            capsule=command.capsule,
            status=status,
            result=result,
        )
        self._command_log.append(report.to_dict())
        return report

    def report_status(self) -> dict:
        return {
            "node_id": NODE_ID,
            "role": "offline-it-executor",
            "supervisor": "deepflex",
            "commands_processed": len(self._command_log),
            "timestamp": time.time(),
        }
