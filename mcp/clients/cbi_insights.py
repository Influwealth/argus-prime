import os
import logging


class CBIInsightsMCPClient:
    def __init__(self):
        self.endpoint = os.environ.get("CBI_INSIGHTS_MCP_URL", "")
        logging.info("CBIInsightsMCPClient initialized")

    def get_market_data(self, sector: str) -> dict:
        return {"status": "stub", "client": "cbi_insights", "sector": sector, "data": {}}

    def get_funding_rounds(self, company: str) -> dict:
        return {"status": "stub", "company": company, "rounds": []}
