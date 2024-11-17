from jinja2 import Environment, BaseLoader

"""(prompt.jinja2) File
- Greet the user with their nickname, which is {{ user_nickname }}.

{% if user_is_in_a_hurry == "True" %}
- The user is in a hurry, so give quick, action-oriented responses.
{% else %}
- The user is relaxed, so feel free to engage in a more conversational and friendly tone.
{% endif %}

"""

class PromptTemplate:
    """
    A generic base agent class template that provides core functionality
    for rendering prompts, validating responses.
    """
    
    PROMPT = open("prompt.jinja2").read().strip()

    def __init__(self):
        pass
        
    def render(self, prompt_data: dict) -> str:
        """Renders the prompt using Jinja2 with the given data."""
        env = Environment(loader=BaseLoader())
        template = env.from_string(self.PROMPT)
        return template.render(**prompt_data)