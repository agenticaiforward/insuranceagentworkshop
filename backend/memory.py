class MemoryStore:
    """Simple in‑memory store for Gemini chat sessions.
    This allows the agent to retain conversation history across multiple calls.
    """

    def __init__(self):
        self._sessions = {}

    def get(self, session_id: str):
        """Return the chat object for *session_id* or ``None`` if not present."""
        return self._sessions.get(session_id)

    def set(self, session_id: str, chat):
        """Store *chat* under *session_id*.
        Overwrites any existing entry.
        """
        self._sessions[session_id] = chat

    def clear(self, session_id: str):
        """Remove the stored chat for *session_id* if it exists."""
        self._sessions.pop(session_id, None)
