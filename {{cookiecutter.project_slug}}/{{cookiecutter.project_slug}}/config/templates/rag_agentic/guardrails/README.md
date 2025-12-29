# SparkGen Guardrails (template)

This starter guardrail bundle provides platform defaults plus workflow and
agent-level hooks for customization.

- `default_guardrails.yaml`: Platform defaults; reuse across workflows.
- `workflow.md`: Describe workflow-specific rationale and examples.
- `agents/*.md`: Capture agent-specific overrides and reasoning.

Follow these steps after generating a project:
1. Update `guardrails/default_guardrails.yaml` to match your policies and add
   tests for new rules.
2. In `workflow.yaml`, set `guardrails.apply_sets` and add any workflow-level
   sets. Point `documentation` and `workflow_doc` at the Markdown files.
3. For each agent, pick `use_sets` and add `overrides`; document intent in
   `guardrails/agents/<agent>.md`.
4. Run `sparksgen run workflow.yaml` to validate the merged guardrails.
