class ChatMemory:
    def __init__(self):
        self.context = []

    def save_context(self, human_msg: str, ai_msg: str):
        self.context.append(f"Human: {human_msg}")
        self.context.append(f"AI: {ai_msg}")

    def get_history(self):
        return "\n".join(self.context)