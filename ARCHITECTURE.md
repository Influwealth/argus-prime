# ARGUS-PRIME — Architecture Overview

## System Summary

ARGUS-PRIME is a vGPU-accelerated, multi-agent autonomous framework for financial
analysis, quantum optimization, and automated outreach. It is implemented entirely
in Python and deployed on Akash Network with NVIDIA GPU support.

---

## Entry Points

| File | Role |
|---|---|
| `main.py` | Starts the MindMax vGPU Core Service via uvicorn on `HOST:PORT` |
| `main_local_backup.py` | CLI tool for activating named capsules locally |

---

## Core Modules

| Module | Class / Function | Responsibility |
|---|---|---|
| `router.py` | `CapsuleRouter` | Maps query keywords to capsule names |
| `handoff.py` | `AgentHandoff` | Logs inter-agent task delegation with timestamps |
| `introspect.py` | `CapsuleIntrospector` | Filesystem-based capsule health checks |
| `session.py` | `runAgentSession()` | Creates a session, delegates via AgentHandoff, returns session metadata |

---

## Agent Modules (`agents/`)

```
agents/
├── mindmax/
│   ├── api.py              MindMaxAPI (FastAPI) — REST surface
│   └── nim/nim_client.py   NIMClient — NVIDIA NIM inference stub
├── argus/
│   └── wealthbridge.py     WealthBridgeCapsule — financial analysis OS
├── prediction_engine/
│   └── capsule.py          PredictionEngineCapsule — risk scoring, outcome prediction
├── deepagent/
│   └── router.py           CLI router (argparse)
├── vaultgemma/
│   └── secure_comm.py      VaultGemmaSecureComm — secret management stub
└── outreach/
    └── youtube_uploader.py  YouTube automation stub
```

---

## API Surface (`agents/mindmax/api.py`)

| Method | Path | Description |
|---|---|---|
| GET | `/health` | Service liveness check |
| POST | `/generate` | NIM-accelerated text generation (query param: `prompt`) |
| POST | `/agent` | Route a query to the appropriate capsule via `CapsuleRouter` |

### POST /agent Request Body
```json
{
  "query": "run credit analysis for federal worker",
  "context": {}
}
```

### POST /agent Response
```json
{
  "session_id": "uuid4",
  "capsule": "wealthbridge",
  "status": "dispatched",
  "query": "run credit analysis for federal worker",
  "timestamp": 1234567890.0
}
```

---

## Capsule Routing

`CapsuleRouter.predict_route(query)` maps the first matching keyword to a capsule:

| Keyword | Capsule |
|---|---|
| `credit` | wealthbridge |
| `simulation` | mindmax |
| `outreach` | bridgebuilder |
| `quantum` | argus-prime |
| `predict` | prediction_engine |
| `risk` | prediction_engine |
| `invoice` | wealthbridge |
| `cashflow` | wealthbridge |
| _(no match)_ | deepagent |

---

## MCP Registry (`mcp/`)

See [MCP_OVERVIEW.md](MCP_OVERVIEW.md) for full details.

```
mcp/
├── mcp.config.json     Registry of all 10 MCP integrations
├── loader.py           load_mcp_config() + get_client(name)
└── clients/            One stub module per integration
```

---

## Capsules (`capsules/`)

YAML execution unit definitions:

| Capsule | Triggers |
|---|---|
| wealthbridge | credit_analysis, grant_match, housing_aid, invoice, cashflow |
| prediction_engine | predict_outcome, score_risk, suggest_action |
| mindmax | (NIM inference) |
| deepagent | (fallback router) |
| youtube-oauth-check | publish_youtube |

---

## Mobile Client Layer

See [MOBILE_CLIENT.md](MOBILE_CLIENT.md).

`mobile/client.py` exposes `sendToArgusPrime(payload)` with exponential-backoff retry.

---

## Local LLM / CoreML (`local_llm/`)

| Module | Function | Purpose |
|---|---|---|
| `coreml.py` | `runLocalLLM(prompt, model, max_tokens)` | On-device LLM inference (Apple Silicon stub) |
| `whisper_coreml.py` | `transcribeAudio(audio_path, language, model)` | On-device Whisper transcription stub |

---

## Infrastructure

| File | Purpose |
|---|---|
| `infra/requirements.txt` | All Python dependencies |
| `infra/dockerfiles/Dockerfile.nim_worker` | NVIDIA PyTorch base image, ports 8080/9090 |
| `infra/akash/mindmax.sdl.yaml` | Akash Network deployment (1 GPU, 4Gi RAM) |
| `.env.example` | Environment variable template |
| `setup.py` | Package registration |

---

## Testing

Run the full test suite:
```bash
python3 -m pytest tests/ -v
```

All external integrations are stubbed — the test suite runs with no live endpoints.
