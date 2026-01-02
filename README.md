<img src="https://github.com/user-attachments/assets/d442f52b-4c3d-4d50-99df-1bdf130e018d" alt="SparkGen logo" width="800">

# SparkGen Cookiecutter Template

SparkGen is a Cookiecutter template that scaffolds production-ready GenAI projects with multi-agent orchestration, optional FastAPI surfaces, RAG building blocks, guardrails, MCP connectivity, and telemetry hooks. This README is a start-to-finish guide: follow it to go from nothing to a working project without hunting for additional docs.

> **TIP**: New to Cookiecutter? You only need Python and this README. Everything else is scaffolded for you.

---

## Table of Contents
- [1. Overview](#1-overview)
- [2. Prerequisites](#2-prerequisites)
- [3. Quick Start (zero → running project)](#3-quick-start-zero--running-project)
- [4. Template Options](#4-template-options)
- [5. Project Structure Walkthrough](#5-project-structure-walkthrough)
- [6. Development Workflow](#6-development-workflow)
- [7. Configuration & Environments](#7-configuration--environments)
- [8. CI/CD](#8-cicd)
- [9. Common Tasks](#9-common-tasks)
- [10. Troubleshooting / FAQ](#10-troubleshooting--faq)
- [11. Appendix](#11-appendix)

---

## 1. Overview

**What this template generates**
- Python 3.11+ GenAI project with:
  - CLI entrypoint for agent flows and Spec-as-Code workflows.
  - Optional FastAPI service with `/health` and `/agent/invoke` endpoints.
  - Multi-agent orchestration patterns (single, router-manager, planner-builder) and reusable orchestration helpers (sequential, hierarchical, critic-review, tool-first, broadcast-reduce).
  - RAG scaffolding (embeddings, in-memory vector store, retriever, reranker hook) and Spec-as-Code workflow runtime.
  - Guardrails framework (YAML + Markdown) applied at platform, workflow, and agent levels.
  - MCP connectivity stub with demo tools plus A2A protocol scaffold.
  - Telemetry hooks with optional MLflow and Langfuse wiring.
  - Docker/K8s deployment stubs and basic tests.

**When to use it**
- You want a reproducible, documented starting point for agentic/RAG workloads.
- You need a FastAPI surface plus CLI for experiments.
- You want guardrails, MCP tools, telemetry, and Spec-as-Code workflows already wired.

**When not to use it**
- You need a minimal REST-only microservice without LLMs.
- You cannot run Python 3.11+.
- You need a language/stack other than Python.

**Supported project types (select during prompts)**
- Library/CLI: single-agent mode, no API.
- API Service: FastAPI surface enabled.
- SparkGen workflow project: RAG + agents + guardrails + Spec-as-Code runtime.

---

## 2. Prerequisites

- **Python**: 3.11+ (3.12 recommended). Ensure `python` points to this version.
- **Cookiecutter**: `pip install cookiecutter` or `pipx install cookiecutter`.
- **Poetry** (recommended): `curl -sSL https://install.python-poetry.org | python3 -`.
  - If you prefer `pip`, you can still run `python -m venv .venv && source .venv/bin/activate && pip install -e .` after generation.
- **Git**: for version control.
- **Docker** (optional): to run the generated service in containers.
- **Recommended IDE**: VS Code or PyCharm with these settings:
  - Enable Python extension/plug-in.
  - Auto-format on save (Black or your preferred formatter).
  - YAML schema support for `config/workflow.example.yaml` (schema export command below).

---

## 3. Quick Start (zero → running project)

### 3.1 Generate from the template
```bash
cookiecutter https://github.com/Praveengovianalytics/SparkGen.git
```

### 3.2 Example interactive answers
```
project_name [My GenAI Project]: Demo Agentic App
project_slug [demo_agentic_app]:
author_name [Your Name]: Ada Lovelace
description [A short description of the project.]: Demo of SparkGen workflow
version [0.1.0]:
open_source_license: 1 - BSD-3-Clause
ci_cd_tool: 1 - GitHub Actions
deployment_platform: 0 - Docker
multi_agent_mode: 0 - router-manager
api_framework: 0 - FastAPI
observability: 1 - OpenTelemetry-ready
openai_agent_sdk: 1 - enabled
```

### 3.3 What gets created (high level)
- Project folder named after `project_slug` containing:
  - Python package with agents, tools, orchestration, telemetry, guardrails, and MCP connectors.
  - `api/app.py` (if FastAPI chosen), `config/workflow.example.yaml`, guardrails, prompts, contexts, docs, and tests.
  - Deployment stubs (`ci_cd/`), `.github/workflows/` placeholders, and evaluation helpers.

### 3.4 Run immediately
```bash
cd demo_agentic_app
poetry install

# Run the legacy CLI (single-agent by default or use --pattern)
poetry run python demo_agentic_app/main.py --pattern single-agent --query "Hello!"

# Run Spec-as-Code workflow (preferred)
poetry run python demo_agentic_app/main.py run config/workflow.example.yaml --query "Summarize SparkGen"

# Start FastAPI (if selected)
uvicorn demo_agentic_app.api.app:app --reload
```

---

## 4. Template Options

Every Cookiecutter prompt is listed below. Defaults shown in brackets.

| Prompt | What it controls | Allowed values |
| --- | --- | --- |
| `project_name` | Human-readable project title. | Any string. |
| `project_slug` | Package/directory name (auto-filled from name). | Lowercase/underscored string. |
| `author_name` | Package author metadata. | Any string. |
| `description` | Short project description. | Any string. |
| `version` | Initial package version. | SemVer (default `0.1.0`). |
| `open_source_license` | LICENSE content. | `MIT` (default), `BSD-3-Clause`, `No license file`. |
| `ci_cd_tool` | CI/CD placeholder files. | `GitHub Actions` (default), `GitLab CI/CD`, `Jenkins`, `Bamboo`, `None`. |
| `deployment_platform` | Deployment hints in docs/stubs. | `Docker` (default), `Kubernetes`, `AWS`, `Azure`, `GCP`, `None`. |
| `multi_agent_mode` | Default orchestration mode. | `router-manager` (default), `planner-builder`, `single-agent`. |
| `api_framework` | Whether to scaffold FastAPI. | `FastAPI` (default), `None`. |
| `observability` | Telemetry wiring level. | `Logging only` (default), `OpenTelemetry-ready`. |
| `openai_agent_sdk` | OpenAI Agents SDK toggle. | `disabled` (default), `enabled`. |

> **NOTE**: MCP connectivity, Spec-as-Code workflows, guardrails, telemetry, RAG components, and A2A protocol scaffolds are always included.

### Recipes

1. **Minimal library/CLI**
   - `multi_agent_mode=single-agent`
   - `api_framework=None`
   - `observability=Logging only`
   - `ci_cd_tool=None`, `deployment_platform=None`
   - Run with: `poetry run python <slug>/main.py --pattern single-agent --query "Hello"`

2. **API service (FastAPI)**
   - `api_framework=FastAPI`
   - Any `multi_agent_mode`
   - Start server: `uvicorn <slug>.api.app:app --reload`
   - Smoke test: `curl -X POST http://localhost:8000/agent/invoke -H "Content-Type: application/json" -d '{"query":"ping"}'`

3. **SparkGen workflow project (RAG + Agents + Guardrails)**
   - `multi_agent_mode=router-manager` (default) or `planner-builder`
   - Keep `api_framework` as you prefer
   - Use Spec-as-Code: `poetry run python <slug>/main.py run config/workflow.example.yaml --query "Summarize"`
   - Export schema for IDEs: `poetry run python <slug>/main.py schema --output workflow.schema.json`
   - Scaffold a new workflow: `poetry run python <slug>/main.py init --template rag_agentic --output ./my-workflow`

### Optional toggles at a glance
- **CI/CD**: `.github/workflows/ci.yml` and `cd.yml` stubs are generated (fill in your jobs). Other CI selections act as placeholders you can adapt.
- **Docker/K8s**: `ci_cd/Dockerfile`, `ci_cd/docker-compose.yml`, `ci_cd/deployment/kubernetes.yml` are always scaffolded.
- **Tests**: `tests/` includes starters for agents, MCP, API, and workflow loader.
- **Docs**: `docs/` holds specs and playbooks for orchestration and operations.
- **MCP tools**: configurable via `config/mcp_connectors.yaml` and surfaced to agents.
- **Memory/Vector store**: in-memory defaults with configuration in `workflow.example.yaml`.
- **Knowledge bases**: declare named KBs in `config/knowledge_bases.example.yaml` and mirror them under `rag.knowledge_bases` in workflow YAML so prompts can cite KB tags (e.g., `product_docs`, `responsible_ai`).
- **Channel delivery**: `channel/` clients and `config/channels.example.yaml` make Slack, Teams, Telegram, and WhatsApp webhooks configurable for broadcasting agent replies.

---

## 5. Project Structure Walkthrough

After generation your project looks like this (top-level only):

```
<project_slug>/
├── .github/workflows/          # CI/CD stubs (adjust per selected tool)
├── ci_cd/                      # Docker, Compose, K8s manifests
├── config/                     # Spec-as-Code example + MCP + KB config
├── contexts/                   # Context blocks referenced by workflows
├── channel/                    # Channel connectors (Slack, Teams, Telegram, WhatsApp)
├── docs/                       # Specs (orchestration, operations, testing)
├── guardrails/                 # Default rules + docs
├── prompts/                    # Agent prompt markdown
├── tests/                      # Pytest suites for agents, MCP, API, spec loader
├── {{project_slug}}/           # Python package with runtime code
└── ... (LICENSE, README, pyproject, poetry.lock, Makefile)
```

Key package modules:
- `{{project_slug}}/main.py`: CLI front door (`run`, `init`, `schema`, legacy patterns).
- `{{project_slug}}/api/app.py`: FastAPI app with `/health` and `/agent/invoke` (if API selected).
- `{{project_slug}}/agents/`: Agent implementations plus evaluation agent.
- `{{project_slug}}/orchestration/`: Patterns (`patterns.py`) and Spec-as-Code runtime (`spec_runtime.py`).
- `{{project_slug}}/config/`: Config loader, Spec-as-Code models/loader/templates.
- `{{project_slug}}/guardrails/`: Rule definitions, resolver, guardrail manager.
- `{{project_slug}}/connectors/`: MCP client stub + tool generation.
- `{{project_slug}}/channel/`: Config loader and outbound connectors for Slack/Teams/Telegram/WhatsApp.
- `{{project_slug}}/retrievers`, `embeddings`, `vectordatabase`: RAG building blocks.
- `{{project_slug}}/telemetry/`: Telemetry hooks, MLflow/Langfuse optional wiring.
- `{{project_slug}}/tools/`: Built-in tools plus MCP-derived tool registry.
- `{{project_slug}}/prompt/`: Jinja prompt template helper.

**Inside `{{project_slug}}/` (detailed view)**
```
{{project_slug}}/
├── main.py                   # CLI entrypoint (run/init/schema/legacy patterns)
├── api/
│   └── app.py                # FastAPI app with /health and /agent/invoke (optional)
├── agents/
│   ├── agent.py              # Core Agent + RouterManager implementations
│   └── eval_agent.py         # EvaluationAgent wrapper for RAG evaluator
├── orchestration/
│   ├── patterns.py           # Sequential, router, planner, hierarchical, critic-review, tool-first, broadcast-reduce
│   └── spec_runtime.py       # Builds agents/tools/guardrails from workflow.yaml and runs handoffs
├── config/
│   ├── config_loader.py      # Env/.env loader + MCP tooling assembly
│   ├── spec_loader.py        # YAML loader, env overrides, validation (prompts/tools/handoffs/guardrails)
│   ├── spec_models.py        # Pydantic models + JSON Schema export
│   ├── spec_templates.py     # `init --template` copier (rag_agentic)
│   └── templates/            # Starter workflow.yaml and prompts/contexts for init
├── guardrails/
│   ├── default_guardrails.yaml # Platform sets
│   ├── resolver.py           # Merge/validate guardrail sets and docs
│   ├── policies.py           # GuardrailManager + builders
│   ├── workflow.md           # Workflow-specific rationale (example)
│   └── agents/               # Agent-specific guardrail docs (optional)
├── connectors/
│   └── mcp_client.py         # MCP gateway/tool loader, demo resources, tool spec builder
├── channel/
│   ├── config.py             # Channel config loader and env resolver
│   └── connectors.py         # Slack/Teams/Telegram/WhatsApp webhook clients
├── tools/
│   └── tools.py              # Built-in tools + MCP assembly helper
├── prompt/
│   └── prompt_template.py    # Jinja prompt helper (extend with your own templates)
├── telemetry/
│   └── telemetry.py          # Telemetry hooks (requests + optional MLflow/Langfuse)
├── retrievers/
│   └── retriever.py          # Thin wrapper over vector store
├── embeddings/
│   └── embedder.py           # Deterministic, dependency-light embedder
├── vectordatabase/
│   └── vector_store.py       # In-memory vector store with cosine similarity
├── memory/
│   └── memory.py             # Chat history persistence (TTL/summarization)
├── evaluation/
│   └── evaluator.py          # RAG evaluator used by EvaluationAgent
├── protocols/
│   └── a2a_protocol.py       # Agent-to-agent messaging scaffold
├── reranker/
│   └── reranker.py           # Reranker hook (stub/local)
└── llms/
    └── base_llm.py           # OpenAI chat + Agents SDK scaffold
```

Where to edit:
- **Prompts/contexts**: `prompts/*.md`, `contexts/*.md`, and `config/templates/rag_agentic/prompts|contexts` for new workflow templates.
- **Workflows/specs**: `config/workflow.example.yaml` or new files under `config/templates/` (use `main.py init ...`).
- **Tools/connectors**: `config/mcp_connectors.yaml` for MCP gateways/tools; `tools/tools.py` for built-ins.
- **Guardrails**: `guardrails/default_guardrails.yaml`, `guardrails/workflow.md`, `guardrails/agents/*.md`.
- **Tests**: `tests/` (e.g., `tests/test_agent_flow.py`, `tests/test_api_integration.py`).

---

## 6. Development Workflow

### 6.1 Create a virtual environment and install deps
```bash
cd <project_slug>
poetry install
# or, without Poetry
python -m venv .venv && source .venv/bin/activate
pip install -e .
```

### 6.2 Run unit tests, lint, and format
- Tests: `poetry run pytest`
- Formatting/linting: add your preferred tools (Black/ruff/flake8) and run via `poetry run <tool>`.

### 6.3 Run locally
- **Legacy/quick agent run**: `poetry run python <slug>/main.py --pattern router-manager --query "Plan a release"`
- **Spec-as-Code workflow**: `poetry run python <slug>/main.py run config/workflow.example.yaml --env dev --query "Summarize"`
- **Export workflow schema** (for IDE validation): `poetry run python <slug>/main.py schema --output workflow.schema.json`
- **Bootstrap a new workflow folder**: `poetry run python <slug>/main.py init --template rag_agentic --output ./my-workflow`

### 6.4 Run the FastAPI service (if enabled)
```bash
uvicorn <slug>.api.app:app --reload
curl -X POST http://localhost:8000/agent/invoke -H "Content-Type: application/json" -d '{"query":"hello","pattern":"single-agent"}'
```

### 6.5 Versioning and release
- Bump `version` in `pyproject.toml` (and `README` badges if you add them) before tagging.
- Build with `poetry build` and publish with your chosen registry tooling.

---

## 7. Configuration & Environments

### 7.1 Environment variables and `.env`
Supported environment variables (load from `.env` thanks to `python-dotenv`):
- `LLM_API_KEY` (required for OpenAI calls)
- `LLM_MODEL_NAME` (default `gpt-4o-mini`)
- `MULTI_AGENT_MODE`, `API_FRAMEWORK`, `OBSERVABILITY`
- `OPENAI_AGENT_SDK` (`enabled`/`disabled`), `OPENAI_AGENT_ID`
- Telemetry: `TELEMETRY_ENDPOINT`, `MLFLOW_TRACKING_URI`, `LANGFUSE_HOST`, `LANGFUSE_PUBLIC_KEY`, `LANGFUSE_SECRET_KEY`
- Guardrails: `GUARDRAIL_BANNED_TERMS`, `GUARDRAIL_MAX_OUTPUT_LEN`
- MCP config path override: `MCP_CONFIG_PATH`
- Channel config path override: `CHANNEL_CONFIG_PATH`

Example `.env`:
```
LLM_API_KEY=sk-...
LLM_MODEL_NAME=gpt-4o-mini
MULTI_AGENT_MODE=router-manager
API_FRAMEWORK=FastAPI
OBSERVABILITY=OpenTelemetry-ready
LANGFUSE_HOST=https://cloud.langfuse.com
LANGFUSE_PUBLIC_KEY=...
LANGFUSE_SECRET_KEY=...
CHANNEL_CONFIG_PATH=./config/channels.example.yaml
```

### 7.2 Workflow overrides (dev/staging/prod)
- Use the `environments` map in `config/workflow.example.yaml` (or your workflow) to override values by environment (e.g., increase `rag.top_k` or change `llm.model`).
- Run with `--env staging` to apply the override.

### 7.3 Secrets guidance
- Keep secrets out of git: reference them as `${ENV_VAR}` in `workflow.yaml` and `config/mcp_connectors.yaml`.
- Do not commit `.env`; use vaults/secret managers for shared environments.

### 7.4 Channel configuration and usage
- Define Slack/Teams/Telegram/WhatsApp endpoints in `config/channels.example.yaml` (or your own file) with `${ENV_VAR}` placeholders for sensitive values.
- Override the path via `CHANNEL_CONFIG_PATH` to point at a team-managed secrets location.
- Call `/agent/invoke` with a `channel` value to broadcast agent responses to that destination; delivery metadata is returned alongside the agent result.

---

## 8. CI/CD

- **Included pipelines**: `.github/workflows/ci.yml` and `cd.yml` are stubs—fill them with your jobs. Other CI choices (GitLab/Jenkins/Bamboo) are placeholders you can adapt.
- **Local parity**: run `poetry run pytest` locally; add lint/format commands to match your CI as you extend it.
- **Adding jobs**: edit the workflow YAMLs or create new ones under `.github/workflows/`. Reference `ci_cd/Dockerfile` or `ci_cd/docker-compose.yml` for build steps, and `ci_cd/deployment/kubernetes.yml` for K8s deploy examples.
- **Bamboo template + Azure Event Hub logging**: a Bamboo YAML spec lives at `ci_cd/bamboo/bamboo-spec.yaml`. It installs dependencies, runs tests, and forwards the captured log file to Azure Event Hub using `ci_cd/bamboo/push_eventhub_logs.py`. Configure `AZURE_EVENTHUB_CONNECTION_STRING` and `AZURE_EVENTHUB_NAME` in Bamboo to enable log forwarding.

---

## 9. Common Tasks

- **Add a new module/package**: create a Python file under `<slug>/` (e.g., `<slug>/utils/feature_flags.py`) and import it where needed. Add tests in `tests/`.
- **Add a new API endpoint**: edit `<slug>/api/app.py`, add a FastAPI route, and cover it in `tests/test_api_integration.py`.
- **Add a new workflow YAML**: copy `config/workflow.example.yaml` or run `poetry run python <slug>/main.py init --template rag_agentic --output ./workflows/my_workflow` then edit prompts/contexts.
- **Add a new agent prompt (.md)**: create `prompts/<agent>.md`, update `contexts/*.md` if needed, and register the agent in your workflow under `agents[]` with `prompt_file`/`context_file`.
- **Add guardrails**: edit `guardrails/default_guardrails.yaml` for platform sets; add workflow-level sets under `guardrails` in your `workflow.yaml`; document rationale in `guardrails/README.md` and `guardrails/agents/*.md`.
- **Add a new MCP tool entry**: update `config/mcp_connectors.yaml` (or your custom file) with a gateway/tool, mark `active: true`, and include the generated tool name in `tools.exposed_mcp_tools` and the relevant agent `tools[]` list.
- **Add a new storage backend config**: adjust `storage.vector_store` or `storage.document_store` in your workflow YAML, using `${ENV_VAR}` for credentials. Implement adapters in `vectordatabase/` or `retrievers/` if needed.
- **Add evaluation scripts**: extend `evaluate_api.py` for API-level checks or add new evaluators under `<slug>/evaluation/`, then wrap them in an agent similar to `EvaluationAgent`.

---

## 10. Troubleshooting / FAQ

- **Cookiecutter command not found**: install via `pip install cookiecutter` or `pipx install cookiecutter`, then rerun the command.
- **Python version mismatch**: ensure `python --version` is 3.11+; recreate your virtual environment after switching.
- **`poetry install` errors**: delete `.venv` (if any), ensure Python headers are present, and retry. You can fall back to `pip install -e .`.
- **Tests failing**: run `poetry run pytest -k <testname> -vv` for detail. Check env vars (LLM_API_KEY, MCP_* tokens) and file paths referenced in failures.
- **Generated service won't start**:
  - Confirm dependencies installed (`poetry install`).
  - For FastAPI, ensure `uvicorn` is installed (`poetry install` already includes it when API enabled).
  - Verify `config/workflow.example.yaml` paths exist (prompts/contexts) and env vars are set.
- **Spec validation errors**: the loader checks prompt/context files, guardrail docs, tool names, and circular handoffs. Fix the reported path or reference and rerun.

---

## 11. Examples (copy/paste starters)

### Workflow YAML (Spec-as-Code starter)
```yaml
# config/workflow.example.yaml
version: v1
name: sparkgen-example
entry_agent: researcher
environment: dev

rag:
  enabled: true
  top_k: 4

tools:
  builtin:
    - get_delivery_date
  mcp_connectors:
    - name: demo
      host: localhost
      port: 9999
      protocol: ws
      active: true
      credentials:
        token: ${MCP_DEMO_TOKEN}
      tools:
        - name: demo.calculator
          resource: demo.calculator
  exposed_mcp_tools:
    - mcp__demo__demo_calculator

agents:
  - name: researcher
    role: "Research-first agent that gathers facts with citations."
    prompt_file: ../prompts/researcher.md
    context_file: ../contexts/default.md
    tools:
      - mcp__demo__demo_calculator
    memory:
      short_term: true
      long_term: true
    guardrails:
      use_sets:
        - workflow_rag
      overrides:
        - name: researcher_sensitive_terms
          description: "Block sharing secrets or passwords."
          categories: ["policy", "privacy"]
          applies_to: ["output"]
          mode: block
          severity: high
          priority: 8
          patterns:
            - "(secret|password)"
          message_templates:
            refusal: "I cannot disclose secrets or passwords."
    handoff_notes: "Return 3-5 bullet summary with citations."
  - name: coder
    role: "Implementation agent that produces steps and patches."
    prompt_file: ../prompts/coder.md
    context_file: ../contexts/default.md
    tools:
      - get_delivery_date
    guardrails:
      use_sets:
        - platform_defaults
      overrides: []

handoffs:
  - source: researcher
    target: coder
    trigger: always
    message_contract: "Summary + citations + recommended next actions."
```

### Prompt markdown (agent persona)
```markdown
<!-- prompts/researcher.md -->
You are **Researcher**, a fact-first agent.
- Cite sources when possible.
- Prefer concise bullet lists (3-5 bullets).
- If unsure, state the uncertainty and propose how to verify.
```

```markdown
<!-- prompts/coder.md -->
You are **Coder**, focused on actionable implementation steps.
- Return short, numbered steps.
- Include code snippets when helpful.
- Ask for missing inputs before proceeding if requirements are unclear.
```

### Guardrails (defaults + workflow)
```yaml
# guardrails/default_guardrails.yaml
allowed_categories:
  - policy
  - privacy
  - citations
  - constraints
apply_sets:
  - platform_defaults
sets:
  - name: platform_defaults
    description: "Baseline platform guardrails."
    rules:
      - name: pii_redaction
        categories: ["privacy"]
        applies_to: ["output"]
        mode: redact
        severity: critical
        priority: 5
        patterns:
          - "(?i)(ssn|social security|credit card)"
```

```yaml
# guardrails/workflow.md (referenced in workflow YAML)
# Document workflow-specific rationale and examples here.
```

> **Tip**: Keep prompts and guardrails in the same folders referenced by your workflow YAML so validation succeeds, and use `${ENV_VAR}` placeholders for any secrets in YAML.

**Glossary**
- **Cookiecutter**: tool that asks prompts and generates a project folder from this template.
- **Poetry**: dependency and packaging manager used by the generated project.
- **pre-commit**: git hook manager (not preconfigured—add if you need automated formatting/checks).
- **MCP (Model Context Protocol)**: standard for exposing tools/resources to LLMs; configured via `config/mcp_connectors.yaml`.
- **RAG (Retrieval-Augmented Generation)**: pattern combining retrieval (embeddings/vector store) with generation.
- **Guardrails**: safety/policy rules enforced on inputs/outputs/tool calls, defined in YAML/Markdown.
- **A2A protocol**: agent-to-agent messaging scaffold in `protocols/a2a_protocol.py`.

## 11. Appendix

**Glossary**
- **Cookiecutter**: tool that asks prompts and generates a project folder from this template.
- **Poetry**: dependency and packaging manager used by the generated project.
- **pre-commit**: git hook manager (not preconfigured—add if you need automated formatting/checks).
- **MCP (Model Context Protocol)**: standard for exposing tools/resources to LLMs; configured via `config/mcp_connectors.yaml`.
- **RAG (Retrieval-Augmented Generation)**: pattern combining retrieval (embeddings/vector store) with generation.
- **Guardrails**: safety/policy rules enforced on inputs/outputs/tool calls, defined in YAML/Markdown.
- **A2A protocol**: agent-to-agent messaging scaffold in `protocols/a2a_protocol.py`.

> **You’re set.** Run the quick start commands, customize `workflow.example.yaml`, and start shipping agentic features.
