import logging
from typing import Any

LOGGER = logging.getLogger("argus.integrations.mesh")


def register_node(context: dict[str, Any]) -> dict[str, Any]:
    LOGGER.info("Mesh register_node invoked with context=%s", context)
    return {"status": "ok", "action": "register_node", "node_id": "mesh-node-001"}


def list_nodes(context: dict[str, Any]) -> dict[str, Any]:
    LOGGER.info("Mesh list_nodes invoked with context=%s", context)
    return {"status": "ok", "action": "list_nodes", "nodes": ["mesh-node-001", "mesh-node-002"]}


def mesh_status(context: dict[str, Any]) -> dict[str, Any]:
    LOGGER.info("Mesh mesh_status invoked with context=%s", context)
    return {"status": "ok", "action": "mesh_status", "health": "nominal"}
