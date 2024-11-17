from jinja2 import Environment, BaseLoader

class PromptTemplate:
    PROMPT_TEMPLATE = """
    - Greet the user with their nickname, which is {{ user_nickname }}.

    {% if user_is_in_a_hurry %}
    - The user is in a hurry, so give quick, action-oriented responses.
    {% else %}
    - The user is relaxed, so feel free to engage in a more conversational and friendly tone.
    {% endif %}

    - Answer the query: {{ query }}
    """

    def __init__(self):
        pass

    def render(self, prompt_data: dict) -> str:
        env = Environment(loader=BaseLoader())
        template = env.from_string(self.PROMPT_TEMPLATE)
        return template.render(**prompt_data)
