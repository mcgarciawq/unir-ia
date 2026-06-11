from src.models.schemas import TaskCreate, TaskUpdate
from src.models.task import Task
from src.services.task_manager import TaskManager


class TaskService:
    """Business logic coordinator between API routes and task persistence."""

    @staticmethod
    def get_all_tasks() -> list[Task]:
        """Return all tasks from storage."""
        return TaskManager.get_all_tasks()

    @staticmethod
    def get_task_by_id(task_id: int) -> Task:
        """Return a task matching the requested identifier."""
        return TaskManager.get_task_by_id(task_id)

    @staticmethod
    def create_task(task_data: TaskCreate) -> Task:
        """Create a new task and persist it to storage."""
        return TaskManager.create_task(task_data)

    @staticmethod
    def upsert_task(task: Task) -> Task:
        """Update an existing task or create it when no stored ID matches."""
        return TaskManager.upsert_task(task)

    @staticmethod
    def update_task(task_id: int, update_data: TaskUpdate) -> Task:
        """Apply updates to an existing task and persist changes."""
        return TaskManager.update_task(task_id, update_data)

    @staticmethod
    def delete_task(task_id: int) -> None:
        """Delete a task from storage by its identifier."""
        TaskManager.delete_task(task_id)
