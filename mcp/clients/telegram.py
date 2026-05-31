import os
import logging


class TelegramMCPClient:
    def __init__(self):
        self.endpoint = os.environ.get("TELEGRAM_MCP_URL", "")
        logging.info("TelegramMCPClient initialized")

    def send_message(self, chat_id: str, text: str) -> dict:
        return {"status": "stub", "client": "telegram", "chat_id": chat_id, "sent": False}

    def get_updates(self) -> dict:
        return {"status": "stub", "updates": []}
