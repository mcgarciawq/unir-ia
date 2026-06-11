import json
from types import SimpleNamespace

from src.managers.ai_story_manager import AIStoryManager
from src.models.enums import CategoryEnum, PriorityEnum, StatusEnum


def make_user_story() -> SimpleNamespace:
    return SimpleNamespace(
        project="TaskApp",
        role="Developer",
        goal="Generate tasks",
        reason="Plan implementation work",
        description="As a developer, I want tasks generated from a user story.",
        priority=PriorityEnum.medium,
        story_points=3,
        effort_hours=4.0,
    )


def test_generate_tasks_maps_unknown_category_to_other(monkeypatch):
    llm_response = [
        {
            "title": "Plan implementation",
            "description": "Define the implementation plan.",
            "priority": "medium",
            "effort_hours": 1.0,
            "status": "pending",
            "assigned_to": "Team",
            "category": "planning",
        }
    ]
    monkeypatch.setattr("src.managers.ai_story_manager.complete", lambda *args, **kwargs: json.dumps(llm_response))

    tasks = AIStoryManager.generate_tasks_for_story(make_user_story(), task_count=1)

    assert tasks[0].category == CategoryEnum.other


def test_generate_tasks_maps_blocker_priority_to_blocking(monkeypatch):
    llm_response = [
        {
            "title": "Resolve release blocker",
            "description": "Fix the issue blocking the release.",
            "priority": "blocker",
            "effort_hours": 2.0,
            "status": "pending",
            "assigned_to": "Team",
            "category": "Backend",
        }
    ]
    monkeypatch.setattr("src.managers.ai_story_manager.complete", lambda *args, **kwargs: json.dumps(llm_response))

    tasks = AIStoryManager.generate_tasks_for_story(make_user_story(), task_count=1)

    assert tasks[0].priority == PriorityEnum.blocking
    assert tasks[0].status == StatusEnum.pending
