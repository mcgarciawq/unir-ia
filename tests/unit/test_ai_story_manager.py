import json
from types import SimpleNamespace
from typing import cast

import pytest
from src.managers.ai_story_manager import AIStoryManager
from src.models.enums import CategoryEnum, PriorityEnum, StatusEnum
from src.models.user_story import UserStory


def make_user_story() -> UserStory:
    return cast(
        UserStory,
        SimpleNamespace(
            project="TaskApp",
            role="Developer",
            goal="Generate tasks",
            reason="Plan implementation work",
            description="As a developer, I want tasks generated from a user story.",
            priority=PriorityEnum.medium,
            story_points=3,
            effort_hours=4.0,
        ),
    )


def fake_retrieve(*_args: object, **_kwargs: object) -> str:
    return ""


def test_generate_tasks_maps_unknown_category_to_other(monkeypatch: pytest.MonkeyPatch) -> None:
    llm_response: list[dict[str, object]] = [
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

    def fake_complete(*_args: object, **_kwargs: object) -> str:
        return json.dumps(llm_response)

    monkeypatch.setattr("src.managers.ai_story_manager.complete", fake_complete)
    monkeypatch.setattr("src.managers.ai_story_manager.RAGManager.retrieve", fake_retrieve)

    tasks = AIStoryManager.generate_tasks_for_story(make_user_story(), task_count=1)

    assert tasks[0].category == CategoryEnum.other


def test_generate_tasks_maps_blocker_priority_to_blocking(monkeypatch: pytest.MonkeyPatch) -> None:
    llm_response: list[dict[str, object]] = [
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

    def fake_complete(*_args: object, **_kwargs: object) -> str:
        return json.dumps(llm_response)

    monkeypatch.setattr("src.managers.ai_story_manager.complete", fake_complete)
    monkeypatch.setattr("src.managers.ai_story_manager.RAGManager.retrieve", fake_retrieve)

    tasks = AIStoryManager.generate_tasks_for_story(make_user_story(), task_count=1)

    assert tasks[0].priority == PriorityEnum.blocking
    assert tasks[0].status == StatusEnum.pending
