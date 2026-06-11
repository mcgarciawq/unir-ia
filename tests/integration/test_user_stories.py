from typing import Any

from fastapi.testclient import TestClient

from src.main import app
from src.services.task_manager import TaskManager

client = TestClient(app)


def test_create_and_generate_tasks(monkeypatch: Any) -> None:
    monkeypatch.setenv("TESTING_USE_JSON", "true")

    def load_tasks() -> list[dict[str, Any]]:
        return []

    def save_tasks(_: list[dict[str, Any]]) -> None:
        return None

    monkeypatch.setattr(TaskManager, "load_tasks", staticmethod(load_tasks))
    monkeypatch.setattr(TaskManager, "save_tasks", staticmethod(save_tasks))

    from src.managers.ai_story_manager import AIStoryManager
    from src.managers.story_service import StoryService
    from types import SimpleNamespace

    fake_story: dict[str, Any] = {
        "project": "ExpenseApp",
        "role": "Usuario",
        "goal": "Registrar gastos",
        "reason": "Llevar control financiero",
        "description": "Como usuario quiero poder registrar mis gastos",
        "priority": "medium",
        "story_points": 3,
        "effort_hours": 4.0,
    }

    def fake_generate_user_story(prompt: str) -> dict[str, Any]:
        return fake_story

    def fake_create_user_story(_: Any) -> None:
        return None

    def fake_get_all_user_stories() -> list[Any]:
        return []

    def fake_get_user_story_by_id(_id: int) -> Any:
        return SimpleNamespace(id=_id)

    monkeypatch.setattr(AIStoryManager, "generate_user_story_from_prompt", staticmethod(fake_generate_user_story))
    monkeypatch.setattr(StoryService, "create_user_story", staticmethod(fake_create_user_story))
    monkeypatch.setattr(StoryService, "get_all_user_stories", staticmethod(fake_get_all_user_stories))
    monkeypatch.setattr(StoryService, "get_user_story_by_id", staticmethod(fake_get_user_story_by_id))

    def fake_generate_tasks(s: Any, task_count: int = 3) -> list[Any]:
        return []

    monkeypatch.setattr(AIStoryManager, "generate_tasks_for_story", staticmethod(fake_generate_tasks))

    response = client.post("/user-stories/", data={"prompt": "Como usuario quiero registrar gastos"})
    assert response.status_code in (200, 302, 303)

    gen_resp = client.post("/user-stories/1/generate-tasks")
    assert gen_resp.status_code in (200, 302, 303, 400, 422)


def test_user_stories_pages_serve_static_html() -> None:
    stories_page = client.get("/user-stories")
    assert stories_page.status_code == 200
    assert "text/html" in stories_page.headers.get("content-type", "")
    assert "Historias de Usuario" in stories_page.text

    tasks_page = client.get("/user-stories/1/tasks")
    assert tasks_page.status_code == 200
    assert "text/html" in tasks_page.headers.get("content-type", "")
    assert "Tareas de la historia" in tasks_page.text
