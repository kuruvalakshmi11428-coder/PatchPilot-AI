
import json
from datetime import datetime, timezone
from pathlib import Path

MEMORY_FILE = Path(__file__).resolve().parent.parent / "memory.json"


def load_memory():
    """Load previously saved project memory."""
    if not MEMORY_FILE.exists():
        return {"project": {}, "history": []}

    try:
        with MEMORY_FILE.open("r", encoding="utf-8") as file:
            data = json.load(file)

        data.setdefault("project", {})
        data.setdefault("history", [])
        return data

    except (json.JSONDecodeError, OSError):
        return {"project": {}, "history": []}


def save_memory(memory):
    """Persist project memory as JSON."""
    with MEMORY_FILE.open("w", encoding="utf-8") as file:
        json.dump(memory, file, indent=2, ensure_ascii=False)


def remember(event, details):
    """Save a timestamped event to long-term project memory."""
    memory = load_memory()

    memory["history"].append({
        "event": event,
        "details": details,
        "timestamp": datetime.now(timezone.utc).isoformat()
    })

    # Keep the most recent 100 events.
    memory["history"] = memory["history"][-100:]

    save_memory(memory)


def get_recent_memory(limit=5):
    """Return the most recent project events."""
    memory = load_memory()
    return list(reversed(memory["history"][-limit:]))
