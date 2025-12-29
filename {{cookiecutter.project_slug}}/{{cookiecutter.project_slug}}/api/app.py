"""
FastAPI scaffold to expose agents via REST/webhooks.

This keeps the runtime minimal: build an agent (or orchestration pattern) from
existing template primitives, then invoke it via a POST endpoint. Extend the
builder functions to wire your own tools, storage, or routing logic.
"""

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Optional

from {{ cookiecutter.project_slug }}.agents.agent import Agent, RouterManager
from {{ cookiecutter.project_slug }}.config.config_loader import ConfigLoader
from {{ cookiecutter.project_slug }}.guardrails.policies import build_default_guardrails
from {{ cookiecutter.project_slug }}.llms.base_llm import BaseLLM
from {{ cookiecutter.project_slug }}.orchestration import patterns
from {{ cookiecutter.project_slug }}.prompt.prompt_template import PromptTemplate
from {{ cookiecutter.project_slug }}.protocols.a2a_protocol import AgentToAgentProtocol
from {{ cookiecutter.project_slug }}.tools.tools import assemble_tools

app = FastAPI(title="{{ cookiecutter.project_name }} Agent API")


class InvokeRequest(BaseModel):
    query: str
    pattern: str = "single-agent"
    channel: Optional[str] = None


def build_single_agent(config):
    guardrails = build_default_guardrails(config)
    llm = BaseLLM(
        {
            "api_key": config["api_key"],
            "model": config["model_name"],
            "use_agents": config.get("openai_agent_sdk") == "enabled",
            "agent_id": config.get("openai_agent_id"),
        }
    )
    prompt = PromptTemplate()
    toolset = assemble_tools(config)
    return Agent(
        llm=llm,
        tools=toolset,
        prompt=prompt.PROMPT_TEMPLATE,
        history=[],
        output_parser=None,
        use_agents_sdk=config.get("openai_agent_sdk") == "enabled",
        guardrails=guardrails,
    )


def build_router_pattern(config):
    guardrails = build_default_guardrails(config)
    llm, prompt = BaseLLM(
        {
            "api_key": config["api_key"],
            "model": config["model_name"],
            "use_agents": config.get("openai_agent_sdk") == "enabled",
            "agent_id": config.get("openai_agent_id"),
        }
    ), PromptTemplate()
    toolset = assemble_tools(config)
    research_agent = Agent(
        llm=llm,
        tools=toolset,
        prompt=f"Research agent: {prompt.PROMPT_TEMPLATE}",
        history=["You are a research specialist."],
        output_parser=None,
        use_agents_sdk=config.get("openai_agent_sdk") == "enabled",
        guardrails=guardrails,
    )
    coding_agent = Agent(
        llm=llm,
        tools=toolset,
        prompt=f"Coding agent: {prompt.PROMPT_TEMPLATE}",
        history=["You write code and return patches."],
        output_parser=None,
        use_agents_sdk=config.get("openai_agent_sdk") == "enabled",
        guardrails=guardrails,
    )
    router = RouterManager(agents=[research_agent, coding_agent])
    return patterns.RouterManagerPattern(router=router)


def build_pattern(pattern_name: str, config):
    single_agent = build_single_agent(config)
    if pattern_name == "single-agent":
        return single_agent
    if pattern_name == "router-manager":
        return build_router_pattern(config)
    if pattern_name == "sequential":
        return patterns.SequentialExecutor([single_agent, single_agent])
    if pattern_name == "planner-executor":
        proto = AgentToAgentProtocol()
        return patterns.PlannerExecutorPattern(protocol=proto, agents=[single_agent])
    if pattern_name == "hierarchical":
        return patterns.HierarchicalManager(manager=single_agent, workers=[single_agent])
    if pattern_name == "broadcast-reduce":
        return patterns.BroadcastReduce(agents=[single_agent, single_agent], reducer=lambda res: res[0])
    if pattern_name == "critic-review":
        return patterns.CriticReview(drafter=single_agent, critic=single_agent)
    if pattern_name == "tool-first":
        return patterns.ToolCallFirst(tool_agent=single_agent, summarizer=single_agent)
    raise HTTPException(status_code=400, detail=f"Unknown pattern: {pattern_name}")


@app.get("/health")
def health():
    return {"status": "ok"}


@app.post("/agent/invoke")
def invoke(req: InvokeRequest):
    config = ConfigLoader().load_config()
    channels = config.get("channel_clients", {})
    pattern = build_pattern(req.pattern, config)
    if isinstance(pattern, Agent):
        result = pattern.execute(req.query)
    else:
        result = pattern.run(req.query)  # type: ignore[attr-defined]
    delivery = None
    if req.channel:
        client = channels.get(req.channel)
        if not client:
            raise HTTPException(status_code=400, detail=f"Unknown channel: {req.channel}")
        delivery = client.send_message(str(result))
        if not delivery.get("ok"):
            raise HTTPException(status_code=502, detail=f"Channel delivery failed: {delivery}")
    return {"pattern": req.pattern, "result": result, "channel_delivery": delivery}
