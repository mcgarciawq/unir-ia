from typing import List

from fastapi import HTTPException

from src.models.schemas import TaskCreate, TaskResponse, TaskUpdate
from src.models.task import Task
from src.services.task_manager import TaskManager


class TaskManagerController:
    """Business logic coordinator between API routes and task persistence."""

    @staticmethod
    def get_all_tasks() -> List[Task]:
        """Return all tasks from storage."""
        return TaskManager.load_tasks()

    @staticmethod
    def get_task_by_id(task_id: int) -> Task:
        """Return a task matching the requested identifier."""
        tasks = TaskManager.load_tasks()
        for task in tasks:
            if task.id == task_id:
                return task
        raise HTTPException(status_code=404, detail="Task not found")

    @staticmethod
    def create_task(task_data: TaskCreate) -> Task:
        """Create a new task and persist it to storage."""
        tasks = TaskManager.load_tasks()
        next_id = max((task.id for task in tasks), default=0) + 1
        new_task = Task(
            id=next_id,
            title=task_data.title,
            description=task_data.description,
            priority=task_data.priority,
            effort_hours=task_data.effort_hours,
            status=task_data.status,
            assigned_to=task_data.assigned_to,
        )
        tasks.append(new_task)
        TaskManager.save_tasks(tasks)
        return new_task

    @staticmethod
    def update_task(task_id: int, update_data: TaskUpdate) -> Task:
        """Apply updates to an existing task and persist changes."""
        tasks = TaskManager.load_tasks()
        for index, task in enumerate(tasks):
            if task.id == task_id:
                if update_data.title is not None:
                    task.title = update_data.title
                if update_data.description is not None:
                    task.description = update_data.description
                if update_data.priority is not None:
                    task.priority = update_data.priority
                if update_data.effort_hours is not None:
                    task.effort_hours = update_data.effort_hours
                if update_data.status is not None:
                    task.status = update_data.status
                if update_data.assigned_to is not None:
                    task.assigned_to = update_data.assigned_to
                tasks[index] = task
                TaskManager.save_tasks(tasks)
                return task

        raise HTTPException(status_code=404, detail="Task not found")

    @staticmethod
    def delete_task(task_id: int) -> None:
        """Delete a task from storage by its identifier."""
        tasks = TaskManager.load_tasks()
        updated_tasks = [task for task in tasks if task.id != task_id]
        if len(updated_tasks) == len(tasks):
            raise HTTPException(status_code=404, detail="Task not found")
        TaskManager.save_tasks(updated_tasks)
