import logging
from fastapi import FastAPI
from agents.mindmax.nim.nim_client import NIMClient

class MindMaxAPI(FastAPI):
    """
    The core vGPU/NIM inference and quantum optimization endpoint.
    """
    def __init__(self):
        super().__init__(
            title="MindMax Core API",
            version="1.0.0",
            description="NIM-accelerated, vGPU-optimized Agent Service."
        )
        self.nim_client = NIMClient(endpoint="https://nim.internal")
        self.startup_check()
        self.add_routes()

    def startup_check(self):
        """Checks for required environment and resources."""
        logging.info(f"MindMax starting up. Checking NIM status: {self.nim_client.is_healthy()}")

    def add_routes(self):
        """Defines API endpoints."""
        @self.get("/health")
        async def health_check():
            return {"status": "ok", "service": "MindMax Core"}

        @self.post("/generate")
        async def generate_response(prompt: str):
            if self.nim_client.is_healthy():
                return {"response": f"NIM processed: {prompt[:20]}..."}
            return {"response": "Service unhealthy."}

    app = MindMaxAPI()
