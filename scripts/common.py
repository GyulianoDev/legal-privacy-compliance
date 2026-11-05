import json
from datetime import datetime, timezone
from pathlib import Path

SKILL_ROOT = Path(__file__).resolve().parents[1]
REVIEW = "REQUIRES_HUMAN_REVIEW"


def timestamp():
    return datetime.now(timezone.utc).isoformat(timespec="seconds")


def load_json(path):
    return json.loads(Path(path).read_text(encoding="utf-8-sig"))


def write_json(path, value):
    Path(path).write_text(json.dumps(value, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def new_output(path):
    target = Path(path).resolve()
    if target.exists():
        raise ValueError(f"Output already exists: {target}. Choose a new directory.")
    target.mkdir(parents=True)
    return target


def safe_name(value):
    return "".join(char for char in str(value) if char.isalnum() or char in " -_./")[:100]


def main_guard(function):
    try:
        return function()
    except (ValueError, OSError, json.JSONDecodeError) as error:
        raise SystemExit(f"Error: {error}") from None
