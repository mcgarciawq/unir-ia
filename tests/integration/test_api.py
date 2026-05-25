from fastapi.testclient import TestClient

from src.main import app
from src.services.task_manager import TaskManager

client = TestClient(app)


def test_health_check():
    response = client.get("/health")

    assert response.status_code == 200
    assert response.json() == {"status": "ok", "message": "Task Manager API is running."}


def test_create_get_update_delete_task(monkeypatch):
    tasks = []

    def load_tasks():
        return tasks

    def save_tasks(updated_tasks):
        updated = list(updated_tasks)
        tasks.clear()
        tasks.extend(updated)

    monkeypatch.setattr(TaskManager, "load_tasks", staticmethod(load_tasks))
    monkeypatch.setattr(TaskManager, "save_tasks", staticmethod(save_tasks))

    create_payload = {
        "title": "Integration Task",
        "description": "Task for integration testing.",
        "priority": "low",
        "effort_hours": 1.5,
        "status": "pending",
        "assigned_to": "Integration Tester",
    }

    create_response = client.post("/tasks/", json=create_payload)
    assert create_response.status_code == 201
    created_task = create_response.json()
    assert created_task["id"] == 1
    assert created_task["title"] == create_payload["title"]

    list_response = client.get("/tasks/")
    assert list_response.status_code == 200
    assert len(list_response.json()) == 1

    get_response = client.get("/tasks/1")
    assert get_response.status_code == 200
    assert get_response.json()["id"] == 1

    update_payload = {"status": "in_progress"}
    update_response = client.put("/tasks/1", json=update_payload)
    assert update_response.status_code == 200
    assert update_response.json()["status"] == "in_progress"

    delete_response = client.delete("/tasks/1")
    assert delete_response.status_code == 200
    assert delete_response.json() == {"detail": "Task deleted successfully."}

    not_found_response = client.get("/tasks/1")
    assert not_found_response.status_code == 404
    assert not_found_response.json() == {"detail": "Task not found"}
