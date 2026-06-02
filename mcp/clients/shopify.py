import os
import logging


class ShopifyMCPClient:
    def __init__(self):
        self.endpoint = os.environ.get("SHOPIFY_MCP_URL", "")
        logging.info("ShopifyMCPClient initialized")

    def get_products(self) -> dict:
        return {"status": "stub", "client": "shopify", "products": []}

    def get_orders(self) -> dict:
        return {"status": "stub", "orders": []}

    def create_product(self, payload: dict) -> dict:
        return {"status": "stub", "action": "create_product", "payload": payload}
