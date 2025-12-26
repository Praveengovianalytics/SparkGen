"""Agent-to-Agent (A2A) protocol scaffold.

This module outlines how agents can exchange messages, register skills, and
share context. It is intentionally lightweight so teams can extend it with
signing, auth, or richer message envelopes.
"""

from typing import Any, Dict, List


class AgentToAgentProtocol:
    """Simple in-memory A2A protocol."""

    def __init__(self):
        self.registry: Dict[str, Dict[str, Any]] = {}

    def register_agent(self, agent_id: str, skills: List[str]) -> None:
        """Register an agent and its skills."""
        self.registry[agent_id] = {"skills": skills}

    def send_message(self, sender: str, recipient: str, content: str) -> Dict[str, Any]:
        """Placeholder message passing. Extend with transport/security."""
        if recipient not in self.registry:
            raise ValueError(f"Recipient {recipient} not registered.")
        return {"from": sender, "to": recipient, "content": content, "delivered": True}

    def list_skills(self, agent_id: str) -> List[str]:
        """List skills for a registered agent."""
        return self.registry.get(agent_id, {}).get("skills", [])
