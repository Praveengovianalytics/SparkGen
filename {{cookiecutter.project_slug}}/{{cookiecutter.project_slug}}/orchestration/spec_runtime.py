"""
Runtime wiring for Spec-as-Code workflows.
"""

from __future__ import annotations

import os
from pathlib import Path
from typing import Dict, List, Tuple

from {{ cookiecutter.project_slug }}.agents.agent import Agent, RouterManager
from {{ cookiecutter.project_slug }}.config.spec_loader import WorkflowSpecLoader
from {{ cookiecutter.project_slug }}.config.spec_models import WorkflowSpec
from {{ cookiecutter.project_slug }}.guardrails.policies import GuardrailManager
from {{ cookiecutter.project_slug }}.guardrails.resolver import GuardrailResolver
from {{ cookiecutter.project_slug }}.llms.base_llm import BaseLLM
from {{ cookiecutter.project_slug }}.memory.memory import ChatMemory
from {{ cookiecutter.project_slug }}.retrievers.retriever import Retriever
from {{ cookiecutter.project_slug }}.telemetry.telemetry import Telemetry
from {{ cookiecutter.project_slug }}.tools.tools import assemble_tools, tools as builtin_tools


class SpecRuntime:
    """
    Build agents, router, and supporting components from a workflow spec.
    """

    def __init__(self, spec: WorkflowSpec, base_dir: Path):
        self.spec = spec
        self.base_dir = base_dir
        self.telemetry = self._build_telemetry()
        self.retriever = Retriever(top_k=self.spec.rag.top_k)
        self._index_contexts()

    @classmethod
    def from_file(cls, path: str, environment: str | None = None) -> "SpecRuntime":
        loader = WorkflowSpecLoader(path, environment=environment)
        spec = loader.load()
        return cls(spec=spec, base_dir=Path(path).parent)

    def run(self, query: str) -> Dict[str, str]:
        agents, router = self._build_agents()
        active_agent_name = self.spec.entry_agent
        active_agent = agents[active_agent_name]
        query_with_context = self._apply_rag(query)
        result = active_agent.execute(query_with_context)
        visited = {active_agent_name}
        for handoff in self.spec.handoffs:
            if handoff.source != active_agent_name or handoff.trigger not in {"always", "on_success"}:
                continue
            if handoff.target in visited:
                continue
            downstream = agents.get(handoff.target)
            if downstream:
                result = downstream.execute(str(result))
                active_agent_name = handoff.target
                visited.add(active_agent_name)
        return {"agent": active_agent_name, "result": result}

    def _build_agents(self) -> Tuple[Dict[str, Agent], RouterManager]:
        tools_registry = self._build_tools()
        guardrail_resolver = GuardrailResolver(self.base_dir)
        defaults_cfg, default_set_names = guardrail_resolver.load_defaults(self.spec.guardrails.defaults_path)
        merged_guardrails, default_set_names = guardrail_resolver.merge_configs(defaults_cfg, self.spec.guardrails)
        guardrail_resolver.validate_docs(merged_guardrails, [agent.guardrails for agent in self.spec.agents])
        agents: Dict[str, Agent] = {}
        for agent_spec in self.spec.agents:
            memory_window = self.spec.memory.short_term if agent_spec.memory.short_term else self.spec.memory.long_term
            memory = ChatMemory(
                storage_path=self.spec.storage.memory_store_path,
                ttl_messages=memory_window.ttl_messages,
                summarization_policy=memory_window.summarization_policy,
            )
            resolved_rules = guardrail_resolver.resolve_agent_rules(merged_guardrails, default_set_names, agent_spec.guardrails)
            guardrails = GuardrailManager(rules=resolved_rules)
            prompt_content = (self.base_dir / agent_spec.prompt_file).read_text()
            if agent_spec.context_file:
                context_content = (self.base_dir / agent_spec.context_file).read_text()
                prompt_content = f"{context_content}\n\n{prompt_content}"
            llm = BaseLLM(
                {
                    "api_key": os.getenv(self.spec.llm.api_key_env, ""),
                    "model": self.spec.llm.model,
                    "use_agents": self.spec.llm.use_agents_sdk,
                    "agent_id": os.getenv(self.spec.llm.agent_id_env, "") if self.spec.llm.agent_id_env else None,
                }
            )
            bound_tools = [tools_registry[name] for name in agent_spec.tools if name in tools_registry]
            agent = Agent(
                llm=llm,
                tools=bound_tools,
                prompt=f"{agent_spec.role}: {prompt_content}",
                history=[],
                output_parser=lambda resp: resp,
                memory=memory,
                telemetry=self.telemetry,
                use_agents_sdk=self.spec.llm.use_agents_sdk,
                guardrails=guardrails,
            )
            agents[agent_spec.name] = agent
        default_agent = agents.get(self.spec.entry_agent)
        router = RouterManager(agents=list(agents.values()), default_agent=default_agent)
        return agents, router

    def _build_telemetry(self) -> Telemetry:
        obs = self.spec.observability
        return Telemetry(
            telemetry_endpoint=obs.telemetry_endpoint or "https://telemetry.example.com/events",
            mlflow_tracking_uri=obs.mlflow_tracking_uri,
            langfuse_config={
                "host": obs.langfuse_host,
                "public_key": os.getenv(obs.langfuse_public_key_env, "") if obs.langfuse_public_key_env else None,
                "secret_key": os.getenv(obs.langfuse_secret_key_env, "") if obs.langfuse_secret_key_env else None,
            },
        )

    def _build_tools(self) -> Dict[str, dict]:
        config = {
            "mcp_connectors": [connector.model_dump() for connector in self.spec.tools.mcp_connectors],
            "mcp_tools": None,
        }
        assembled = assemble_tools(config)
        registry: Dict[str, dict] = {}
        builtin_map = {tool["function"]["name"]: tool for tool in builtin_tools}
        allowed_builtin = set(self.spec.tools.builtin)
        for name in allowed_builtin:
            if name in builtin_map:
                registry[name] = builtin_map[name]
        for tool in assembled:
            name = tool.get("function", {}).get("name")
            if not name:
                continue
            if self.spec.tools.exposed_mcp_tools and name not in self.spec.tools.exposed_mcp_tools:
                continue
            registry[name] = tool
        return registry

    def _index_contexts(self) -> None:
        if not self.spec.rag.enabled:
            return
        docs: List[str] = []
        metadata: List[Dict[str, str]] = []
        for agent in self.spec.agents:
            if not agent.context_file:
                continue
            context_path = (self.base_dir / agent.context_file).resolve()
            if not context_path.exists():
                continue
            text = context_path.read_text()
            for chunk in self._chunk_text(text, self.spec.rag.chunking.size, self.spec.rag.chunking.overlap):
                docs.append(chunk)
                metadata.append({"agent": agent.name, "source": str(agent.context_file)})
        if docs:
            self.retriever.add_texts(docs, metadatas=metadata)

    @staticmethod
    def _chunk_text(text: str, size: int, overlap: int) -> List[str]:
        if size <= 0:
            return [text]
        chunks: List[str] = []
        start = 0
        while start < len(text):
            end = min(len(text), start + size)
            chunks.append(text[start:end])
            start = end - overlap if overlap < size else end
        return chunks

    def _apply_rag(self, query: str) -> str:
        if not self.spec.rag.enabled:
            return query
        results = self.retriever.retrieve(query)
        if not results:
            return query
        formatted = "\n".join(
            f"- ({hit.get('score', 0):.2f}) {hit.get('text','')}" for hit in results
        )
        return f"{query}\n\nContext:\n{formatted}"


def load_workflow(spec_path: str, environment: str | None = None) -> SpecRuntime:
    """
    Convenience helper for CLI entrypoints.
    """
    return SpecRuntime.from_file(spec_path, environment=environment)
