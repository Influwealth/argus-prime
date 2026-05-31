# ARGUS-PRIME — Architecture Overview

## System Hierarchy

```
┌─────────────────────────────────────┐
│         DeepFlex (separate repo)    │  ← Supervisor / Brain
│  Orchestrates all nodes & agents    │
└────────────────┬────────────────────┘
                 │ dispatches commands via POST /deepflex/dispatch
                 ▼
┌─────────────────────────────────────┐
│         Argus Prime (this repo)     │  ← Offline IT / Ops / Security Node
│  Executes capsules, MCP calls,      │
│  NIM/vGPU inference, device ops     │
└───────┬─────────────┬───────────────┘
        │             │
        ▼             ▼
   Capsules       MCP Registry
   (Python)       (10 stubs)
        │
        ├── WealthBridge OS
        ├── Prediction Engine
        └── DeepAgent (fallback)

┌─────────────────────────────────────┐
│   Argus-Mobile (iOS/Android)        │  ← Mobile client, calls Argus
└─────────────────────────────────────┘

┌─────────────────────────────────────┐
│   WebMCP (separate TypeScript repo) │  ← Frontend layer
└─────────────────────────────────────┘
```

### Critical Distinction

| Node | Role | Initiates work? |
|---|---|---|
| **DeepFlex** | Supervisor / orchestrator / brain | Yes — issues all commands |
| **Argus Prime** | Offline IT / ops / security executor | No — only acts on DeepFlex commands |
| **WebMCP** | TypeScript frontend layer | Separate repo |
| **Argus-Mobile** | iOS/Android client | Calls Argus directly for local ops |
| **WealthBridge OS** | Business logic capsule | Executed by Argus |
| **Prediction Engine** | ICP/LLM/quantum capsule | Executed by Argus |

**Argus never self-orchestrates.** All top-level decisions come from DeepFlex.

---

## Entry Points

| File | Role |
|---|---|
| `main.py` | Starts Argus node via uvicorn on `HOST:PORT` (env vars) |
| `main_local_backup.py` | CLI for activating named capsules locally during dev |

---

## DeepFlex Interface (`deepflex/`)

The `deepflex/interface.py` module is the boundary between the DeepFlex supervisor
and this Argus execution node.

```python
from deepflex.interface import ArgusDeepFlexInterface, DeepFlexCommand

iface = ArgusDeepFlexInterface()

# DeepFlex dispatches a command to Argus
report = iface.receive_command(DeepFlexCommand(
    command_id="df-001",
    capsule="wealthbridge",
    payload={"query": "credit analysis", "user": "alice"},
))

print(report.status)   # "accepted"
print(report.node_id)  # "argus-prime"
```

| Class | Purpose |
|---|---|
| `DeepFlexCommand` | Command issued by DeepFlex to Argus |
| `ArgusReport` | Execution result returned to DeepFlex |
| `ArgusDeepFlexInterface` | Receives commands, executes via `runAgentSession`, logs results |

---

## API Surface (`agents/mindmax/api.py`)

All endpoints are callable by DeepFlex or directly for local dev.

| Method | Path | Caller | Description |
|---|---|---|---|
| GET | `/health` | DeepFlex / any | Node liveness check |
| POST | `/deepflex/dispatch` | **DeepFlex** | Primary entry point — receive a `DeepFlexCommand` and execute it |
| GET | `/deepflex/status` | **DeepFlex** | Poll Argus node status, role, and commands processed |
| POST | `/agent` | Local / dev | Internal capsule dispatch (bypasses DeepFlex interface) |
| POST | `/generate` | Internal | NIM/vGPU inference endpoint |

### POST /deepflex/dispatch

DeepFlex sends a command; Argus executes it and returns an `ArgusReport`.

Request:
```json
{
  "command_id": "df-001",
  "capsule": "wealthbridge",
  "payload": {"query": "credit analysis for alice"},
  "command_type": "execute_capsule",
  "priority": 0
}
```

Response:
```json
{
  "command_id": "df-001",
  "capsule": "wealthbridge",
  "status": "accepted",
  "result": { "session_id": "...", "query": "..." },
  "node_id": "argus-prime",
  "timestamp": 1234567890.0
}
```

---

## Internal Routing

`CapsuleRouter.predict_route(query)` maps keywords to capsules (used by `/agent`).
For DeepFlex-initiated work, the capsule is specified directly in the command.

| Keyword | Capsule |
|---|---|
| `credit`, `invoice`, `cashflow` | wealthbridge |
| `simulation` | mindmax |
| `outreach` | bridgebuilder |
| `quantum` | argus-prime |
| `predict`, `risk` | prediction_engine |
| _(no match)_ | deepagent |

---

## Session Tracking (`session.py`)

`runAgentSession(capsule, payload)` creates an execution session, logs it via
`AgentHandoff`, and returns a session metadata dict. Called by both `/agent`
and the DeepFlex interface.

---

## Capsule Modules (`agents/`)

```
agents/
├── argus/
│   └── wealthbridge.py     WealthBridgeCapsule — credit, grants, housing, invoices
├── prediction_engine/
│   └── capsule.py          PredictionEngineCapsule — risk, outcomes, action suggestions
├── mindmax/
│   ├── api.py              MindMaxAPI — FastAPI execution node
│   └── nim/nim_client.py   NIMClient — NVIDIA NIM inference stub
├── vaultgemma/
│   └── secure_comm.py      VaultGemmaSecureComm — secret management stub
└── deepagent/
    └── router.py           CLI fallback router
```

---

## MCP Registry (`mcp/`)

Argus executes MCP calls on behalf of DeepFlex. See [MCP_OVERVIEW.md](MCP_OVERVIEW.md).

---

## Mobile Client (`mobile/`)

See [MOBILE_CLIENT.md](MOBILE_CLIENT.md).

---

## Infrastructure

| File | Purpose |
|---|---|
| `infra/requirements.txt` | All Python dependencies |
| `infra/dockerfiles/Dockerfile.nim_worker` | NVIDIA PyTorch base, ports 8080/9090 |
| `infra/akash/mindmax.sdl.yaml` | Akash deployment (1 GPU, 4Gi RAM) |
| `.env.example` | All environment variable templates |

Environment variable to set this node's identity:
```
ARGUS_NODE_ID=argus-prime   # reported back to DeepFlex in all ArgusReport responses
```

---

## Testing

```bash
python3 -m pytest tests/ -v
```

All external integrations are stubbed — the full suite runs with no live endpoints.
