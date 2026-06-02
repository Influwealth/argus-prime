import os
import logging


class OpenJarvisMCPClient:
    def __init__(self):
        self.endpoint = os.environ.get("OPENJARVIS_MCP_URL", "")
        logging.info("OpenJarvisMCPClient initialized")

    def execute_task(self, task: str, context: dict = None) -> dict:
        return {"status": "stub", "client": "openjarvis", "task": task, "result": None}

    def is_healthy(self) -> bool:
        return True
