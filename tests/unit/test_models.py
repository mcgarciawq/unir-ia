from src.models.enums import CategoryEnum, PriorityEnum, StatusEnum
from src.models.task import Task


def test_task_to_dict_and_from_dict():
    data: dict[str, object] = {
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
    assert task.category == ""
    assert task.risk_analysis == ""
    assert task.risk_mitigation == ""
    expected_data: dict[str, object] = data | {
        "category": None,
        "risk_analysis": "",
        "risk_mitigation": "",
    }
    assert task.to_dict() == expected_data


def test_task_from_dict_maps_unknown_category_to_other():
    data: dict[str, object] = {
        "id": 1,
        "title": "Legacy Task",
        "description": "A task with an old category value.",
        "priority": "medium",
        "effort_hours": 1.0,
        "status": "pending",
        "assigned_to": "Tester",
        "category": "Database",
    }

    task = Task.from_dict(data)

    assert task.category == CategoryEnum.other.value


def test_task_from_dict_maps_unknown_priority_to_medium():
    data: dict[str, object] = {
        "id": 1,
        "title": "Legacy Priority Task",
        "description": "A task with an old priority value.",
        "priority": "urgent",
        "effort_hours": 1.0,
        "status": "pending",
        "assigned_to": "Tester",
    }

    task = Task.from_dict(data)

    assert task.priority == PriorityEnum.medium
