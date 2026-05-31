# ARGUS-PRIME Mobile Client Layer

## Purpose

`mobile/client.py` provides a thin, retry-safe HTTP client for sending agent
requests from mobile or edge environments to the ARGUS-PRIME API.

---

## Usage

```python
from mobile.client import sendToArgusPrime

result = sendToArgusPrime({
    "query": "run credit analysis for federal worker",
    "context": {"user_id": "u123", "region": "CA"}
})

print(result["capsule"])    # "wealthbridge"
print(result["session_id"]) # uuid4 string
print(result["status"])     # "dispatched"
```

---

## Configuration (Environment Variables)

| Variable | Default | Description |
|---|---|---|
| `ARGUS_PRIME_URL` | `http://localhost:8080` | Base URL of the ARGUS-PRIME API |
| `ARGUS_CLIENT_TIMEOUT` | `10` | Request timeout in seconds |
| `ARGUS_CLIENT_RETRIES` | `3` | Max retry attempts on connection failure |

---

## Retry Behaviour

`sendToArgusPrime` uses **exponential backoff** on connection errors and timeouts:

| Attempt | Delay before next |
|---|---|
| 1 | 2s |
| 2 | 4s |
| 3 | 8s |
| 4 (final) | — |

HTTP errors (4xx/5xx) are **not retried** — they return an error dict immediately
since retrying is unlikely to help.

---

## Return Value

On success:
```json
{
  "session_id": "...",
  "capsule": "wealthbridge",
  "status": "dispatched",
  "query": "run credit analysis",
  "timestamp": 1234567890.0
}
```

On failure:
```json
{
  "status": "error",
  "error": "Max retries exceeded",
  "url": "http://localhost:8080/agent"
}
```

---

## CoreML / Local Inference

For on-device inference on Apple Silicon, see `local_llm/`:

```python
from local_llm.coreml import runLocalLLM
from local_llm.whisper_coreml import transcribeAudio

text = runLocalLLM("Summarize my portfolio risk")
transcript = transcribeAudio("/tmp/voice_note.m4a", language="en")
```

Both functions are stubs — replace the bodies with CoreML/MLX or WhisperKit
bindings when targeting iOS/macOS.
