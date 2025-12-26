from {{ cookiecutter.project_slug }}.protocols.a2a_protocol import AgentToAgentProtocol


def test_register_and_send_message():
    proto = AgentToAgentProtocol()
    proto.register_agent("agent_a", ["search"])
    proto.register_agent("agent_b", ["code"])

    result = proto.send_message("agent_a", "agent_b", "Hello")
    assert result["delivered"] is True
    assert result["to"] == "agent_b"
    assert proto.list_skills("agent_b") == ["code"]
