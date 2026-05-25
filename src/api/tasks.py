from fastapi import APIRouter
from src.managers.task_manager_controller import TaskManagerController
from src.models.schemas import TaskCreate, TaskResponse, TaskUpdate

router = APIRouter(prefix="/tasks", tags=["tasks"])


@router.post("/", response_model=TaskResponse, status_code=201)
def create_task(task_create: TaskCreate) -> TaskResponse:
    """Create a new task."""
    created_task = TaskManagerController.create_task(task_create)
    return TaskResponse(**created_task.to_dict())


@router.get("/", response_model=list[TaskResponse])
def list_tasks() -> list[TaskResponse]:
    """List all tasks."""
    tasks = TaskManagerController.get_all_tasks()
    return [TaskResponse(**task.to_dict()) for task in tasks]


@router.get("/{task_id}", response_model=TaskResponse)
def get_task(task_id: int) -> TaskResponse:
    """Retrieve a task by ID."""
    task = TaskManagerController.get_task_by_id(task_id)
    return TaskResponse(**task.to_dict())


@router.put("/{task_id}", response_model=TaskResponse)
def update_task(task_id: int, task_update: TaskUpdate) -> TaskResponse:
    """Update an existing task."""
    updated_task = TaskManagerController.update_task(task_id, task_update)
    return TaskResponse(**updated_task.to_dict())


@router.delete("/{task_id}", response_model=dict, status_code=200)
def delete_task(task_id: int) -> dict:
    """Delete a task by ID."""
    TaskManagerController.delete_task(task_id)
    return {"detail": "Task deleted successfully."}
