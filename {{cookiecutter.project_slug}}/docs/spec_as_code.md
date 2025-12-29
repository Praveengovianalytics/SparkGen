# Spec-as-Code Upgrade Guide (SparkGen)

1. **Project layout**
```
{{cookiecutter.project_slug}}/
├── config/
│   ├── workflow.example.yaml        # End-to-end Spec-as-Code example
│   ├── spec_models.py               # Pydantic schema definitions (v1)
│   ├── spec_loader.py               # YAML loader, env override merge, validation
│   ├── spec_templates.py            # `sparksgen init --template ...` helper
│   └── templates/rag_agentic/       # Starter workflow + prompts/contexts
├── guardrails/
│   ├── default_guardrails.yaml      # Platform default guardrail sets
│   ├── README.md                    # Guardrail rationale + how-to guides
│   ├── workflow.md                  # Example workflow-specific guardrails
│   └── agents/*.md                  # Optional agent-specific rationales
├── orchestration/spec_runtime.py    # Wiring layer to build agents/tools/router
├── prompts/*.md                     # Agent prompts (referenced by YAML)
├── contexts/*.md                    # Workflow context blocks (referenced by YAML)
└── main.py                          # `sparksgen run <yaml>`, `init`, `schema`, legacy runner
```

2. **YAML schema (human-readable, v1)**
- `version`: always `v1`.
- `name`, `description`: identifiers for the workflow.
- `entry_agent`: name of the first agent to run.
- `environment`: selected environment key (`dev/staging/prod`).
- `rag`: `enabled`, `retriever (in_memory|stub)`, `top_k`, `embedding_model`, `chunking.size|overlap|strategy`, `reranker.enabled|provider|top_n`, `citations`, `collection`.
- `storage`: `vector_store.backend|collection|credentials`, `document_store.backend|path|credentials`, `memory_store_path`.
- `memory`: `short_term.store|ttl_messages|null|summarization_policy`, `long_term.store|ttl_messages|null|summarization_policy`.
- `tools`: `builtin` tool names, `mcp_connectors[]` (`name`, `host`, `port`, `protocol`, `active`, `credentials ${ENV}`, `tools[]` with `name`, `resource`, `description`, `active`, `rate_limit_per_minute`), `exposed_mcp_tools` to allowlist MCP tools by name.
- `guardrails`: `defaults_path`, `documentation`, `workflow_doc`, `apply_sets[]`, `allowed_categories[]`, `sets[]` (each with `name`, optional `description|docs`, and `rules[]` of `name`, `description`, `categories[]`, `applies_to[] (input|output|tool)`, `mode (block|warn|redact|allow)`, `severity`, `priority`, `patterns[]`, `tags[]`, `policy_references[]`, `message_templates.refusal|escalation`, `tests[prompt, expected_outcome]`).
- `agents[]`: `name`, `role`, `prompt_file`, optional `context_file`, `tools[]` (must exist in registry), `memory.short_term|long_term`, `guardrails.use_sets|overrides|doc`, `handoff_notes`.
- `handoffs[]`: `source`, `target`, `trigger (always|on_success)`, `message_contract`.
- `observability`: `logging (basic|verbose)`, `tracing`, `metrics`, `run_id_env`, `telemetry_endpoint`, `mlflow_tracking_uri`, `langfuse_host`, `langfuse_public_key_env`, `langfuse_secret_key_env`.
- `llm`: `provider`, `model`, `api_key_env`, `use_agents_sdk`, `agent_id_env`.
- `environments`: map of environment keys to partial overrides for `rag`, `storage`, `memory`, `tools`, `observability`, or `llm`.

3. **Example `workflow.yaml`**
- Full example lives at `config/workflow.example.yaml` (mirrors the template under `config/templates/rag_agentic/workflow.yaml`). It wires RAG chunking/reranker, MCP calculator, two agents, handoff rules, memory policies, storage backends, environment overrides, and observability.

4. **Example `.md` prompt/context files**
- Agent prompts: `prompts/researcher.md`, `prompts/coder.md`.
- Workflow context: `contexts/default.md`.
- Template variants: `config/templates/rag_agentic/prompts/*.md`, `config/templates/rag_agentic/contexts/product_context.md`.
- YAML references these relative paths (e.g., `prompt_file: ../prompts/researcher.md`).

5. **Python code files**
- `config/spec_models.py`: Pydantic schema + JSON Schema export helper.
- `config/spec_loader.py`: YAML loader, env override merge, missing-file guard, tool validation, circular handoff detection, secret placeholder enforcement.
- `config/spec_templates.py`: `init_template()` copy helper for `sparksgen init --template rag_agentic`.
- `orchestration/spec_runtime.py`: builds Telemetry, LLM, guardrails, memory, tools (MCP + built-ins), agents, and handoffs; exposes `load_workflow(...).run(query)`.
- `main.py`: CLI front-door with `run`, `init`, `schema`, and legacy patterns.

6. **Docs (practical playbooks)**
- Add a new Agent:
  1) Create `prompts/<agent>.md` (and optional `contexts/*.md` block).
  2) Append an entry to `agents[]` in `workflow.yaml` with `name`, `role`, `prompt_file`, `context_file`, tool list, and guardrails (`use_sets`, `overrides`, `doc`).
  3) Reference the agent in `entry_agent` or `handoffs` as needed; rerun `sparksgen run workflow.yaml`.
- Add guardrails:
  1) Update `guardrails/default_guardrails.yaml` with platform sets, categories, message templates, and tests; document rationale in `guardrails/README.md`.
  2) In `workflow.yaml`, set `guardrails.defaults_path`, `documentation`, `workflow_doc`, and `apply_sets`; add workflow-level sets under `guardrails.sets[]`.
  3) For each agent, select `guardrails.use_sets`, add `overrides` as needed, and document them under `guardrails/agents/*.md`.
- Add a new MCP Tool:
  1) Add a connector or tool under `tools.mcp_connectors[]` with `${ENV}` credentials.
  2) Include the generated tool name (e.g., `mcp__demo_gateway__demo_calculator`) in `tools.exposed_mcp_tools` and in an agent’s `tools[]`.
  3) Ensure the env vars exist; loader will fail fast otherwise.
- Create a new Workflow from the template:
  1) Run `sparksgen init --template rag_agentic --output ./my-workflow`.
  2) Edit `workflow.yaml`, plus `prompts/*.md` and `contexts/*.md`.
  3) Execute with `sparksgen run workflow.yaml --query "..." --env staging`.
