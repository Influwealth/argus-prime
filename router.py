from typing import Any


def route(task: str) -> dict[str, Any]:
    """Return the Argus routing decision for a natural-language task."""
    lowered = task.lower()

    pattern_map = [
        (
            ("social", "twitter", "instagram", "tiktok", "youtube"),
            {
                "target": "capsule",
                "name": "social_farm",
                "action": "schedule_post",
                "meta": {"platform": first_match(lowered, ("twitter", "instagram", "tiktok", "youtube")) or "social"},
            },
        ),
        (
            ("finance", "revenue", "treasury", "funding"),
            {
                "target": "capsule",
                "name": "financials",
                "action": "generate_funding_snapshot",
                "meta": {"domain": "finance"},
            },
        ),
        (
            ("vision", "screen", "screenshot", "ui"),
            {
                "target": "agent",
                "name": "vision",
                "action": "describe_screen",
                "meta": {"mode": "screen"},
            },
        ),
        (
            ("voice", "speak", "listen"),
            {
                "target": "capsule",
                "name": "openwispr",
                "action": "handle_voice_command",
                "meta": {"mode": "voice"},
            },
        ),
        (
            ("planter", "environment", "greenhouse"),
            {
                "target": "capsule",
                "name": "openplanter",
                "action": "get_status",
                "meta": {"mode": "environment"},
            },
        ),
        (
            ("code", "refactor", "repo", "git"),
            {
                "target": "llm_tool",
                "name": "codex_client",
                "action": "code",
                "meta": {"tool": "codex"},
            },
        ),
        (
            ("doc", "write", "summarize"),
            {
                "target": "llm_tool",
                "name": llm_doc_tool(lowered),
                "action": llm_doc_action(lowered),
                "meta": {"tool": "documentation"},
            },
        ),
        (
            ("sheet", "gmail", "calendar"),
            {
                "target": "llm_tool",
                "name": "workspace_client",
                "action": "run",
                "meta": {"tool": "workspace"},
            },
        ),
        (
            ("quantum", "qubit", "experiment"),
            {
                "target": "quantum",
                "name": "quantum",
                "action": "status",
                "meta": {"domain": "quantum"},
            },
        ),
        (
            ("infra", "mesh", "radio", "ran", "core"),
            {
                "target": "infra",
                "name": "intraflow",
                "action": "status",
                "meta": {"domain": "infra"},
            },
        ),
    ]

    for keywords, decision in pattern_map:
        if any(keyword in lowered for keyword in keywords):
            return decision

    return {
        "target": "llm_tool",
        "name": "gemini_client",
        "action": "run",
        "meta": {"tool": "fallback"},
    }


def first_match(task: str, keywords: tuple[str, ...]) -> str | None:
    for keyword in keywords:
        if keyword in task:
            return keyword
    return None


def llm_doc_tool(task: str) -> str:
    if "summarize" in task:
        return "claude_client"
    return "gemini_client"


def llm_doc_action(task: str) -> str:
    if "summarize" in task:
        return "summarize"
    if "write" in task:
        return "generate"
    return "run"
