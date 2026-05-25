import pytest

from src.managers.ai_task_manager import AITaskManager, AIValidationError
from src.models.enums import PriorityEnum, StatusEnum
from src.models.task import Task


def make_task(description: str = "", effort_hours: float = 0.0) -> Task:
    return Task(
        id=1,
        title="Test Task",
        description=description,
        priority=PriorityEnum.medium,
        effort_hours=effort_hours,
        status=StatusEnum.pending,
        assigned_to="Tester",
    )


def test_categorize_returns_valid_category(monkeypatch):
    task = make_task(description="Build a backend API endpoint.")

    monkeypatch.setattr("src.managers.ai_task_manager.complete", lambda *args, **kwargs: "Backend")
    enriched = AITaskManager.categorize(task)

    assert enriched.category == "Backend"


def test_estimate_parses_numeric_effort(monkeypatch):
    task = make_task(description="Create a landing page.")

    monkeypatch.setattr("src.managers.ai_task_manager.complete", lambda *args, **kwargs: "Approximately 4.5 hours")
    enriched = AITaskManager.estimate(task)

    assert enriched.effort_hours == 4.5


def test_describe_raises_when_response_empty(monkeypatch):
    task = make_task()
    monkeypatch.setattr("src.managers.ai_task_manager.complete", lambda *args, **kwargs: "")

    with pytest.raises(AIValidationError):
        AITaskManager.describe(task)


def test_categorize_raises_for_unknown_category(monkeypatch):
    task = make_task(description="Write a new test suite.")
    monkeypatch.setattr("src.managers.ai_task_manager.complete", lambda *args, **kwargs: "UnknownCategory")

    with pytest.raises(AIValidationError):
        AITaskManager.categorize(task)
