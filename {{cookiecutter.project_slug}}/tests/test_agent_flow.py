from {{ cookiecutter.project_slug }}.agents.agent import Agent, RouterManager


class DummyLLM:
    def __init__(self):
        self.calls = []

    def chat(self, prompt, message, tools=None):
        self.calls.append({"prompt": prompt, "message": message})
        return {"content": f"Echo: {message}"}


def test_router_executes_first_agent():
    llm = DummyLLM()
    agent = Agent(
        llm=llm,
        tools=[],
        prompt="system",
        history=[],
        output_parser=lambda resp: resp["content"],
    )
    router = RouterManager([agent])
    result = router.route("hello")
    assert result == "Echo: hello"
    assert len(llm.calls) == 1
