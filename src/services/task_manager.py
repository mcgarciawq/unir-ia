import json
import os
import tempfile

from src.core.config import DATA_PATH
from src.models.task import Task


class TaskManager:
    """
    Static service responsible for task persistence to JSON storage.
    Ensures compliance with static method requirements.
    """

    @staticmethod
    def load_tasks() -> list[Task]:
        """
        Load tasks from JSON and convert them to Task objects.
        Handles missing or corrupt files by returning an empty list.
        """
        if not DATA_PATH.exists():
            return []

        try:
            with open(DATA_PATH, "r", encoding="utf-8") as file:
                raw_tasks = json.load(file)
            # Conversión obligatoria de dict a objeto Task
            return [Task.from_dict(task_data) for task_data in raw_tasks]
        except json.JSONDecodeError:
            return []

    @staticmethod
    def save_tasks(tasks: list[Task]) -> None:
        DATA_PATH.parent.mkdir(parents=True, exist_ok=True)

        json_data = [task.to_dict() for task in tasks]

        # Escritura segura
        with tempfile.NamedTemporaryFile("w", delete=False, encoding="utf-8") as tmp:
            json.dump(json_data, tmp, indent=4)
            temp_name = tmp.name

        os.replace(temp_name, DATA_PATH)
