"""
Helpers to load, merge, and validate guardrail definitions across default,
workflow, and agent scopes.
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Dict, List, Optional, Set, Tuple

import yaml

from {{ cookiecutter.project_slug }}.config.errors import SpecValidationError
from {{ cookiecutter.project_slug }}.config.spec_models import (
    AgentGuardrailConfig,
    GuardrailConfig,
    GuardrailRule,
    GuardrailSet,
)


class GuardrailResolver:
    def __init__(self, base_dir: Path):
        self.base_dir = base_dir

    def load_defaults(self, defaults_path: str) -> Tuple[GuardrailConfig, Set[str]]:
        path = (self.base_dir / defaults_path).resolve()
        if not path.exists():
            raise SpecValidationError(f"Guardrail defaults file not found: {defaults_path}")
        payload = yaml.safe_load(path.read_text()) or {}
        config = GuardrailConfig.model_validate(payload)
        default_set_names = {guardrail_set.name for guardrail_set in config.sets}
        return config, default_set_names

    def merge_configs(
        self, defaults: GuardrailConfig, workflow_cfg: GuardrailConfig
    ) -> Tuple[GuardrailConfig, Set[str]]:
        default_set_names = {guardrail_set.name for guardrail_set in defaults.sets}
        merged_sets: Dict[str, GuardrailSet] = {s.name: s for s in defaults.sets}
        for candidate in workflow_cfg.sets:
            merged_sets[candidate.name] = candidate
        allowed_categories: List[str] = list(
            dict.fromkeys((defaults.allowed_categories or []) + (workflow_cfg.allowed_categories or []))
        )
        apply_sets = workflow_cfg.apply_sets or defaults.apply_sets
        merged = GuardrailConfig(
            defaults_path=workflow_cfg.defaults_path or defaults.defaults_path,
            documentation=workflow_cfg.documentation or defaults.documentation,
            workflow_doc=workflow_cfg.workflow_doc or defaults.workflow_doc,
            apply_sets=apply_sets,
            allowed_categories=allowed_categories,
            sets=list(merged_sets.values()),
        )
        return merged, default_set_names

    def resolve_agent_rules(
        self,
        merged: GuardrailConfig,
        default_set_names: Set[str],
        agent_cfg: AgentGuardrailConfig,
    ) -> List[GuardrailRule]:
        set_index = {s.name: s for s in merged.sets}
        unknown_sets = [name for name in agent_cfg.use_sets if name not in set_index]
        unknown_global = [name for name in merged.apply_sets if name not in set_index]
        if unknown_sets or unknown_global:
            missing = unknown_global + unknown_sets
            raise SpecValidationError(
                f"Guardrail set(s) referenced but not defined: {', '.join(sorted(set(missing)))}"
            )

        def severity_rank(severity: str) -> int:
            order = {"critical": 0, "high": 1, "medium": 2, "low": 3}
            return order.get(severity, 3)

        def preferred(current: Tuple[GuardrailRule, str], candidate: Tuple[GuardrailRule, str]) -> bool:
            current_rule, current_layer = current
            candidate_rule, candidate_layer = candidate
            if candidate_rule.priority != current_rule.priority:
                return candidate_rule.priority < current_rule.priority
            if severity_rank(candidate_rule.severity) != severity_rank(current_rule.severity):
                return severity_rank(candidate_rule.severity) < severity_rank(current_rule.severity)
            layer_rank = {"agent": 0, "workflow": 1, "default": 2}
            return layer_rank.get(candidate_layer, 3) < layer_rank.get(current_layer, 3)

        resolved: Dict[str, Tuple[GuardrailRule, str]] = {}

        def add_rules(rules: List[GuardrailRule], layer: str):
            for rule in rules:
                existing = resolved.get(rule.name)
                candidate = (rule, layer)
                if not existing or preferred(existing, candidate):
                    resolved[rule.name] = candidate

        for set_name in merged.apply_sets:
            layer = "default" if set_name in default_set_names else "workflow"
            add_rules(set_index[set_name].rules, layer)

        for set_name in agent_cfg.use_sets:
            layer = "default" if set_name in default_set_names else "workflow"
            add_rules(set_index[set_name].rules, layer)

        add_rules(agent_cfg.overrides, "agent")

        allowed_categories = set(merged.allowed_categories or [])
        if not allowed_categories:
            raise SpecValidationError("Guardrail config must declare allowed_categories to validate rule categories.")
        for rule, _ in resolved.values():
            unknown = set(rule.categories) - allowed_categories
            if unknown:
                raise SpecValidationError(
                    f"Guardrail rule '{rule.name}' uses invalid categories: {', '.join(sorted(unknown))}"
                )

        sorted_rules = sorted(
            [rule for rule, _ in resolved.values()],
            key=lambda r: (r.priority, severity_rank(r.severity)),
        )
        return sorted_rules

    def validate_docs(
        self, merged: GuardrailConfig, agents: List[AgentGuardrailConfig]
    ) -> None:
        doc_paths: List[Optional[str]] = [merged.documentation, merged.workflow_doc]
        doc_paths.extend(set_cfg.docs for set_cfg in merged.sets)
        doc_paths.extend(agent.doc for agent in agents)
        missing: List[str] = []
        for path in doc_paths:
            if not path:
                continue
            candidate = (self.base_dir / path).resolve()
            if not candidate.exists():
                missing.append(path)
        if missing:
            raise SpecValidationError(
                f"Guardrail documentation file(s) missing: {', '.join(sorted(set(missing)))}"
            )

    @staticmethod
    def serialize_rules_for_debug(rules: List[GuardrailRule]) -> str:
        return json.dumps([rule.model_dump() for rule in rules], indent=2)
