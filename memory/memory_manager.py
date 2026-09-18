import json
from pathlib import Path

MEMORY_PATH = Path(__file__).resolve().parent / "user_preferences.json"

class MemoryManager:
    def __init__(self):
        self.session_messages = []
        self.persistent = {}
        if MEMORY_PATH.exists():
            try:
                self.persistent = json.loads(MEMORY_PATH.read_text(encoding="utf-8"))
            except (json.JSONDecodeError, OSError):
                self.persistent = {}

    def add_message(self, role: str, content: str):
        self.session_messages.append({"role": role, "content": content})

    def get_session_messages(self):
        return list(self.session_messages)

    def save_preference(self, preference: str):
        self.persistent["learning_preference"] = preference.strip()
        MEMORY_PATH.write_text(json.dumps(self.persistent, indent=2), encoding="utf-8")

    def get_preference(self):
        return self.persistent.get("learning_preference")
