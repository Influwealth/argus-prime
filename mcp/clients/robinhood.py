import os
import logging


class RobinhoodMCPClient:
    def __init__(self):
        self.endpoint = os.environ.get("ROBINHOOD_MCP_URL", "")
        logging.info("RobinhoodMCPClient initialized")

    def get_portfolio(self) -> dict:
        return {"status": "stub", "client": "robinhood", "data": {}}

    def get_quote(self, symbol: str) -> dict:
        return {"status": "stub", "symbol": symbol, "price": None}

    def place_order(self, payload: dict) -> dict:
        return {"status": "stub", "action": "place_order", "payload": payload}
