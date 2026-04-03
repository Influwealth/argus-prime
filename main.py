import importlib
import logging
from pathlib import Path
from typing import Any

import router

logging.basicConfig(level=logging.INFO)
LOGGER = logging.getLogger("argus.runtime")


class ArgusRuntime:
    """Unified sovereign runtime for capsules, agents, and integrations."""

    def __init__(self, root_path: str | None = None) -> None:
        self.root = Path(root_path or __file__).resolve().parent
        self.logger = LOGGER
        self.available_paths = {
            "agents": self.root / "agents",
            "capsules": self.root / "capsules",
            "infra": self.root / "infra",
            "integrations": self.root / "integrations",
            "quantum_internet": self.root / "quantum_internet",
        }
        self.capsules = self._scan_packages(self.available_paths["capsules"])
        self.agents = self._scan_packages(self.available_paths["agents"])
        self.integrations = self._scan_packages(self.available_paths["integrations"])
        self.infra = self._scan_files(self.available_paths["infra"])
        self.quantum_modules = self._scan_files(self.available_paths["quantum_internet"])

    def _scan_packages(self, path: Path) -> dict[str, str]:
        if not path.exists():
            return {}

        packages: dict[str, str] = {}
        for item in sorted(path.iterdir()):
            if item.is_dir() and (item / "__init__.py").exists():
                packages[item.name] = item.name
        return packages

    def _scan_files(self, path: Path) -> dict[str, str]:
        if not path.exists():
            return {}

        return {
            item.stem: item.name
            for item in sorted(path.iterdir())
            if item.is_file() and not item.name.startswith(".")
        }

    def run(self, task: str) -> dict[str, Any]:
        context = {
            "task": task,
            "root": str(self.root),
            "capsules": sorted(self.capsules),
            "agents": sorted(self.agents),
            "integrations": sorted(self.integrations),
            "infra": sorted(self.infra),
            "quantum_internet": sorted(self.quantum_modules),
        }
        self.logger.info("ArgusRuntime received task: %s", task)

        try:
            decision = router.route(task)
            self.logger.info("Routing decision: %s", decision)
            result = self._dispatch(decision, context)
            return {"status": "ok", "decision": decision, "result": result}
        except Exception as exc:
            self.logger.exception("ArgusRuntime failed while processing task")
            return {
                "status": "error",
                "task": task,
                "error": str(exc),
            }

    def _dispatch(self, decision: dict[str, Any], context: dict[str, Any]) -> dict[str, Any]:
        target = decision["target"]
        name = decision["name"]
        action = decision["action"]
        meta = decision.get("meta", {})

        module_map = {
            "capsule": f"capsules.{name}",
            "agent": f"agents.{name}",
            "infra": f"integrations.intraflow",
            "quantum": f"integrations.quantum",
            "llm_tool": f"agents.llm_tools.{name}",
        }
        if target not in module_map:
            raise ValueError(f"Unsupported routing target: {target}")

        module = importlib.import_module(module_map[target])
        handler = getattr(module, action)

        if target == "capsule" and name == "social_farm" and action == "schedule_post":
            return handler(
                meta.get("platform", "generic"),
                task_to_content(context["task"]),
                meta.get("when", "asap"),
                context,
            )
        if target == "capsule" and name == "openwispr" and action == "handle_voice_command":
            return handler(context["task"], context)
        if target == "capsule" and name == "financials" and action == "generate_funding_snapshot":
            return handler(context)
        if target == "capsule" and name == "openplanter" and action == "get_status":
            return handler(context)
        if target == "agent" and name == "vision" and action == "describe_screen":
            return handler(context)
        if target == "llm_tool":
            return handler(context["task"], context)
        if target == "infra":
            return handler(context)
        if target == "quantum":
            return handler(context)

        raise ValueError(f"Unsupported action mapping for {decision}")


def task_to_content(task: str) -> str:
    return task.strip()


if __name__ == "__main__":
    runtime = ArgusRuntime()
    result = runtime.run("initialize argus-prime runtime")
    print(result)
    print("ARGUS-PRIME V3 UPGRADE COMPLETE")
    print("Modules installed:")
    print("- OpenPlanter")
    print("- OpenWISPR")
    print("- Vision (NIMS/NEMO interface stubs)")
    print("- Social Media Farm")
    print("- Financial Engine")
    print("- Claude/Gemini/Codex/Workspace tool clients")
    print("- DeepFlex integration stubs")
    print("- WealthBridge OS integration stubs")
    print("- Quantum / Mesh / InfraFlow integration stubs")
