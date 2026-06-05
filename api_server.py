"""
Argus HTTP API — FastAPI server exposing ArgusRuntime on port 7700.
Implements Sovereign Agent Protocol (SAP) headers for distributed tracing.
"""
from __future__ import annotations

import uuid
from typing import Any

from fastapi import FastAPI, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

from main import ArgusRuntime

app = FastAPI(title="Argus Prime API", version="1.0.0", description="Argus offline IT/ops/security node HTTP API")
runtime = ArgusRuntime()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:8000"],  # DeepFlex supervisor only
    allow_methods=["POST", "GET"],
    allow_headers=["*"],
)


class TaskRequest(BaseModel):
    task: str
    context: dict[str, Any] = {}


class TaskResponse(BaseModel):
    status: str
    decision: dict[str, Any]
    result: Any
    trace_id: str
    node_id: str = "argus-prime"


def _sap_headers(trace_id: str) -> dict[str, str]:
    return {
        "x-sap-node-id": "argus-prime",
        "x-sap-trace-id": trace_id,
        "x-sap-version": "1.0",
    }


@app.get("/health")
async def health() -> dict[str, str]:
    return {"status": "ok", "node": "argus-prime", "port": "7700"}


@app.post("/task", response_model=TaskResponse)
async def run_task(req: TaskRequest, request: Request) -> TaskResponse:
    trace_id = request.headers.get("x-sap-trace-id", str(uuid.uuid4()))
    try:
        result = runtime.run(req.task)
        return TaskResponse(
            status=result.get("status", "ok"),
            decision=result.get("decision", {}),
            result=result.get("result"),
            trace_id=trace_id,
        )
    except Exception as exc:
        raise HTTPException(status_code=500, detail=str(exc)) from exc


@app.post("/agent")
async def run_agent(req: TaskRequest, request: Request) -> dict[str, Any]:
    """Route directly to agent layer."""
    trace_id = request.headers.get("x-sap-trace-id", str(uuid.uuid4()))
    task_with_prefix = f"agent: {req.task}"
    result = runtime.run(task_with_prefix)
    return {"trace_id": trace_id, "node_id": "argus-prime", **result}


@app.post("/capsule")
async def run_capsule(req: TaskRequest, request: Request) -> dict[str, Any]:
    """Route directly to capsule layer."""
    trace_id = request.headers.get("x-sap-trace-id", str(uuid.uuid4()))
    task_with_prefix = f"capsule: {req.task}"
    result = runtime.run(task_with_prefix)
    return {"trace_id": trace_id, "node_id": "argus-prime", **result}


@app.post("/deepflex/callback")
async def deepflex_callback(payload: dict[str, Any]) -> dict[str, str]:
    """Callback endpoint for DeepFlex supervisor to push instructions."""
    return {"status": "received", "node_id": "argus-prime"}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=7700)
