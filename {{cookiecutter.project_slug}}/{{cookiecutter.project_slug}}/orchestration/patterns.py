"""
Common agentic orchestration patterns, provided as lightweight scaffolds that
developers can extend. Each pattern exposes a `run` method to illustrate where
coordination logic should be added.
"""

from typing import Any, List

from {{ cookiecutter.project_slug }}.agents.agent import Agent, RouterManager
from {{ cookiecutter.project_slug }}.protocols.a2a_protocol import AgentToAgentProtocol


class SequentialExecutor:
    """Run agents one after another, passing outputs as inputs."""

    def __init__(self, agents: List[Agent]):
        self.agents = agents

    def run(self, user_query: str) -> Any:
        payload = user_query
        for agent in self.agents:
            payload = agent.execute(payload)
        return payload


class RouterManagerPattern:
    """Route to a single specialist agent via RouterManager."""

    def __init__(self, router: RouterManager):
        self.router = router

    def run(self, user_query: str) -> Any:
        return self.router.route(user_query)


class PlannerExecutorPattern:
    """Simple planner that selects an agent and then executes."""

    def __init__(self, protocol: AgentToAgentProtocol, agents: List[Agent]):
        self.protocol = protocol
        self.agents = agents
        for idx, agent in enumerate(agents):
            self.protocol.register_agent(f"planner_agent_{idx}", ["generic"])

    def run(self, user_query: str) -> Any:
        # Naive plan: pick first agent; extend with skill lookup or graph planning.
        target = next(iter(self.protocol.registry.keys()))
        result = self.agents[0].execute(user_query)
        self.protocol.send_message("planner", target, f"completed:{user_query}")
        return result


class HierarchicalManager:
    """Top-level manager assigns work to child agents and aggregates results."""

    def __init__(self, manager: Agent, workers: List[Agent]):
        self.manager = manager
        self.workers = workers

    def run(self, user_query: str) -> Any:
        plan = self.manager.execute(f"Plan tasks for: {user_query}")
        outputs = [worker.execute(user_query) for worker in self.workers]
        return {"plan": plan, "results": outputs}


class BroadcastReduce:
    """Broadcast a query to many agents, then reduce their answers."""

    def __init__(self, agents: List[Agent], reducer):
        self.agents = agents
        self.reducer = reducer

    def run(self, user_query: str) -> Any:
        responses = [agent.execute(user_query) for agent in self.agents]
        return self.reducer(responses)


class CriticReview:
    """Draft-answer + critic pattern to improve quality."""

    def __init__(self, drafter: Agent, critic: Agent):
        self.drafter = drafter
        self.critic = critic

    def run(self, user_query: str) -> Any:
        draft = self.drafter.execute(user_query)
        critique = self.critic.execute(f"Review this answer: {draft}")
        return {"draft": draft, "critique": critique}


class ToolCallFirst:
    """Tool selection first, then LLM summarization."""

    def __init__(self, tool_agent: Agent, summarizer: Agent):
        self.tool_agent = tool_agent
        self.summarizer = summarizer

    def run(self, user_query: str) -> Any:
        tool_output = self.tool_agent.execute(user_query)
        return self.summarizer.execute(f"Summarize tool results: {tool_output}")
