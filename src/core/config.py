from pathlib import Path

BASE_DIR = Path(__file__).resolve().parents[2]
DATA_PATH = BASE_DIR / "data" / "tasks.json"

API_TITLE = "Task Manager API"
API_VERSION = "1.0.0"