import json
import os
import logging
from pathlib import Path

_CONFIG_PATH = Path(__file__).parent / "mcp.config.json"

_CLIENT_MAP = {
    "robinhood":     "mcp.clients.robinhood.RobinhoodMCPClient",
    "coinbase":      "mcp.clients.coinbase.CoinbaseMCPClient",
    "telegram":      "mcp.clients.telegram.TelegramMCPClient",
    "shopify":       "mcp.clients.shopify.ShopifyMCPClient",
    "web_llm":       "mcp.clients.web_llm.WebLLMMCPClient",
    "turbo_quantum": "mcp.clients.turbo_quantum.TurboQuantumMCPClient",
    "cbi_insights":  "mcp.clients.cbi_insights.CBIInsightsMCPClient",
    "x402":          "mcp.clients.x402.X402MCPClient",
    "whisper":       "mcp.clients.whisper.WhisperMCPClient",
    "openjarvis":    "mcp.clients.openjarvis.OpenJarvisMCPClient",
}


def load_mcp_config() -> dict:
    with open(_CONFIG_PATH) as f:
        config = json.load(f)
    for entry in config.get("registry", []):
        entry["endpoint"] = os.environ.get(entry.get("env_url", ""), "")
    return config


def get_client(name: str):
    if name not in _CLIENT_MAP:
        raise ValueError(f"Unknown MCP client: '{name}'. Available: {list(_CLIENT_MAP)}")
    module_path, class_name = _CLIENT_MAP[name].rsplit(".", 1)
    import importlib
    module = importlib.import_module(module_path)
    cls = getattr(module, class_name)
    logging.info(f"MCP loader: instantiating {class_name}")
    return cls()
