import json
from typing import List
from src.models.task import Task
from src.core.config import DATA_PATH 

class TaskManager:
    """
    Static service responsible for task persistence to JSON storage.
    Ensures compliance with static method requirements.
    """

    @staticmethod
    def load_tasks() -> List[Task]:
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
        except (json.JSONDecodeError, TypeError, ValueError):
            # Seguridad: evita que la API se rompa si el JSON está mal formado[cite: 1]
            return []

    @staticmethod
    def save_tasks(tasks: List[Task]) -> None:
        """
        Persist the list of Task objects into the JSON storage file[cite: 1].
        Converts objects back to dictionaries for JSON serialization[cite: 1].
        """
        # Asegura que la carpeta data exista antes de escribir
        DATA_PATH.parent.mkdir(parents=True, exist_ok=True)
        
        with open(DATA_PATH, "w", encoding="utf-8") as file:
            # Uso de to_dict() requerido por el entregable[cite: 1]
            json_data = [task.to_dict() for task in tasks]
            json.dump(json_data, file, indent=4)
