# {{ cookiecutter.project_name }}

{{ cookiecutter.description }}

## 🧠 Why Multi-Agent?

This template now ships with a **multi-agent-ready** architecture inspired by
community templates like [neural-maze/agent-api-cookiecutter](https://github.com/neural-maze/agent-api-cookiecutter).
You can choose between:

- **Router Manager**: Dispatches queries to specialized agents.
- **Planner Builder**: Scaffold for building planner/solver style task graphs.
- **Single Agent**: Minimal flow for quick prototypes.

Configure these options when running Cookiecutter or later via environment
variables such as `MULTI_AGENT_MODE`, `API_FRAMEWORK`, and `OBSERVABILITY`.

Observability hooks for **MLflow** and **Langfuse** are scaffolded in the telemetry
layer. Set `MLFLOW_TRACKING_URI`, `LANGFUSE_HOST`, `LANGFUSE_PUBLIC_KEY`, and
`LANGFUSE_SECRET_KEY` to enable them in generated projects. Enable the
OpenAI Agents SDK by setting `OPENAI_AGENT_SDK=enabled` (and providing
`OPENAI_AGENT_ID` when you have provisioned one).

### 🛰️ Connectivity & Protocols
- **MCP Connectivity**: `connectors/mcp_client.py` contains a stub to negotiate
  Model Context Protocol resources and schemas. Configure gateways and tools in
  `config/mcp_connectors.yaml` (or override with `MCP_CONFIG_PATH`). Tools and
  gateways marked `active: true` are exposed to agents; credentials are pulled
  from environment variables referenced as `${ENV_VAR_NAME}`.
- **A2A Protocol**: `protocols/a2a_protocol.py` offers an agent-to-agent message
  scaffold for sharing skills and context across agents.
- **Orchestration Patterns**: `orchestration/patterns.py` includes 7 scaffolds
  (sequential, router, planner-executor, hierarchical, broadcast-reduce,
  critic-review, tool-first) with a cheatsheet in `docs/orchestration_patterns.md`.
- **FastAPI Surface**: `api/app.py` exposes `/health` and `/agent/invoke` to call
  agents or patterns. Run with:
  ```bash
  uvicorn {{cookiecutter.project_slug}}.api.app:app --reload
  ```

## 🧭 Usage Steps
1. Generate your project with Cookiecutter.
2. Install dependencies:
   ```bash
   poetry install
   ```
3. Run CLI entrypoint (single-agent by default):
   ```bash
   poetry run python {{cookiecutter.project_slug}}/main.py
   ```
4. Run FastAPI service (if selected):
   ```bash
   uvicorn {{cookiecutter.project_slug}}.api.app:app --reload
   ```
5. Call the API:
   ```bash
   curl -X POST http://localhost:8000/agent/invoke -H "Content-Type: application/json" -d '{"query":"hello","pattern":"single-agent"}'
   ```
6. Switch orchestration patterns by setting `pattern` to one of:
   `single-agent`, `router-manager`, `sequential`, `planner-executor`,
   `hierarchical`, `broadcast-reduce`, `critic-review`, `tool-first`.

## 🔌 Configuring MCP gateways & tools
1. Declare gateways and tools in `config/mcp_connectors.yaml`. Use `${ENV_VAR}`
   placeholders for credentials so secrets stay out of version control.
2. Mark a gateway or tool `active: true` to expose it to agents; inactive items
   stay hidden but documented in the file.
3. Override the config location with `MCP_CONFIG_PATH` to point at an ops-managed
   secret store or environment-specific file.
4. Agents automatically merge these MCP tools with built-in tools so the LLM can
   select them during planning and execution.

## 🗂️ Project Structure (key files)
```
{{cookiecutter.project_slug}}/
├── api/
│   └── app.py               # FastAPI surface
├── agents/                  # agent definitions
├── prompt/                  # prompt templates
├── llms/                    # LLM wrappers
├── tools/                   # tool specs/functions
├── memory/                  # memory abstractions
├── telemetry/               # telemetry hooks
├── orchestration/
│   └── patterns.py          # orchestration scaffolds
├── guardrails/
│   └── policies.py          # guardrail manager and policies
├── protocols/
│   └── a2a_protocol.py      # agent-to-agent messaging
├── connectors/
│   └── mcp_client.py        # MCP connectivity stub
├── config/
│   ├── config_loader.py     # environment + YAML configuration loader
│   └── mcp_connectors.yaml  # MCP gateway and tool registry (toggle active flags)
├── docs/
│   ├── context_engineering_spec.md
│   └── orchestration_patterns.md
├── tests/                   # unit tests for agents/protocols
└── main.py                  # CLI entrypoint (single/router/planner)
```

See `docs/context_engineering_spec.md` for a spec-driven checklist that keeps
prompts, skills, and routing consistent.

## 🚀 Getting Started

Instructions on how to get a copy of the project running on your local machine.

## 📚 Documentation

Detailed documentation is available in the `docs/` directory.

## 🛠️ Installation

### Create a virtual environment

```bash

Step 1 - 
python -m venv venv

Step 2 - 
cd venv/Scripts&&Activate  ( Windows )
source venv/bin/activate ( Mac / Linux )

Step 3 -
pip install poetry

step 4 -
poetry init

Give the project name as same project slug

step 5 -

poetry add library_1 library_2 library_3
