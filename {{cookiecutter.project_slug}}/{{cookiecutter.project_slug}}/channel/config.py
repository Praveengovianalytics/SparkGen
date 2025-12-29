"""Channel configuration loader and helpers.

This module keeps channel wiring declarative so the FastAPI surface can push
agent responses to collaboration platforms without hard-coding credentials.
Configurations live in `config/channels.example.yaml` by default and can be
overridden via the `CHANNEL_CONFIG_PATH` environment variable.
"""

from dataclasses import dataclass, field, asdict
import os
import re
from pathlib import Path
from typing import Any, Dict, List

import yaml


ENV_VAR_PATTERN = re.compile(r"^\${(?P<env_var>[A-Z0-9_]+)}$")


@dataclass
class ChannelConfig:
    """Declarative configuration for a single outbound channel."""

    name: str
    type: str
    active: bool = True
    description: str = ""
    settings: Dict[str, Any] = field(default_factory=dict)


def _resolve_env(value: Any) -> Any:
    if isinstance(value, str):
        match = ENV_VAR_PATTERN.match(value)
        if match:
            return os.getenv(match.group("env_var"), "")
    return value


def load_channel_configs(config_path: str) -> List[Dict[str, Any]]:
    """Load channel definitions from YAML and resolve env placeholders."""

    path = Path(config_path)
    if not path.exists():
        return []

    data = yaml.safe_load(path.read_text()) or {}
    connectors: List[Dict[str, Any]] = []
    for raw in data.get("channels", []):
        if not raw.get("name") or not raw.get("type"):
            continue
        cfg = ChannelConfig(
            name=raw["name"],
            type=raw["type"],
            active=bool(raw.get("active", True)),
            description=raw.get("description", ""),
            settings={k: _resolve_env(v) for k, v in (raw.get("settings") or {}).items()},
        )
        connectors.append(asdict(cfg))
    return connectors
