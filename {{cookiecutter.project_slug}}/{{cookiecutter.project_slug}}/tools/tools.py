from typing import Any, Dict, List

from {{ cookiecutter.project_slug }}.connectors.mcp_client import build_mcp_tooling

tools = [
    {
        "type": "function",
        "function": {
            "name": "get_delivery_date",
            "description": "Get the delivery date for a customer's order. Call this whenever you need to know the delivery date, for example when a customer asks 'Where is my package'",
            "parameters": {
                "type": "object",
                "properties": {
                    "order_id": {
                        "type": "string",
                        "description": "The customer's order ID.",
                    },
                },
                "required": ["order_id"],
                "additionalProperties": False,
            },
        }
    }
]


def assemble_tools(config: Dict[str, Any]) -> List[dict]:
    """
    Combine built-in tools with MCP tooling derived from configuration. If the
    config already contains pre-built MCP tool specs, they are reused to avoid
    recomputing.
    """
    base_tools = list(tools)
    mcp_tooling = config.get("mcp_tools") or build_mcp_tooling(config.get("mcp_connectors", []))
    return base_tools + mcp_tooling
