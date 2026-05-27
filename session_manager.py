import json
import os
from datetime import datetime
from pathlib import Path

SESSIONS_DIR = Path("data/sessions")
SESSIONS_DIR.mkdir(exist_ok=True)


def save_session(history: list, session_id: str = None) -> str:
    """Save conversation history to a file. Returns the session ID."""
    if not session_id:
        session_id = datetime.now().strftime("%Y%m%d_%H%M%S")
    
    session_data = {
        "id": session_id,
        "saved_at": datetime.now().isoformat(),
        "turn_count": len([m for m in history if m["role"] == "user"]),
        "history": _serialize_history(history)
    }
    
    path = SESSIONS_DIR / f"{session_id}.json"
    with open(path, "w") as f:
        json.dump(session_data, f, indent=2)
    
    return session_id


def load_session(session_id: str) -> list:
    """Load a previous conversation history."""
    path = SESSIONS_DIR / f"{session_id}.json"
    if not path.exists():
        raise FileNotFoundError(f"Session {session_id} not found")
    
    with open(path) as f:
        data = json.load(f)
    
    return _deserialize_history(data["history"])


def list_sessions() -> list:
    """List all saved sessions."""
    sessions = []
    for path in sorted(SESSIONS_DIR.glob("*.json"), reverse=True):
        with open(path) as f:
            data = json.load(f)
        sessions.append({
            "id": data["id"],
            "saved_at": data["saved_at"],
            "turns": data["turn_count"]
        })
    return sessions


def _serialize_history(history: list) -> list:
    """Convert message history to a JSON-serializable format."""
    serialized = []
    for msg in history:
        if isinstance(msg["content"], str):
            serialized.append(msg)
        elif isinstance(msg["content"], list):
            # Convert SDK objects to dicts
            content = []
            for block in msg["content"]:
                if hasattr(block, "model_dump"):
                    content.append(block.model_dump())
                elif isinstance(block, dict):
                    content.append(block)
            serialized.append({"role": msg["role"], "content": content})
    return serialized


def _deserialize_history(history: list) -> list:
    """Load serialized history back to the format the API expects."""
    # The serialized format already works — dicts are accepted by the API
    return history