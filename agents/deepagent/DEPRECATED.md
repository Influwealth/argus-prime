# DEPRECATED — Boundary Violation

This directory (`agents/deepagent/`) is a boundary violation: DeepFlex supervisor logic
does not belong inside the Argus node repo.

**Status**: Scheduled for removal. Do NOT add new code here.

**Migration**: All DeepFlex supervisor calls from Argus must go through HTTP:
- DeepFlex Supervisor: `http://localhost:8000` (see contracts/deepflex-argus-api.yaml)
- Use `requests.post("http://localhost:8000/task", json={"task": ..., "source": "argus-prime"})`

**Removal**: This directory will be deleted once the HTTP integration is wired in `router.py`.
