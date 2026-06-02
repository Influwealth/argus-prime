import logging
from fastapi import FastAPI
from pydantic import BaseModel
from agents.mindmax.nim.nim_client import NIMClient
from router import CapsuleRouter
from session import runAgentSession
from deepflex.interface import ArgusDeepFlexInterface, DeepFlexCommand


class AgentRequest(BaseModel):
    query: str
    context: dict = {}


class DeepFlexDispatchRequest(BaseModel):
    command_id: str
    capsule: str
    payload: dict = {}
    command_type: str = "execute_capsule"
    priority: int = 0


class MindMaxAPI(FastAPI):
    """
    Argus Prime execution node API.
    Receives commands from DeepFlex supervisor and executes capsules, MCP calls,
    and NIM/vGPU inference. Does not orchestrate — DeepFlex does.
    """
    def __init__(self):
        super().__init__(
            title="Argus Prime — Execution Node API",
            version="1.0.0",
            description=(
                "Offline IT/ops/security executor. "
                "Supervised by DeepFlex. Executes capsules and MCP calls on command."
            ),
        )
        self.nim_client = NIMClient(endpoint="https://nim.internal")
        self.capsule_router = CapsuleRouter()
        self.deepflex_interface = ArgusDeepFlexInterface()
        self.startup_check()
        self.add_routes()

    def startup_check(self):
        logging.info(f"[Argus] Node starting. NIM status: {self.nim_client.is_healthy()}")

    def add_routes(self):
        @self.get("/health")
        async def health_check():
            return {"status": "ok", "service": "Argus Prime", "role": "offline-it-executor"}

        @self.post("/generate")
        async def generate_response(prompt: str):
            if self.nim_client.is_healthy():
                return {"response": f"NIM processed: {prompt[:20]}..."}
            return {"response": "Service unhealthy."}

        @self.post("/agent")
        async def agent_endpoint(request: AgentRequest):
            capsule = self.capsule_router.predict_route(request.query)
            return runAgentSession(capsule, {"query": request.query, "context": request.context})

        @self.post("/deepflex/dispatch")
        async def deepflex_dispatch(request: DeepFlexDispatchRequest):
            command = DeepFlexCommand(
                command_id=request.command_id,
                capsule=request.capsule,
                payload=request.payload,
                command_type=request.command_type,
                priority=request.priority,
            )
            return self.deepflex_interface.receive_command(command).to_dict()

        @self.get("/deepflex/status")
        async def deepflex_status():
            return self.deepflex_interface.report_status()

if __name__ == "__main__":
    app = MindMaxAPI()
