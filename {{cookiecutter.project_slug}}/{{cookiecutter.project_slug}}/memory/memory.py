import json
from pathlib import Path
from typing import Dict, List, Optional


class ChatMemory:
    """
    A simple class to track and store chat history between a human and AI.
    Backed by a JSON file so conversations persist across runs.
    """

    def __init__(self, storage_path: Optional[str] = None):
        """
        Initializes the memory store and loads any existing history from disk.

        Args:
            storage_path (str, optional): Location to persist chat history.
                Defaults to ".sparkgen_memory.json" in the working directory.
        """
        self.storage_path = Path(storage_path or ".sparkgen_memory.json")
        self.history: List[Dict[str, str]] = []
        self._load()

    def _load(self) -> None:
        """
        Load persisted history if available.
        """
        if self.storage_path.exists():
            try:
                self.history = json.loads(self.storage_path.read_text())
            except (json.JSONDecodeError, OSError):
                self.history = []

    def _persist(self) -> None:
        """
        Persist the in-memory history to disk.
        """
        try:
            self.storage_path.write_text(json.dumps(self.history, indent=2))
        except OSError:
            # If persistence fails, keep history in memory.
            pass

    def save_context(self, human_msg: str, ai_msg: str) -> None:
        """
        Saves the human and AI messages to the conversation context.

        Args:
            human_msg (str): The message from the human user.
            ai_msg (str): The response from the AI.
        """
        self.history.append({"human": human_msg, "ai": ai_msg})
        self._persist()

    def get_history(self) -> str:
        """
        Retrieves the stored conversation history.

        Returns:
            str: The conversation history in "Human/AI" format.
        """
        formatted = []
        for entry in self.history:
            formatted.append(f"Human: {entry.get('human', '')}")
            formatted.append(f"AI: {entry.get('ai', '')}")
        return "\n".join(formatted)

    def clear(self) -> None:
        """
        Clears the conversation history both in memory and on disk.
        """
        self.history = []
        if self.storage_path.exists():
            try:
                self.storage_path.unlink()
            except OSError:
                pass
