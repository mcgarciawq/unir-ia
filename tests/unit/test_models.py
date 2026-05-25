from src.models.enums import PriorityEnum, StatusEnum
from src.models.task import Task


def test_task_to_dict_and_from_dict():
    data = {
        "id": 1,
        "title": "Test Task",
        "description": "A task used for unit testing.",
        "priority": "high",
        "effort_hours": 2.5,
        "status": "pending",
        "assigned_to": "Tester",
    }

    task = Task.from_dict(data)
    assert task.id == 1
    assert task.title == "Test Task"
    assert task.description == "A task used for unit testing."
    assert task.priority == PriorityEnum.high
    assert task.effort_hours == 2.5
    assert task.status == StatusEnum.pending
    assert task.assigned_to == "Tester"
    assert task.to_dict() == data
