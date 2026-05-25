from fastapi import APIRouter

from src.api.serializers import task_to_response
from src.managers.task_service import TaskService
from src.models.schemas import TaskCreate, TaskResponse, TaskUpdate

router = APIRouter(prefix="/tasks", tags=["tasks"])


@router.post("/", response_model=TaskResponse, status_code=201)
def create_task(task_create: TaskCreate) -> TaskResponse:
    """Create a new task."""
    created_task = TaskService.create_task(task_create)
    return task_to_response(created_task)


@router.get("/", response_model=list[TaskResponse])
def list_tasks() -> list[TaskResponse]:
    """List all tasks."""
    tasks = TaskService.get_all_tasks()
    return [task_to_response(task) for task in tasks]


@router.get("/{task_id}", response_model=TaskResponse)
def get_task(task_id: int) -> TaskResponse:
    """Retrieve a task by ID."""
    task = TaskService.get_task_by_id(task_id)
    return task_to_response(task)


@router.put("/{task_id}", response_model=TaskResponse)
def update_task(task_id: int, task_update: TaskUpdate) -> TaskResponse:
    """Update an existing task."""
    updated_task = TaskService.update_task(task_id, task_update)
    return task_to_response(updated_task)


@router.delete("/{task_id}", response_model=dict[str, str], status_code=200)
def delete_task(task_id: int) -> dict[str, str]:
    """Delete a task by ID."""
    TaskService.delete_task(task_id)
    return {"detail": "Task deleted successfully."}
