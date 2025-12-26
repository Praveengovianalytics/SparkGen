# Agentic Orchestration Patterns (Template Cheatsheet)

This template includes stubs for common coordination patterns. Each pattern is
implemented in `{{cookiecutter.project_slug}}/orchestration/patterns.py` and is
intended to be customized.

## Patterns Included
1) **Sequential Executor** — chain agents, pass outputs as inputs.
2) **Router Manager** — route a query to a single specialist.
3) **Planner + Executor** — lightweight planner selects an agent (extend with graphs).
4) **Hierarchical Manager** — manager agent delegates to workers and aggregates.
5) **Broadcast + Reduce** — fan-out to many agents, then reduce (e.g., vote/score).
6) **Critic Review** — drafter produces, critic reviews.
7) **Tool-Call First** — tool-focused agent runs first, summarizer wraps up.

## How to Use
- Pick a pattern and initialize it with agents wired to your prompts/tools.
- Extend the `run` method with your routing, scoring, or planning logic.
- Combine with MCP skills or A2A protocol to share context/skills across agents.
- Trace execution via telemetry (MLflow/Langfuse) to compare patterns side by side.
