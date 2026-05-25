import pytest
from src.models.enums import PriorityEnum, StatusEnum
from src.models.task import Task
from src.services.task_manager import TaskManager
import src.services.task_manager

def test_load_tasks_returns_empty_for_missing_file(tmp_path, monkeypatch):
    data_file = tmp_path / "tasks.json"
    monkeypatch.setattr(src.services.task_manager, "DATA_PATH", data_file)
    tasks = TaskManager.load_tasks()
    assert tasks == []


def test_load_tasks_returns_empty_for_invalid_json(tmp_path, monkeypatch):
    data_file = tmp_path / "tasks.json"
    data_file.write_text("invalid json", encoding="utf-8")
    monkeypatch.setattr(src.services.task_manager, "DATA_PATH", data_file)
    tasks = TaskManager.load_tasks()
    assert tasks == []


def test_save_and_load_tasks(tmp_path, monkeypatch):
    data_file = tmp_path / "tasks.json"
    monkeypatch.setattr(src.services.task_manager, "DATA_PATH", data_file)
    task = Task(
        id=1,
        title="Saved Task",
        description="A task saved during unit testing.",
        priority=PriorityEnum.medium,
        effort_hours=3.0,
        status=StatusEnum.in_progress,
        assigned_to="Tester",
    )
    TaskManager.save_tasks([task])
    loaded_tasks = TaskManager.load_tasks()
    assert len(loaded_tasks) == 1
    assert loaded_tasks[0].id == task.id
    assert loaded_tasks[0].to_dict() == task.to_dict()