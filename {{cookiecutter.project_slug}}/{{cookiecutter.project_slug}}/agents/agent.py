from typing import List, Callable, Any, Optional
from {{ cookiecutter.project_slug }}.guardrails.policies import GuardrailManager, GuardrailViolation


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
        use_agents_sdk: bool = False,
        guardrails: Optional[GuardrailManager] = None,
    ) -> None:
        self._llm = llm
        self._tools = tools
        self._prompt = prompt
        self._history = history
        self._output_parser = output_parser
        self._use_agents_sdk = use_agents_sdk
        self._guardrails = guardrails or GuardrailManager()
        self._validated_tools = self.prepare_tools()
        self._formatted_history = self.prepare_history()
        self._final_prompt = self.prepare_prompt(self._validated_tools)

    def prepare_tools(self) -> List[dict]:
        """Prepare and validate tools before executing the query."""
        return [tool for tool in self._tools if tool.get("function")]

    def prepare_prompt(self, validated_tools: List[dict]) -> str:
        """Prepare the final prompt by incorporating validated tools and formatted history."""
        tool_names = [tool["function"]["name"] for tool in validated_tools]
        tools_text = ", ".join(tool_names) if tool_names else "no tools"
        return f"{self._prompt}\nAvailable tools: {tools_text}\nHistory:\n{self._formatted_history}"

    def query_llm(self, prompt: str, msg: str) -> Any:
        """Send a message to the LLM and return the response."""
        return self._llm.chat(prompt, msg, tools=self._validated_tools)

    def prepare_history(self) -> str:
        """Format the conversation history for the LLM."""
        return "\n".join(self._history)

    def parse_output(self, llm_response: Any) -> Any:
        """Parse the LLM's response into a usable format."""
        if self._output_parser:
            return self._output_parser(llm_response)
        if isinstance(llm_response, dict) and "content" in llm_response:
            return llm_response["content"]
        return llm_response

    def execute(self, user_query: str) -> Any:
        """Run the agent workflow: prepare prompt, query LLM, parse result."""
        self._guardrails.run_pre(user_query)
        if self._use_agents_sdk:
            llm_response = self._llm.agent_chat(user_query)
        else:
            llm_response = self.query_llm(self._final_prompt, user_query)
        parsed = self.parse_output(llm_response)
        # Apply post-guardrails on stringified content.
        if isinstance(parsed, str):
            self._guardrails.run_post(parsed)
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
        # Placeholder: naive selection of the first agent. Replace with semantic routing.
        agent = self.agents[0]
        return agent.execute(user_query)
