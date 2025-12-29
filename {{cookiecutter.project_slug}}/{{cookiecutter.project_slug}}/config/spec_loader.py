"""
Loader and validator for Spec-as-Code workflow files.
"""

from __future__ import annotations

import copy
import json
from pathlib import Path
from typing import Any, Dict, List, Optional

import yaml

from {{ cookiecutter.project_slug }}.config.errors import SpecValidationError
from {{ cookiecutter.project_slug }}.connectors.mcp_client import _normalize_name
from {{ cookiecutter.project_slug }}.config.spec_models import (
    WorkflowOverrides,
    WorkflowSpec,
)
from {{ cookiecutter.project_slug }}.guardrails.resolver import GuardrailResolver


def _deep_merge(base: Dict[str, Any], overrides: Dict[str, Any]) -> Dict[str, Any]:
    """Recursively merge dictionaries."""
    merged = copy.deepcopy(base)
    for key, value in overrides.items():
        if isinstance(value, dict) and isinstance(merged.get(key), dict):
            merged[key] = _deep_merge(merged[key], value)
        else:
            merged[key] = copy.deepcopy(value)
    return merged


class WorkflowSpecLoader:
    """
    Load, validate, and resolve a workflow.yaml file into a typed spec.
    """

    def __init__(self, spec_path: str, environment: Optional[str] = None):
        self.spec_path = Path(spec_path)
        self.environment = environment
        self.base_dir = self.spec_path.parent

    def load(self) -> WorkflowSpec:
        raw = yaml.safe_load(self.spec_path.read_text())
        if not isinstance(raw, dict):
            raise SpecValidationError("workflow.yaml must parse into a mapping.")

        selected_env = self.environment or raw.get("environment") or "dev"
        overrides_payload = (raw.get("environments") or {}).get(selected_env, {})
        if overrides_payload:
            overrides_payload = WorkflowOverrides.model_validate(overrides_payload).model_dump(exclude_none=True)
        merged_payload = _deep_merge({k: v for k, v in raw.items() if k != "environments"}, overrides_payload)
        merged_payload["environment"] = selected_env
        merged_payload["environments"] = {
            key: WorkflowOverrides.model_validate(value).model_dump(exclude_none=True)
            for key, value in (raw.get("environments") or {}).items()
        }
        spec = WorkflowSpec.model_validate(merged_payload)
        self._validate_prompts_and_context(spec)
        self._validate_tool_references(spec)
        self._validate_handoffs(spec)
        self._validate_guardrails(spec)
        return spec

    def _validate_prompts_and_context(self, spec: WorkflowSpec) -> None:
        missing: List[str] = []
        for agent in spec.agents:
            prompt_path = (self.base_dir / agent.prompt_file).resolve()
            if not prompt_path.exists():
                missing.append(agent.prompt_file)
            if agent.context_file:
                context_path = (self.base_dir / agent.context_file).resolve()
                if not context_path.exists():
                    missing.append(agent.context_file)
        if missing:
            raise SpecValidationError(f"Prompt/context files missing: {', '.join(sorted(set(missing)))}")

    def _validate_tool_references(self, spec: WorkflowSpec) -> None:
        registry_names = set(spec.tools.builtin)
        for connector in spec.tools.mcp_connectors:
            normalized_connector = _normalize_name(connector.name)
            for tool in connector.tools:
                if tool.active:
                    registry_names.add(tool.name)
                    registry_names.add(f"mcp__{normalized_connector}__{_normalize_name(tool.name)}")
        for agent in spec.agents:
            unknown = [tool for tool in agent.tools if tool not in registry_names]
            if unknown:
                raise SpecValidationError(
                    f"Agent '{agent.name}' references unknown tools: {', '.join(unknown)}"
                )

    def _validate_handoffs(self, spec: WorkflowSpec) -> None:
        agent_names = {agent.name for agent in spec.agents}
        adjacency: Dict[str, List[str]] = {}
        for handoff in spec.handoffs:
            if handoff.source not in agent_names or handoff.target not in agent_names:
                raise SpecValidationError(
                    f"Handoff references unknown agents: {handoff.source} -> {handoff.target}"
                )
            adjacency.setdefault(handoff.source, []).append(handoff.target)
        visited: Dict[str, bool] = {}
        rec_stack: Dict[str, bool] = {}

        def _cycle(node: str) -> bool:
            visited[node] = True
            rec_stack[node] = True
            for neighbor in adjacency.get(node, []):
                if not visited.get(neighbor, False) and _cycle(neighbor):
                    return True
                if rec_stack.get(neighbor, False):
                    return True
            rec_stack[node] = False
            return False

        for node in adjacency:
            if not visited.get(node, False) and _cycle(node):
                raise SpecValidationError("Circular agent handoff detected in workflow.")

    def _validate_guardrails(self, spec: WorkflowSpec) -> None:
        resolver = GuardrailResolver(self.base_dir)
        defaults_cfg, default_set_names = resolver.load_defaults(spec.guardrails.defaults_path)
        merged_cfg, default_set_names = resolver.merge_configs(defaults_cfg, spec.guardrails)
        resolver.validate_docs(merged_cfg, [agent.guardrails for agent in spec.agents])
        for agent_cfg in spec.agents:
            resolver.resolve_agent_rules(merged_cfg, default_set_names, agent_cfg.guardrails)

    def export_schema(self) -> Dict[str, Any]:
        """
        Return the JSON Schema for WorkflowSpec to make IDE consumption easy.
        """
        return WorkflowSpec.model_json_schema()

    @staticmethod
    def write_schema(path: Path) -> None:
        schema = WorkflowSpec.model_json_schema()
        path.write_text(json.dumps(schema, indent=2))
