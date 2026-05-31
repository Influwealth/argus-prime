# MCP (Model Context Protocol) Registry — Overview

## Purpose

The MCP registry provides a unified, config-driven interface to all external
service integrations used by ARGUS-PRIME capsules. All clients are currently
stubbed — replace the method bodies with live SDK/HTTP calls once credentials
and endpoints are available.

---

## Configuration

**`mcp/mcp.config.json`** — the single source of truth for registered integrations.

Each entry maps a client name to an environment variable that holds its endpoint URL:

```json
{
  "version": "1.0",
  "registry": [
    {"name": "robinhood", "env_url": "ROBINHOOD_MCP_URL", "enabled": true},
    ...
  ]
}
```

At runtime, `load_mcp_config()` resolves `env_url` → `endpoint` via `os.environ`.

---

## Loading Clients

```python
from mcp.loader import load_mcp_config, get_client

# Get the full resolved config
config = load_mcp_config()

# Instantiate a named client
client = get_client("robinhood")
portfolio = client.get_portfolio()
```

`get_client(name)` dynamically imports and instantiates the correct class.
It raises `ValueError` for unknown client names.

---

## Registered Clients

| Name | Class | Env Var | Key Methods |
|---|---|---|---|
| `robinhood` | `RobinhoodMCPClient` | `ROBINHOOD_MCP_URL` | `get_portfolio()`, `get_quote()`, `place_order()` |
| `coinbase` | `CoinbaseMCPClient` | `COINBASE_MCP_URL` | `get_balance()`, `get_price()`, `place_order()` |
| `telegram` | `TelegramMCPClient` | `TELEGRAM_MCP_URL` | `send_message()`, `get_updates()` |
| `shopify` | `ShopifyMCPClient` | `SHOPIFY_MCP_URL` | `get_products()`, `get_orders()`, `create_product()` |
| `web_llm` | `WebLLMMCPClient` | `WEB_LLM_MCP_URL` | `infer()`, `is_healthy()` |
| `turbo_quantum` | `TurboQuantumMCPClient` | `TURBO_QUANTUM_MCP_URL` | `run_circuit()`, `optimize()` |
| `cbi_insights` | `CBIInsightsMCPClient` | `CBI_INSIGHTS_MCP_URL` | `get_market_data()`, `get_funding_rounds()` |
| `x402` | `X402MCPClient` | `X402_MCP_URL` | `pay()`, `get_balance()` |
| `whisper` | `WhisperMCPClient` | `WHISPER_MCP_URL` | `transcribe()`, `is_healthy()` |
| `openjarvis` | `OpenJarvisMCPClient` | `OPENJARVIS_MCP_URL` | `execute_task()`, `is_healthy()` |

---

## Capsule Integrations

| Capsule | Uses |
|---|---|
| `prediction_engine` | `web_llm`, `cbi_insights` |
| `wealthbridge` | `prediction_engine` (which uses `web_llm`, `cbi_insights`) |
| `local_llm/whisper_coreml` | `whisper` (remote fallback when CoreML unavailable) |

---

## Adding a New MCP Client

1. Add an entry to `mcp/mcp.config.json`
2. Add an env var to `.env.example`
3. Create `mcp/clients/<name>.py` with a class following the existing pattern
4. Register the class path in `_CLIENT_MAP` in `mcp/loader.py`
5. Add tests to `tests/test_mcp_loader.py`
