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
  Model Context Protocol resources and schemas.
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
