from src.models.enums import CategoryEnum
from src.models.schemas import AITaskPayload, AITaskResponse, TaskResponse
from src.models.task import Task


def task_to_response(task: Task) -> TaskResponse:
    """Convert a domain task into the public CRUD response schema."""
    return TaskResponse(**task.to_dict())


def ai_payload_to_task(payload: AITaskPayload) -> Task:
    """Convert an AI endpoint payload into the domain task model."""
    return Task(
        id=int(payload.id) if payload.id is not None else 0,
        title=payload.title,
        description=payload.description or "",
        priority=payload.priority,
        effort_hours=float(payload.effort_hours) if payload.effort_hours is not None else 0.0,
        status=payload.status,
        assigned_to=payload.assigned_to,
        category=payload.category.value if payload.category is not None else "",
        risk_analysis=payload.risk_analysis or "",
        risk_mitigation=payload.risk_mitigation or "",
    )


def task_to_ai_response(task: Task) -> AITaskResponse:
    """Convert a domain task into the public AI response schema."""
    category = None
    if task.category:
        try:
            category = CategoryEnum(task.category)
        except ValueError:
            category = None

    return AITaskResponse(
        id=task.id,
        title=task.title,
        description=task.description,
        priority=task.priority,
        effort_hours=task.effort_hours,
        status=task.status,
        assigned_to=task.assigned_to,
        category=category,
        risk_analysis=task.risk_analysis,
        risk_mitigation=task.risk_mitigation,
    )
