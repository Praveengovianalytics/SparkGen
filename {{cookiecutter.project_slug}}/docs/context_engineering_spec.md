# Context Engineering & Skill Management (Spec-Driven Outline)

This specification provides a lightweight checklist for designing prompts,
skills, and agent collaboration patterns generated from this template.

## Goals
- Establish consistent **spec-driven development** for prompts and skills.
- Encourage modular **skills** that map to tools, MCP resources, or A2A
  interactions.
- Make it easy to swap between single-agent and multi-agent configurations.
- Declare knowledge bases by name so prompts can reference them explicitly.

## Core Specs
1. **Context Model**
   - Define the canonical entities (user, session, task, skill).
   - Capture context in `memory/` and surface it in prompts using
     `prompt/prompt_template.py`.

2. **Skill Registry**
   - Document skills each agent owns (align with `protocols/a2a_protocol.py`).
   - For MCP-driven skills, outline the resource names and schema contracts, and
     reflect them in `config/mcp_connectors.yaml` with `active` flags.
   - The template includes demo MCP skills (`demo.calculator`, `demo.datetime`,
     `demo.local_terminal`) to accelerate local testing—swap or disable them for
     production.
3. **Knowledge Bases**
   - Maintain a KB registry (e.g., `config/knowledge_bases.example.yaml`) with `name`, `collection`, `description`, and `contexts[]`.
   - Reference KB names in prompts (e.g., `product_docs`, `responsible_ai`) so retrieval context is explicit.
   - Keep contexts short and chunk-friendly; cite KB names in responses.

4. **Prompt Contracts**
   - Keep prompts declarative; store defaults in `prompt_template.py`.
   - Include tool exposure lists and guidance for tool selection.

5. **Observability & Traces**
   - Ensure telemetry spans tool use, A2A hops, and MCP lookups.
   - Configure MLflow/Langfuse keys via environment variables for reproducible runs.

6. **Testing Matrix**
   - Unit: agent routing (`tests/test_agent_flow.py`), A2A messaging,
     and MCP schema fetch stubs.
   - Integration: simulated end-to-end flow with router-manager and planner-builder.

## Extension Hooks
- **MCP Connectivity**: expand `connectors/mcp_client.py` with capability
  negotiation and schema caching.
- **A2A Protocol**: enrich `protocols/a2a_protocol.py` with signing/auth and
  transport adapters (HTTP, gRPC, WebSockets).
- **Agent Skills**: map skills to tools or MCP resources and expose them in the
  prompt templates for planner/routing decisions.

## Usage Guidance
1. Start from this spec and fill in the details per project.
2. Align agents’ skills with prompt instructions and router/planner logic.
3. Capture every new capability (tool, MCP resource, A2A channel) in this spec
   before coding to keep the system coherent.
