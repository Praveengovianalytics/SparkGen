# SparkGen Guardrails

This directory centralizes platform-wide guardrails plus workflow- and
agent-specific overrides. Guardrails are defined in YAML and documented in
Markdown so policy intent and enforcement stay auditable.

## How guardrails are organized
- `default_guardrails.yaml`: Platform defaults and reusable guardrail sets.
- `workflow.md`: Optional workflow-specific rationale and examples.
- `agents/*.md`: Optional agent-level guidance and overrides.

Guardrails attach at three layers:
1. **Platform defaults** (`default_guardrails.yaml`): baseline sets reused across
   workflows.
2. **Workflow guardrails** (`workflow.yaml`): extend/override defaults and point
   to workflow-specific docs.
3. **Agent guardrails** (`workflow.yaml` + `agents/*.md`): per-agent set
   selection plus overrides and rationale.

## How to update default guardrails
1. Edit `default_guardrails.yaml` to add or tweak reusable sets. Keep
   `allowed_categories` aligned with the categories used in your rules.
2. Document changes in this `README.md` (what changed and why).
3. Add or update test cases inside the YAML to capture expected outcomes.
4. Run `sparksgen run workflow.yaml` (or your CI) to validate the config.

## How to add workflow guardrails
1. In `workflow.yaml`, set `guardrails.defaults_path` to the defaults file and
   reference this README via `documentation`.
2. Add workflow-specific sets under `guardrails.sets[]` and include a
   `workflow_doc` (e.g., `../guardrails/workflow.md`).
3. List the sets to apply globally via `guardrails.apply_sets`.
4. Keep rules grounded in reusable categories and include `message_templates`
   plus `tests` for clarity.

## How to override guardrails per agent
1. For each agent, choose which sets to use via `guardrails.use_sets`.
2. Add targeted `overrides` to tighten or loosen enforcement for that agent.
3. Document intent in `guardrails.doc` (e.g., `../guardrails/agents/<agent>.md`).
4. Prefer `block` for safety-critical cases, `redact` for PII, and `warn` for
   style/citation hints.

## Common pitfalls
- Forgetting to include Markdown docs for referenced guardrail sets or agents
  (loader will fail fast).
- Using categories not listed in `allowed_categories` (validation will fail).
- Omitting `apply_sets`, which can unintentionally disable defaults.
- Leaving `patterns` empty on a `block` rule that should only trigger on
  specific text.

## Merge order (deterministic)
1. Platform defaults load first.
2. Workflow sets override defaults when they share a rule name.
3. Agent overrides trump workflow/default rules.

Ties resolve by `(priority asc, severity critical→low, layer agent→workflow→default)`.
