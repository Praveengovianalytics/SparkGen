class ChatMemory:
    """
    A simple class to track and store chat history between a human and AI.
    """

    def __init__(self):
        """
        Initializes an empty context to store the conversation history.
        """
        self.context = ""

    def save_context(self, human_msg: str, ai_msg: str):
        """
        Saves the human and AI messages to the conversation context.

        Args:
            human_msg (str): The message from the human user.
            ai_msg (str): The response from the AI.
        """
        self.context += f"Human: {human_msg} \nAI: {ai_msg}\n"
        
    def get_history(self):
        """
        Retrieves the stored conversation history.

        Returns:
            str: The conversation history in "Human/AI" format.
        """
        return self.context