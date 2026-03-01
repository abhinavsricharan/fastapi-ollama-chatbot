from typing import Dict, List
from app.config import MAX_HISTORY

# In-memory session store: { session_id: [{"role": ..., "content": ...}, ...] }
_sessions: Dict[str, List[dict]] = {}


def get_history(session_id: str) -> List[dict]:
    """Return the last MAX_HISTORY messages for a session."""
    return _sessions.get(session_id, [])[-MAX_HISTORY:]


def add_message(session_id: str, role: str, content: str) -> None:
    """Append a new message to the session history."""
    if session_id not in _sessions:
        _sessions[session_id] = []
    _sessions[session_id].append({"role": role, "content": content})


def clear_history(session_id: str) -> bool:
    """Delete a session's history. Returns True if it existed."""
    if session_id in _sessions:
        del _sessions[session_id]
        return True
    return False


def get_all_sessions() -> List[str]:
    """Return all active session IDs."""
    return list(_sessions.keys())
