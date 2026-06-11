from typing import Any

import pytest
from fastapi.testclient import TestClient

from src.managers.ai_story_manager import AIStoryManager
from src.models.enums import PriorityEnum, StatusEnum
from src.models.schemas import TaskCreate, UserStoryCreate
from tests.conftest import persist_user_story, sample_user_story_create


@pytest.fixture(autouse=True)
def use_sqlite_database(sqlite_db, monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.delenv("TESTING_USE_JSON", raising=False)


def test_list_user_stories_json_empty(api_client: TestClient) -> None:
    response = api_client.get("/user-stories/json")

    assert response.status_code == 200
    assert response.json() == {"user_stories": []}


def test_list_user_stories_json_returns_persisted_stories(api_client: TestClient, sqlite_db) -> None:
    session = sqlite_db()
    try:
        persist_user_story(session)
    finally:
        session.close()

    response = api_client.get("/user-stories/json")

    assert response.status_code == 200
    payload = response.json()
    assert len(payload["user_stories"]) == 1
    assert payload["user_stories"][0]["project"] == "ExpenseApp"
    assert payload["user_stories"][0]["goal"] == "Registrar gastos"


def test_get_user_story_by_id(api_client: TestClient, sqlite_db) -> None:
    session = sqlite_db()
    try:
        story = persist_user_story(session)
        story_id = story.id
    finally:
        session.close()

    response = api_client.get(f"/user-stories/{story_id}")

    assert response.status_code == 200
    payload = response.json()
    assert payload["id"] == story_id
    assert payload["role"] == "Usuario"
    assert payload["story_points"] == 3


def test_get_user_story_not_found(api_client: TestClient) -> None:
    response = api_client.get("/user-stories/999")

    assert response.status_code == 404
    assert response.json() == {"detail": "User story not found"}


def test_list_story_tasks_json_returns_only_matching_tasks(api_client: TestClient, sqlite_db) -> None:
    from src.models.task import TaskORM

    session = sqlite_db()
    try:
        story = persist_user_story(session)
        other_story = persist_user_story(session, project="OtherApp")
        session.add(
            TaskORM(
                title="Tarea de la historia",
                description="Detalle de la tarea",
                priority=PriorityEnum.high,
                effort_hours=2.0,
                status=StatusEnum.pending,
                assigned_to="Dev 1",
                user_story_id=story.id,
            )
        )
        session.add(
            TaskORM(
                title="Tarea de otra historia",
                description="No debe aparecer",
                priority=PriorityEnum.low,
                effort_hours=1.0,
                status=StatusEnum.pending,
                assigned_to="Dev 2",
                user_story_id=other_story.id,
            )
        )
        session.commit()
        story_id = story.id
    finally:
        session.close()

    response = api_client.get(f"/user-stories/{story_id}/tasks/json")

    assert response.status_code == 200
    payload = response.json()
    assert len(payload["tasks"]) == 1
    assert payload["tasks"][0]["title"] == "Tarea de la historia"
    assert payload["tasks"][0]["user_story_id"] == story_id


def test_list_story_tasks_json_empty_when_story_has_no_tasks(api_client: TestClient, sqlite_db) -> None:
    session = sqlite_db()
    try:
        story = persist_user_story(session)
        story_id = story.id
    finally:
        session.close()

    response = api_client.get(f"/user-stories/{story_id}/tasks/json")

    assert response.status_code == 200
    assert response.json() == {"tasks": []}


def test_create_user_story_post_redirects_on_success(
    api_client: TestClient,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    def fake_generate_user_story(prompt: str) -> UserStoryCreate:
        assert prompt == "Como usuario quiero registrar gastos"
        return sample_user_story_create()

    monkeypatch.setattr(
        AIStoryManager,
        "generate_user_story_from_prompt",
        staticmethod(fake_generate_user_story),
    )

    response = api_client.post(
        "/user-stories",
        data={"prompt": "Como usuario quiero registrar gastos"},
        follow_redirects=False,
    )

    assert response.status_code == 303
    assert response.headers["location"] == "/user-stories"

    list_response = api_client.get("/user-stories/json")
    assert len(list_response.json()["user_stories"]) == 1


def test_create_user_story_post_redirects_with_error(
    api_client: TestClient,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    def fake_generate_user_story(_prompt: str) -> UserStoryCreate:
        raise RuntimeError("Fallo de IA")

    monkeypatch.setattr(
        AIStoryManager,
        "generate_user_story_from_prompt",
        staticmethod(fake_generate_user_story),
    )

    response = api_client.post(
        "/user-stories",
        data={"prompt": "prompt inválido"},
        follow_redirects=False,
    )

    assert response.status_code == 303
    assert response.headers["location"].startswith("/user-stories?error=")


def test_generate_tasks_post_persists_tasks_and_redirects(
    api_client: TestClient,
    sqlite_db,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    session = sqlite_db()
    try:
        story = persist_user_story(session)
        story_id = story.id
    finally:
        session.close()

    fake_tasks = [
        TaskCreate(
            title="Tarea generada",
            description="Descripción generada",
            priority=PriorityEnum.medium,
            effort_hours=2.0,
            status=StatusEnum.pending,
            assigned_to="QA",
        )
    ]

    def fake_generate_tasks(story: Any, task_count: int = 3) -> list[TaskCreate]:
        assert story.id == story_id
        assert task_count == 3
        return fake_tasks

    monkeypatch.setattr(
        AIStoryManager,
        "generate_tasks_for_story",
        staticmethod(fake_generate_tasks),
    )

    response = api_client.post(
        f"/user-stories/{story_id}/generate-tasks",
        follow_redirects=False,
    )

    assert response.status_code == 303
    assert response.headers["location"] == f"/user-stories/{story_id}/tasks"

    tasks_response = api_client.get(f"/user-stories/{story_id}/tasks/json")
    payload = tasks_response.json()
    assert len(payload["tasks"]) == 1
    assert payload["tasks"][0]["title"] == "Tarea generada"
    assert payload["tasks"][0]["user_story_id"] == story_id


def test_generate_tasks_json_response(
    api_client: TestClient,
    sqlite_db,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    session = sqlite_db()
    try:
        story = persist_user_story(session)
        story_id = story.id
    finally:
        session.close()

    fake_tasks = [
        TaskCreate(
            title="Tarea JSON",
            description="Generada vía API JSON",
            priority=PriorityEnum.low,
            effort_hours=1.0,
            status=StatusEnum.pending,
            assigned_to="Dev",
        )
    ]

    monkeypatch.setattr(
        AIStoryManager,
        "generate_tasks_for_story",
        staticmethod(lambda story, task_count=3: fake_tasks),
    )

    response = api_client.post(
        f"/user-stories/{story_id}/generate-tasks",
        data={"task_count": "3"},
        headers={"Accept": "application/json"},
    )

    assert response.status_code == 200
    assert response.json()["tasks_created"] == 1

    tasks_response = api_client.get(f"/user-stories/{story_id}/tasks/json")
    assert len(tasks_response.json()["tasks"]) == 1


def test_delete_user_story(api_client: TestClient, sqlite_db) -> None:
    session = sqlite_db()
    try:
        story = persist_user_story(session)
        story_id = story.id
    finally:
        session.close()

    response = api_client.delete(f"/user-stories/{story_id}")

    assert response.status_code == 200
    assert response.json() == {"detail": "User story deleted successfully."}
    assert api_client.get(f"/user-stories/{story_id}").status_code == 404


def test_delete_user_story_not_found(api_client: TestClient) -> None:
    response = api_client.delete("/user-stories/999")

    assert response.status_code == 404
    assert response.json() == {"detail": "User story not found"}


def test_delete_user_story_cascades_tasks(api_client: TestClient, sqlite_db) -> None:
    from src.models.task import TaskORM

    session = sqlite_db()
    try:
        story = persist_user_story(session)
        task = TaskORM(
            title="Tarea asociada",
            description="Se elimina con la historia",
            priority=PriorityEnum.medium,
            effort_hours=1.0,
            status=StatusEnum.pending,
            assigned_to="Dev",
            user_story_id=story.id,
        )
        session.add(task)
        session.commit()
        story_id = story.id
        task_id = task.id
    finally:
        session.close()

    response = api_client.delete(f"/user-stories/{story_id}")
    assert response.status_code == 200
    assert api_client.get(f"/tasks/{task_id}").status_code == 404
