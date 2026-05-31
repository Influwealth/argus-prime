import os
import logging


class X402MCPClient:
    def __init__(self):
        self.endpoint = os.environ.get("X402_MCP_URL", "")
        logging.info("X402MCPClient initialized")

    def pay(self, amount: float, currency: str, recipient: str) -> dict:
        return {"status": "stub", "client": "x402", "amount": amount, "currency": currency, "tx_id": None}

    def get_balance(self) -> dict:
        return {"status": "stub", "balance": None}
