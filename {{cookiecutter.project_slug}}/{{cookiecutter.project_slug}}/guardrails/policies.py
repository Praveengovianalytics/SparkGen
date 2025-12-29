"""
Centralized guardrail scaffolding.

Defines pre-, post-, and tool-call guardrails composed from YAML/Markdown
definitions. Guardrails are layered (defaults -> workflow -> agent) and merged
deterministically before being evaluated at runtime.
"""

from __future__ import annotations

import json
import re
from pathlib import Path
from typing import Dict, Iterable, List, Optional

from {{ cookiecutter.project_slug }}.config.spec_models import AgentGuardrailConfig, GuardrailRule
from {{ cookiecutter.project_slug }}.guardrails.resolver import GuardrailResolver


class GuardrailViolation(Exception):
    """Raised when a guardrail is violated."""


def _compile_patterns(patterns: Iterable[str]) -> List[re.Pattern[str]]:
    compiled: List[re.Pattern[str]] = []
    for pat in patterns:
        try:
            compiled.append(re.compile(pat, flags=re.IGNORECASE))
        except re.error as exc:  # pragma: no cover - validated by loader
            raise ValueError(f"Invalid regex in guardrail pattern '{pat}': {exc}") from exc
    return compiled


def _severity_rank(severity: str) -> int:
    order = {"critical": 0, "high": 1, "medium": 2, "low": 3}
    return order.get(severity, 3)


class GuardrailManager:
    """
    Execute guardrail rules deterministically across input, output, and tool-call stages.
    """

    def __init__(self, rules: Optional[List[GuardrailRule]] = None):
        self.rules = sorted(rules or [], key=lambda r: (r.priority, _severity_rank(r.severity), r.name))
        self._compiled = {rule.name: _compile_patterns(rule.patterns) for rule in self.rules}
        self.warnings: List[str] = []

    def _apply(self, text: str, stage: str, tool_name: Optional[str] = None, params: Optional[Dict] = None) -> str:
        sanitized = text
        for rule in self.rules:
            if stage not in rule.applies_to:
                continue

            haystack = (
                sanitized
                if stage != "tool"
                else json.dumps({"tool": tool_name, "params": params or {}}, sort_keys=True)
            )
            matchers = self._compiled.get(rule.name, [])
            triggered = any(matcher.search(haystack) for matcher in matchers) if matchers else True
            if not triggered:
                continue

            if rule.mode == "redact" and stage != "tool":
                for matcher in matchers:
                    sanitized = matcher.sub("[REDACTED]", sanitized)
                continue

            if rule.mode == "block":
                message = rule.message_templates.refusal or f"Guardrail '{rule.name}' blocked {stage}."
                raise GuardrailViolation(message)
            if rule.mode == "warn":
                note = rule.message_templates.escalation or f"Guardrail '{rule.name}' warning on {stage}."
                self.warnings.append(note)
            # allow/no-op handled implicitly
        return sanitized

    def check_input(self, user_input: str) -> str:
        return self._apply(user_input, stage="input")

    def check_output(self, output: str) -> str:
        return self._apply(output, stage="output")

    def check_tool(self, tool_name: str, params: Optional[Dict] = None) -> None:
        self._apply("", stage="tool", tool_name=tool_name, params=params)


def build_default_guardrails(config: Optional[Dict] = None) -> GuardrailManager:
    """
    Build guardrails using the YAML/Markdown-driven system for legacy entrypoints.
    """

    cfg = config or {}
    base_dir = Path(cfg.get("base_dir", Path.cwd()))
    defaults_path = cfg.get("guardrails_path", "guardrails/default_guardrails.yaml")
    workflow_guardrails = cfg.get("workflow_guardrails")
    agent_guardrails = cfg.get("agent_guardrails")

    resolver = GuardrailResolver(base_dir)
    defaults_cfg, default_set_names = resolver.load_defaults(defaults_path)
    merged, default_set_names = resolver.merge_configs(defaults_cfg, workflow_guardrails or defaults_cfg)
    agent_cfg = agent_guardrails or AgentGuardrailConfig(use_sets=merged.apply_sets)
    resolver.validate_docs(merged, [agent_cfg])
    rules = resolver.resolve_agent_rules(merged, default_set_names, agent_cfg)
    return GuardrailManager(rules=rules)
