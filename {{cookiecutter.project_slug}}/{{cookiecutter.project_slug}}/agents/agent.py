from typing import List, Callable, Any, Optional

from {{ cookiecutter.project_slug }}.guardrails.policies import GuardrailManager
from {{ cookiecutter.project_slug }}.memory.memory import ChatMemory
from {{ cookiecutter.project_slug }}.telemetry.telemetry import Telemetry


class Agent:
    """
    Lightweight agent capable of running a single task with an LLM, tools,
    and conversation history. This keeps the default generated project simple
    while allowing the multi-agent orchestrator to compose multiple instances.
    """

    def __init__(
        self,
        llm: Any,
        tools: List[dict],
        prompt: str,
        history: List[str],
        output_parser: Callable[[Any], Any],
        memory: Optional[ChatMemory] = None,
        telemetry: Optional[Telemetry] = None,
        use_agents_sdk: bool = False,
        guardrails: Optional[GuardrailManager] = None,
    ) -> None:
        self._llm = llm
        self._tools = tools
        self._prompt = prompt
        self._history = history
        self._memory = memory
        self._telemetry = telemetry
        self._output_parser = output_parser
        self._use_agents_sdk = use_agents_sdk
        self._guardrails = guardrails or GuardrailManager()
        self._validated_tools = self.prepare_tools()

    def prepare_tools(self) -> List[dict]:
        """Prepare and validate tools before executing the query."""
        validated: List[dict] = []
        for tool in self._tools:
            if not tool.get("function"):
                continue
            name = tool["function"].get("name")
            if name:
                self._guardrails.check_tool(name, {})
            validated.append(tool)
        return validated

    def prepare_prompt(self, validated_tools: List[dict], formatted_history: str) -> str:
        """Prepare the final prompt by incorporating validated tools and formatted history."""
        tool_names = [tool["function"]["name"] for tool in validated_tools]
        tools_text = ", ".join(tool_names) if tool_names else "no tools"
        return f"{self._prompt}\nAvailable tools: {tools_text}\nHistory:\n{formatted_history}"

    def query_llm(self, prompt: str, msg: str) -> Any:
        """Send a message to the LLM and return the response."""
        return self._llm.chat(prompt, msg, tools=self._validated_tools)

    def prepare_history(self) -> str:
        """Format the conversation history for the LLM."""
        past_history = "\n".join(self._history)
        memory_history = self._memory.get_history() if self._memory else ""
        combined = "\n".join(segment for segment in [past_history, memory_history] if segment)
        return combined

    def parse_output(self, llm_response: Any) -> Any:
        """Parse the LLM's response into a usable format."""
        if self._output_parser:
            return self._output_parser(llm_response)
        if isinstance(llm_response, dict) and "content" in llm_response:
            return llm_response["content"]
        return llm_response

    def execute(self, user_query: str) -> Any:
        """Run the agent workflow: prepare prompt, query LLM, parse result."""
        sanitized_query = self._guardrails.check_input(user_query)
        if self._telemetry:
            self._telemetry.log_event("agent_input", sanitized_query)
        formatted_history = self.prepare_history()
        final_prompt = self.prepare_prompt(self._validated_tools, formatted_history)
        if self._use_agents_sdk:
            llm_response = self._llm.agent_chat(sanitized_query)
        else:
            llm_response = self.query_llm(final_prompt, sanitized_query)
        parsed = self.parse_output(llm_response)
        # Apply post-guardrails on stringified content.
        if isinstance(parsed, str):
            parsed = self._guardrails.check_output(parsed)
        if self._memory:
            self._memory.save_context(sanitized_query, parsed if isinstance(parsed, str) else str(parsed))
        if self._telemetry:
            self._telemetry.log_event("agent_output", str(parsed))
        return parsed


class RouterManager:
    """
    Simple router that dispatches user queries to specialized agents based on
    provided routing logic. In a real project, this can be expanded with
    semantic routing, capability scoring, or planner/solver roles.
    """

    def __init__(self, agents: List[Agent], default_agent: Optional[Agent] = None):
        self.agents = agents
        self.default_agent = default_agent or (agents[0] if agents else None)

    def route(self, user_query: str) -> Any:
        """Route a query to an agent and execute it."""
        if not self.agents:
            raise ValueError("No agents configured for routing.")
        agent = self.default_agent or self.agents[0]
        return agent.execute(user_query)
