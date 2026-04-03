from pathlib import Path


ROOT = Path(__file__).resolve().parent


def _list_dirs(path: Path) -> list[str]:
    if not path.exists():
        return []
    return sorted(item.name for item in path.iterdir() if item.is_dir() and not item.name.startswith("__"))


def list_capsules() -> list[str]:
    capsule_root = ROOT / "capsules"
    yaml_capsules = sorted(item.stem for item in capsule_root.glob("*.yaml"))
    package_capsules = sorted(
        item.name
        for item in capsule_root.iterdir()
        if item.is_dir() and (item / "__init__.py").exists()
    ) if capsule_root.exists() else []
    return sorted(set(yaml_capsules + package_capsules))


def list_agents() -> list[str]:
    return _list_dirs(ROOT / "agents")


def health_summary() -> dict[str, str]:
    checks = {
        "agents": "OK" if (ROOT / "agents").exists() else "ERROR",
        "capsules": "OK" if (ROOT / "capsules").exists() else "ERROR",
        "infra": "OK" if (ROOT / "infra").exists() else "ERROR",
        "integrations": "OK" if (ROOT / "integrations").exists() else "ERROR",
        "quantum_internet": "OK" if (ROOT / "quantum_internet").exists() else "ERROR",
    }
    return checks


if __name__ == "__main__":
    print("Available Capsules:", list_capsules())
    print("Available Agents:", list_agents())
    print("Argus Health:", health_summary())
