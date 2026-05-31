import os
import logging


class CoinbaseMCPClient:
    def __init__(self):
        self.endpoint = os.environ.get("COINBASE_MCP_URL", "")
        logging.info("CoinbaseMCPClient initialized")

    def get_balance(self, currency: str = "USD") -> dict:
        return {"status": "stub", "client": "coinbase", "currency": currency, "balance": None}

    def get_price(self, pair: str = "BTC-USD") -> dict:
        return {"status": "stub", "pair": pair, "price": None}

    def place_order(self, payload: dict) -> dict:
        return {"status": "stub", "action": "place_order", "payload": payload}
