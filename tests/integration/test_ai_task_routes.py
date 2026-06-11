from fastapi.testclient import TestClient
import pytest

from src.main import app
from src.models.enums import PriorityEnum, StatusEnum
from src.models.task import Task
from src.services.task_manager import TaskManager

client = TestClient(app)


@pytest.fixture
def stored_tasks(monkeypatch):
    monkeypatch.setenv("TESTING_USE_JSON", "true")
    tasks = []

    def load_tasks():
        return tasks

    def save_tasks(updated_tasks):
        updated = list(updated_tasks)
        tasks.clear()
        tasks.extend(updated)

    monkeypatch.setattr(TaskManager, "load_tasks", staticmethod(load_tasks))
    monkeypatch.setattr(TaskManager, "save_tasks", staticmethod(save_tasks))
    return tasks


def test_docs_available():
    response = client.get("/openapi.json")
    assert response.status_code == 200
    assert "/ai/tasks/describe" in response.json()["paths"]


def test_describe_endpoint(monkeypatch, stored_tasks):
    def fake_complete(*args, **kwargs):
        return "AI-generated description for the task."

    monkeypatch.setattr("src.managers.ai_task_manager.complete", fake_complete)

    payload = {
        "title": "Write tests",
        "description": "",
        "priority": "medium",
        "effort_hours": 2.0,
        "status": "pending",
        "assigned_to": "Developer",
    }

    response = client.post("/ai/tasks/describe", json=payload)
    assert response.status_code == 200
    assert response.json()["description"] == "AI-generated description for the task."
    assert response.json()["id"] == 1
    assert len(stored_tasks) == 1
    assert stored_tasks[0].description == "AI-generated description for the task."


def test_describe_endpoint_updates_existing_task(monkeypatch, stored_tasks):
    stored_tasks.append(
        Task(
            id=7,
            title="Existing task",
            description="",
            priority=PriorityEnum.medium,
            effort_hours=2.0,
            status=StatusEnum.pending,
            assigned_to="Developer",
        )
    )
    monkeypatch.setattr(
        "src.managers.ai_task_manager.complete",
        lambda *args, **kwargs: "Updated AI description.",
    )

    payload = {
        "id": 7,
        "title": "Existing task",
        "description": "",
        "priority": "medium",
        "effort_hours": 2.0,
        "status": "pending",
        "assigned_to": "Developer",
    }

    response = client.post("/ai/tasks/describe", json=payload)

    assert response.status_code == 200
    assert response.json()["id"] == 7
    assert len(stored_tasks) == 1
    assert stored_tasks[0].description == "Updated AI description."


def test_categorize_endpoint(monkeypatch, stored_tasks):
    monkeypatch.setattr("src.managers.ai_task_manager.complete", lambda *args, **kwargs: "Backend")

    payload = {
        "title": "Fix authentication bug",
        "description": "Login fails for new users.",
        "priority": "high",
        "effort_hours": 3.5,
        "status": "pending",
        "assigned_to": "Developer",
    }

    response = client.post("/ai/tasks/categorize", json=payload)
    assert response.status_code == 200
    assert response.json()["category"] == "Backend"
    assert response.json()["id"] == 1
    assert len(stored_tasks) == 1
    assert stored_tasks[0].category == "Backend"


def test_estimate_endpoint(monkeypatch, stored_tasks):
    monkeypatch.setattr("src.managers.ai_task_manager.complete", lambda *args, **kwargs: "5")

    payload = {
        "title": "Prepare deployment docs",
        "description": "Document the deployment process.",
        "priority": "low",
        "effort_hours": 0.0,
        "status": "pending",
        "assigned_to": "DevOps",
    }

    response = client.post("/ai/tasks/estimate", json=payload)
    assert response.status_code == 200
    assert response.json()["effort_hours"] == 5.0
    assert response.json()["id"] == 1
    assert len(stored_tasks) == 1
    assert stored_tasks[0].effort_hours == 5.0


def test_audit_endpoint(monkeypatch, stored_tasks):
    def fake_complete(*args, **kwargs):
        system_prompt = (kwargs.get("system_prompt") or "").lower()
        if "risk analyst" in system_prompt:
            return "There is a risk due to third-party dependencies."
        return "Use automated checks and contingency planning."

    monkeypatch.setattr("src.managers.ai_task_manager.complete", fake_complete)

    payload = {
        "title": "Integrate payment gateway",
        "description": "Add a secure payment provider integration.",
        "priority": "high",
        "effort_hours": 8.0,
        "status": "pending",
        "assigned_to": "Backend Team",
    }

    response = client.post("/ai/tasks/audit", json=payload)
    assert response.status_code == 200
    assert "risk_analysis" in response.json()
    assert "risk_mitigation" in response.json()
    assert response.json()["risk_analysis"] == "There is a risk due to third-party dependencies."
    assert response.json()["risk_mitigation"] == "Use automated checks and contingency planning."
    assert response.json()["id"] == 1
    assert len(stored_tasks) == 1
    assert stored_tasks[0].risk_analysis == "There is a risk due to third-party dependencies."
    assert stored_tasks[0].risk_mitigation == "Use automated checks and contingency planning."
