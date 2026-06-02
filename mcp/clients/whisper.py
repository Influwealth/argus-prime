import os
import logging


class WhisperMCPClient:
    def __init__(self):
        self.endpoint = os.environ.get("WHISPER_MCP_URL", "")
        logging.info("WhisperMCPClient initialized")

    def transcribe(self, audio_path: str, language: str = "en") -> dict:
        return {"status": "stub", "client": "whisper", "audio_path": audio_path, "transcript": ""}

    def is_healthy(self) -> bool:
        return True
