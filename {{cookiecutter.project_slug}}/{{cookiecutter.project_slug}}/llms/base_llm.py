from typing import Any, Dict, List, Optional

from openai import OpenAI


class BaseLLM:
    """
    A base class to interface with OpenAI's chat and Agents SDK while keeping the
    surface area minimal for template users.
    """

    def __init__(self, model_config: Dict[str, Any]) -> None:
        """
        Initializes the BaseLLM instance with the provided model configuration.

        Args:
            model_config (dict): A dictionary containing model configuration parameters such as API key, model ID, etc.
        """
        self.client = OpenAI(api_key=model_config.get("api_key"))
        self.model = model_config.get("model", "gpt-4o-mini")
        self.use_agents = model_config.get("use_agents", False)
        self.agent_id = model_config.get("agent_id")

    def chat(self, prompt: str, message: str, tools: Optional[List[dict]] = None) -> Dict[str, Any]:
        """
        Basic chat helper for single-agent or router-managed flows.
        """
        completion = self.client.chat.completions.create(  # type: ignore[attr-defined]
            model=self.model,
            messages=[{"role": "system", "content": prompt}, {"role": "user", "content": message}],
            tools=tools or None,
        )
        message_content = (
            completion.choices[0].message.content if completion and completion.choices else ""
        )
        return {"raw": completion, "content": message_content}

    def agent_chat(self, user_input: str, attachments: Optional[List[Any]] = None) -> Dict[str, Any]:
        """
        Scaffold to call the OpenAI Agents SDK. Requires an `agent_id` to be
        pre-provisioned; template users can wire provisioning in CI/CD later.
        """
        if not self.use_agents or not self.agent_id:
            raise ValueError("Agents SDK not enabled or agent_id missing.")

        # Placeholder call; real implementation would stream responses and tool calls.
        response = self.client.agents.responses.create(  # type: ignore[attr-defined]
            model=self.model,
            agent_id=self.agent_id,
            input=[{"role": "user", "content": user_input}],
            attachments=attachments or [],
        )
        content = ""
        if getattr(response, "output", None):
            output_items = getattr(response.output, "output", [])  # type: ignore[attr-defined]
            if output_items:
                content = output_items[0].get("content", "")
        return {"raw": response, "content": content}

    def ensure_agent(self, name: str = "default-agent") -> Optional[str]:
        """
        Helper to provision an agent id if one is not provided.
        """
        if self.agent_id:
            return self.agent_id
        try:
            created = self.client.agents.create(  # type: ignore[attr-defined]
                model=self.model,
                name=name,
            )
            self.agent_id = getattr(created, "id", None)
        except Exception:
            # Leave agent_id as None; caller can fallback to chat mode.
            self.agent_id = None
        return self.agent_id
