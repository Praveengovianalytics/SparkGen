"""Minimal MCP connectivity scaffold with YAML-based configuration.

This module scaffolds integration with Model Context Protocol (MCP) gateways.
Projects generated from the template can register gateways and tools via
`config/mcp_connectors.yaml` and expose only the `active` entries to agents.
Credentials should be supplied via environment variables to avoid committing
secrets to version control.
"""

import os
import re
from dataclasses import dataclass, field, asdict
from pathlib import Path
from typing import Any, Dict, List, Optional

import yaml


ENV_VAR_PATTERN = re.compile(r"^\\${(?P<env_var>[A-Z0-9_]+)}$")


@dataclass
class MCPToolConfig:
    """Configuration for a single MCP tool."""

    name: str
    resource: str
    description: str = ""
    active: bool = True


@dataclass
class MCPGatewayConfig:
    """Configuration for an MCP gateway and its tools."""

    name: str
    host: str
    port: int
    protocol: str = "ws"
    active: bool = True
    description: str = ""
    credentials: Dict[str, str] = field(default_factory=dict)
    tools: List[MCPToolConfig] = field(default_factory=list)
    metadata: Dict[str, Any] = field(default_factory=dict)


class MCPClient:
    """Lightweight MCP client scaffold."""

    def __init__(
        self,
        host: str = "localhost",
        port: int = 8000,
        protocol: str = "ws",
        credentials: Optional[Dict[str, Any]] = None,
        metadata: Optional[Dict[str, Any]] = None,
    ):
        self.host = host
        self.port = port
        self.protocol = protocol
        self.credentials = credentials or {}
        self.metadata = metadata or {}

    def connect(self) -> None:
        """Placeholder connect method. Extend with real MCP handshake."""
        # TODO: implement MCP handshake and capability negotiation.
        return None

    def fetch_schema(self, resource: str) -> Dict[str, Any]:
        """Retrieve a schema for the given resource from the MCP server."""
        # TODO: implement schema retrieval.
        return {"resource": resource, "schema": "pending"}

    def invoke(self, resource: str, payload: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """
        Placeholder invocation shim. Replace with real MCP calls when wiring an
        actual gateway client or SDK.
        """
        return {
            "resource": resource,
            "payload": payload or {},
            "status": "not-implemented",
            "gateway": f"{self.protocol}://{self.host}:{self.port}",
        }


def _resolve_env(value: Any) -> Any:
    if isinstance(value, str):
        match = ENV_VAR_PATTERN.match(value)
        if match:
            return os.getenv(match.group("env_var"), "")
    return value


def _normalize_name(name: str) -> str:
    return re.sub(r"[^a-zA-Z0-9_]+", "_", name).strip("_").lower()


def load_mcp_connectors(config_path: str) -> List[Dict[str, Any]]:
    """
    Load MCP gateways and tools from YAML. Secrets are resolved from env vars
    when provided as ${ENV_VAR_NAME} placeholders.
    """
    path = Path(config_path)
    if not path.exists():
        return []

    data = yaml.safe_load(path.read_text()) or {}
    connectors: List[Dict[str, Any]] = []
    for raw_gateway in data.get("gateways", []):
        if not raw_gateway.get("name"):
            continue
        connector = MCPGatewayConfig(
            name=raw_gateway["name"],
            host=raw_gateway.get("host", "localhost"),
            port=int(raw_gateway.get("port", 8000)),
            protocol=raw_gateway.get("protocol", "ws"),
            active=bool(raw_gateway.get("active", True)),
            description=raw_gateway.get("description", ""),
            credentials={k: _resolve_env(v) for k, v in (raw_gateway.get("credentials") or {}).items()},
            tools=[
                MCPToolConfig(
                    name=tool.get("name"),
                    resource=tool.get("resource"),
                    description=tool.get("description", ""),
                    active=bool(tool.get("active", True)),
                )
                for tool in raw_gateway.get("tools", [])
                if tool.get("name") and tool.get("resource")
            ],
            metadata=raw_gateway.get("metadata", {}),
        )
        connectors.append(asdict(connector))
    return connectors


def build_mcp_tooling(connectors: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    """
    Convert MCP connector config into tool specs consumable by the LLM tool API.
    Only gateways and tools with `active: true` are exposed to agents.
    """
    tool_specs: List[Dict[str, Any]] = []
    for connector in connectors:
        if not connector.get("active", True):
            continue
        connector_name = _normalize_name(connector.get("name", "mcp"))
        for tool in connector.get("tools", []):
            if not tool.get("active", True):
                continue
            tool_name = _normalize_name(tool.get("name", "tool"))
            resource = tool.get("resource", "")
            description = tool.get("description") or f"MCP resource {resource} via {connector_name} gateway."
            tool_specs.append(
                {
                    "type": "function",
                    "function": {
                        "name": f"mcp__{connector_name}__{tool_name}",
                        "description": description,
                        "parameters": {
                            "type": "object",
                            "properties": {
                                "payload": {
                                    "type": "object",
                                    "description": "Structured payload forwarded to the MCP resource.",
                                },
                                "resource": {
                                    "type": "string",
                                    "description": "Resource identifier (defaults to the configured resource).",
                                    "default": resource,
                                },
                            },
                            "required": [],
                            "additionalProperties": True,
                        },
                    },
                    "metadata": {
                        "mcp_resource": resource,
                        "mcp_gateway": connector_name,
                        "connection": {
                            "host": connector.get("host"),
                            "port": connector.get("port"),
                            "protocol": connector.get("protocol", "ws"),
                        },
                    },
                }
            )
    return tool_specs
