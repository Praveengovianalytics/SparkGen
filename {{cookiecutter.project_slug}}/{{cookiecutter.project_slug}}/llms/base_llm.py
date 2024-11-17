from openai import OpenAI

class BaseLLM:
    """
    A base class to interface with OpenAI's language models. 
    It handles model configuration, input prediction, and token utilization.

    Attributes:
        llm (OpenAI): An instance of OpenAI initialized with the model configuration.
    """

    def __init__(self, model_config: dict) -> None:
        """
        Initializes the BaseLLM instance with the provided model configuration.

        Args:
            model_config (dict): A dictionary containing model configuration parameters such as API key, model ID, etc.
        """
        # Initialize the OpenAI instance with the provided configuration
        self.llm = OpenAI(**model_config)
    
    def predict(self, prompt: str, callback: object):
        """
        Sends a prompt to the language model and returns the generated output. 
        Optionally handles token usage and allows for future expansion (like input/output capture).

        Args:
            prompt (str): The input prompt for the language model to generate a response.
            callback (object): Placeholder for a callback function to process the model's response, if needed.

        Returns:
            output (str): The generated output from the language model.
        """
        # Start input capture (future expansion for logging input, etc.)
        # Send the prompt to the LLM and get the output
        output = self.llm(prompt)
    
        # Token utilization capture (future expansion for tracking token usage)
        # End output capture (future expansion for logging output, etc.)
        # Return the generated response from the model
        return output