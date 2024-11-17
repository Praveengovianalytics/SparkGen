from jinja2 import Environment, BaseLoader

class PromptTemplate:
    PROMPT_TEMPLATE = """
    - Greet the user with their nickname, which is XXXXX.
    """

    def __init__(self):
        pass

    def render(self, prompt_data: dict) -> str:
        env = Environment(loader=BaseLoader())
        template = env.from_string(self.PROMPT_TEMPLATE)
        return template.render(**prompt_data)
