from typing import Callable

from fastapi import APIRouter, HTTPException

from src.api.errors import map_ai_error
from src.api.serializers import ai_payload_to_task, task_to_ai_response
from src.managers.ai_task_manager import AITaskManager
from src.managers.task_service import TaskService
from src.models.schemas import AITaskPayload, AITaskResponse
from src.models.task import Task

router = APIRouter(prefix="/ai/tasks", tags=["AI Tasks"])


def _enrich_and_persist(
    task_payload: AITaskPayload,
    enrich_task: Callable[[Task], Task],
    default_status: int,
) -> AITaskResponse:
    task = ai_payload_to_task(task_payload)
    try:
        enriched = enrich_task(task)
    except Exception as error:
        raise map_ai_error(error, default_status=default_status)

    persisted = TaskService.upsert_task(enriched)
    return task_to_ai_response(persisted)


@router.post("/describe", response_model=AITaskResponse)
def describe_task(task_payload: AITaskPayload) -> AITaskResponse:
    if task_payload.description:
        raise HTTPException(status_code=400, detail="Description must be empty for describe endpoint.")

    return _enrich_and_persist(task_payload, AITaskManager.describe, default_status=502)


@router.post("/categorize", response_model=AITaskResponse)
def categorize_task(task_payload: AITaskPayload) -> AITaskResponse:
    if task_payload.category is not None:
        raise HTTPException(status_code=400, detail="Category must be empty for categorize endpoint.")

    return _enrich_and_persist(task_payload, AITaskManager.categorize, default_status=422)


@router.post("/estimate", response_model=AITaskResponse)
def estimate_task(task_payload: AITaskPayload) -> AITaskResponse:
    if task_payload.effort_hours is not None and task_payload.effort_hours > 0:
        raise HTTPException(status_code=400, detail="Effort hours must be empty or zero for estimate endpoint.")

    return _enrich_and_persist(task_payload, AITaskManager.estimate, default_status=422)


@router.post("/audit", response_model=AITaskResponse)
def audit_task(task_payload: AITaskPayload) -> AITaskResponse:
    if task_payload.risk_analysis:
        raise HTTPException(status_code=400, detail="risk_analysis must be empty for audit endpoint.")
    if task_payload.risk_mitigation:
        raise HTTPException(status_code=400, detail="risk_mitigation must be empty for audit endpoint.")
    if not task_payload.description:
        raise HTTPException(status_code=400, detail="Description is required for audit endpoint.")
    if task_payload.effort_hours is None or task_payload.effort_hours <= 0:
        raise HTTPException(status_code=400, detail="Effort hours must be provided and greater than zero for audit endpoint.")

    return _enrich_and_persist(task_payload, AITaskManager.audit, default_status=502)
