# MCP (Model Context Protocol) Registry — Overview

## Role in the Hierarchy

**DeepFlex** decides *which* MCP calls to make and *when*.
**Argus** executes those calls and returns results.

MCP clients live in `mcp/clients/` and are invoked by Argus capsules
(WealthBridge, Prediction Engine, etc.) as part of executing a DeepFlexCommand.
They are never called directly by DeepFlex.

```
DeepFlex  ──dispatch──▶  Argus  ──capsule──▶  PredictionEngine
                                                    │
                                                    ├── web_llm MCP
                                                    └── cbi_insights MCP
```

---

## Configuration

**`mcp/mcp.config.json`** — single source of truth for registered integrations.

Each entry maps a client name to an environment variable that holds its endpoint:

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

config = load_mcp_config()        # full resolved config
client = get_client("robinhood")  # instantiates RobinhoodMCPClient
```

`get_client(name)` raises `ValueError` for unknown names.

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

## Which Capsule Uses Which MCP

| Capsule | MCP clients used |
|---|---|
| `prediction_engine` | `web_llm`, `cbi_insights` |
| `wealthbridge` | via prediction_engine (`web_llm`, `cbi_insights`) |
| `local_llm/whisper_coreml` | `whisper` (remote fallback when CoreML unavailable) |

---

## Adding a New MCP Client

1. Add an entry to `mcp/mcp.config.json`
2. Add the env var to `.env.example`
3. Create `mcp/clients/<name>.py` following the existing stub pattern
4. Register the dotted class path in `_CLIENT_MAP` in `mcp/loader.py`
5. Add tests to `tests/test_mcp_loader.py`
