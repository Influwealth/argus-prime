import os
import logging


class WebLLMMCPClient:
    def __init__(self):
        self.endpoint = os.environ.get("WEB_LLM_MCP_URL", "")
        logging.info("WebLLMMCPClient initialized")

    def infer(self, prompt: str, model: str = "default") -> dict:
        return {"status": "stub", "client": "web_llm", "model": model, "text": ""}

    def is_healthy(self) -> bool:
        return True
