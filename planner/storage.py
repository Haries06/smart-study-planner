import json
from pathlib import Path

DB_PATH = Path(__file__).resolve().parents[1] / "tasks.json"


def load_tasks():
    """Load tasks from tasks.json or return an empty list."""
    if not DB_PATH.exists():
        DB_PATH.write_text("[]", encoding="utf-8")
        return []

    try:
        with open(DB_PATH, "r", encoding="utf-8") as f:
            data = json.load(f)

        if isinstance(data, list):
            return data
        return []
    except (json.JSONDecodeError, OSError):
        return []


def save_tasks(tasks):
    """Save tasks back to tasks.json."""
    with open(DB_PATH, "w", encoding="utf-8") as f:
        json.dump(tasks, f, indent=2)