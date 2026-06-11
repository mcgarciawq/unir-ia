import json
import os
import tempfile

from fastapi import HTTPException
from sqlalchemy import select

from src.core.config import DATA_PATH
from src.core.database import SessionLocal
from src.models.task import Task, TaskORM
from src.models.schemas import TaskCreate, TaskUpdate


class TaskManager:
    """Business logic for task persistence using SQLAlchemy."""

    @staticmethod
    def _task_from_orm(task_orm: TaskORM) -> Task:
        return Task(
            id=task_orm.id,
            title=task_orm.title,
            description=task_orm.description,
            priority=task_orm.priority,
            effort_hours=task_orm.effort_hours,
            status=task_orm.status,
            assigned_to=task_orm.assigned_to,
            category=task_orm.category or "",
            risk_analysis=task_orm.risk_analysis,
            risk_mitigation=task_orm.risk_mitigation,
            user_story_id=task_orm.user_story_id,
            created_at=task_orm.created_at.isoformat() if task_orm.created_at else None,
        )

    @staticmethod
    def get_all_tasks() -> list[Task]:
        # Testing mode: allow using legacy JSON storage when explicitly enabled.
        if os.getenv("TESTING_USE_JSON", "false").lower() == "true":
            return TaskManager.load_tasks()

        with SessionLocal() as session:
            tasks = session.execute(select(TaskORM)).scalars().all()
            return [TaskManager._task_from_orm(task) for task in tasks]

    @staticmethod
    def get_task_by_id(task_id: int) -> Task:
        if os.getenv("TESTING_USE_JSON", "false").lower() == "true":
            tasks = TaskManager.load_tasks()
            for t in tasks:
                if t.id == task_id:
                    return t
            raise HTTPException(status_code=404, detail="Task not found")

        with SessionLocal() as session:
            task = session.get(TaskORM, task_id)
            if task is None:
                raise HTTPException(status_code=404, detail="Task not found")
            return TaskManager._task_from_orm(task)

    @staticmethod
    def create_task(task_data: TaskCreate) -> Task:
        # Support legacy JSON-backed mode for tests
        if os.getenv("TESTING_USE_JSON", "false").lower() == "true":
            tasks = TaskManager.load_tasks()
            max_id = max((t.id for t in tasks), default=0)
            new_id = max_id + 1
            now = None
            task = Task(
                id=new_id,
                title=task_data.title,
                description=task_data.description,
                priority=task_data.priority,
                effort_hours=task_data.effort_hours,
                status=task_data.status,
                assigned_to=task_data.assigned_to,
                category=task_data.category.value if task_data.category is not None else "",
                risk_analysis="",
                risk_mitigation="",
                user_story_id=task_data.user_story_id,
                created_at=now,
            )
            tasks.append(task)
            TaskManager.save_tasks(tasks)
            return task

        with SessionLocal() as session:
            task_orm = TaskORM(
                title=task_data.title,
                description=task_data.description,
                priority=task_data.priority,
                effort_hours=task_data.effort_hours,
                status=task_data.status,
                assigned_to=task_data.assigned_to,
                category=task_data.category.value if task_data.category is not None else None,
                user_story_id=task_data.user_story_id,
            )
            session.add(task_orm)
            session.commit()
            session.refresh(task_orm)
            return TaskManager._task_from_orm(task_orm)

    @staticmethod
    def upsert_task(task: Task) -> Task:
        if os.getenv("TESTING_USE_JSON", "false").lower() == "true":
            tasks = TaskManager.load_tasks()
            if task.id and task.id > 0:
                for idx, existing_task in enumerate(tasks):
                    if existing_task.id == task.id:
                        updated = existing_task
                        updated.title = task.title
                        updated.description = task.description
                        updated.priority = task.priority
                        updated.effort_hours = task.effort_hours
                        updated.status = task.status
                        updated.assigned_to = task.assigned_to
                        updated.category = task.category or ""
                        updated.risk_analysis = task.risk_analysis
                        updated.risk_mitigation = task.risk_mitigation
                        updated.user_story_id = task.user_story_id
                        tasks[idx] = updated
                        TaskManager.save_tasks(tasks)
                        return updated

            max_id = max((t.id for t in tasks), default=0)
            new_id = max_id + 1
            new_task = Task(
                id=new_id,
                title=task.title,
                description=task.description,
                priority=task.priority,
                effort_hours=task.effort_hours,
                status=task.status,
                assigned_to=task.assigned_to,
                category=task.category or "",
                risk_analysis=task.risk_analysis,
                risk_mitigation=task.risk_mitigation,
                user_story_id=task.user_story_id,
                created_at=task.created_at,
            )
            tasks.append(new_task)
            TaskManager.save_tasks(tasks)
            return new_task

        with SessionLocal() as session:
            if task.id and task.id > 0:
                task_orm = session.get(TaskORM, task.id)
                if task_orm is not None:
                    task_orm.title = task.title
                    task_orm.description = task.description
                    task_orm.priority = task.priority
                    task_orm.effort_hours = task.effort_hours
                    task_orm.status = task.status
                    task_orm.assigned_to = task.assigned_to
                    task_orm.category = task.category or None
                    task_orm.risk_analysis = task.risk_analysis
                    task_orm.risk_mitigation = task.risk_mitigation
                    task_orm.user_story_id = task.user_story_id
                    session.commit()
                    session.refresh(task_orm)
                    return TaskManager._task_from_orm(task_orm)

            task_orm = TaskORM(
                title=task.title,
                description=task.description,
                priority=task.priority,
                effort_hours=task.effort_hours,
                status=task.status,
                assigned_to=task.assigned_to,
                category=task.category or None,
                risk_analysis=task.risk_analysis,
                risk_mitigation=task.risk_mitigation,
                user_story_id=task.user_story_id,
            )
            session.add(task_orm)
            session.commit()
            session.refresh(task_orm)
            return TaskManager._task_from_orm(task_orm)

    @staticmethod
    def update_task(task_id: int, update_data: TaskUpdate) -> Task:
        if os.getenv("TESTING_USE_JSON", "false").lower() == "true":
            tasks = TaskManager.load_tasks()
            for idx, t in enumerate(tasks):
                if t.id == task_id:
                    updated = t
                    if update_data.title is not None:
                        updated.title = update_data.title
                    if update_data.description is not None:
                        updated.description = update_data.description
                    if update_data.priority is not None:
                        updated.priority = update_data.priority
                    if update_data.effort_hours is not None:
                        updated.effort_hours = update_data.effort_hours
                    if update_data.status is not None:
                        updated.status = update_data.status
                    if update_data.assigned_to is not None:
                        updated.assigned_to = update_data.assigned_to
                    if update_data.user_story_id is not None:
                        updated.user_story_id = update_data.user_story_id
                    if update_data.category is not None:
                        updated.category = update_data.category.value
                    if update_data.risk_analysis is not None:
                        updated.risk_analysis = update_data.risk_analysis
                    if update_data.risk_mitigation is not None:
                        updated.risk_mitigation = update_data.risk_mitigation
                    tasks[idx] = updated
                    TaskManager.save_tasks(tasks)
                    return updated
            raise HTTPException(status_code=404, detail="Task not found")

        with SessionLocal() as session:
            task_orm = session.get(TaskORM, task_id)
            if task_orm is None:
                raise HTTPException(status_code=404, detail="Task not found")

            if update_data.title is not None:
                task_orm.title = update_data.title
            if update_data.description is not None:
                task_orm.description = update_data.description
            if update_data.priority is not None:
                task_orm.priority = update_data.priority
            if update_data.effort_hours is not None:
                task_orm.effort_hours = update_data.effort_hours
            if update_data.status is not None:
                task_orm.status = update_data.status
            if update_data.assigned_to is not None:
                task_orm.assigned_to = update_data.assigned_to
            if update_data.user_story_id is not None:
                task_orm.user_story_id = update_data.user_story_id
            if update_data.category is not None:
                task_orm.category = update_data.category.value
            if update_data.risk_analysis is not None:
                task_orm.risk_analysis = update_data.risk_analysis
            if update_data.risk_mitigation is not None:
                task_orm.risk_mitigation = update_data.risk_mitigation
            session.commit()
            session.refresh(task_orm)
            return TaskManager._task_from_orm(task_orm)

    @staticmethod
    def delete_task(task_id: int) -> None:
        if os.getenv("TESTING_USE_JSON", "false").lower() == "true":
            tasks = TaskManager.load_tasks()
            remaining = [t for t in tasks if t.id != task_id]
            if len(remaining) == len(tasks):
                raise HTTPException(status_code=404, detail="Task not found")
            TaskManager.save_tasks(remaining)
            return

        with SessionLocal() as session:
            task_orm = session.get(TaskORM, task_id)
            if task_orm is None:
                raise HTTPException(status_code=404, detail="Task not found")
            session.delete(task_orm)
            session.commit()

    @staticmethod
    def load_tasks() -> list[Task]:
        if not DATA_PATH.exists():
            return []

        try:
            with open(DATA_PATH, "r", encoding="utf-8") as file:
                raw_tasks = json.load(file)
            return [Task.from_dict(task_data) for task_data in raw_tasks]
        except json.JSONDecodeError:
            return []

    @staticmethod
    def save_tasks(tasks: list[Task]) -> None:
        DATA_PATH.parent.mkdir(parents=True, exist_ok=True)
        json_data = [task.to_dict() for task in tasks]

        with tempfile.NamedTemporaryFile("w", delete=False, encoding="utf-8") as tmp:
            json.dump(json_data, tmp, indent=4)
            temp_name = tmp.name
        os.replace(temp_name, DATA_PATH)
