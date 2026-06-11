from pathlib import Path
from urllib.parse import quote

from fastapi import APIRouter, Form, HTTPException, Request
from fastapi.responses import FileResponse, RedirectResponse

from src.ai.exceptions import LLMCallError, LLMNotConfiguredError
from src.api.serializers import task_to_response, user_story_to_response
from src.managers.ai_story_manager import AIStoryManager
from src.managers.story_service import StoryService
from src.managers.task_service import TaskService
from src.models.schemas import TaskSchemas, UserStorySchema, UserStorySchemas

router = APIRouter(prefix="/user-stories", tags=["user-stories"])

STATIC_DIR = Path(__file__).resolve().parents[2] / "static"


def _user_stories_page() -> FileResponse:
    return FileResponse(STATIC_DIR / "user-stories.html", media_type="text/html")


def _tasks_page() -> FileResponse:
    return FileResponse(STATIC_DIR / "tasks.html", media_type="text/html")


def _redirect_with_error(path: str, error: str) -> RedirectResponse:
    return RedirectResponse(url=f"{path}?error={quote(str(error))}", status_code=303)


def _wants_json_response(request: Request) -> bool:
    return "application/json" in request.headers.get("accept", "")


@router.get("")
def list_user_stories() -> FileResponse:
    """Serve the user stories HTML page."""
    return _user_stories_page()


@router.get("/json", response_model=UserStorySchemas)
def list_user_stories_json() -> UserStorySchemas:
    """Return all user stories using the Pydantic plural schema."""
    stories = StoryService.get_all_user_stories()
    return UserStorySchemas(user_stories=[user_story_to_response(story) for story in stories])


@router.get("/{story_id}", response_model=UserStorySchema)
def get_user_story(story_id: int) -> UserStorySchema:
    """Return a single user story by ID."""
    story = StoryService.get_user_story_by_id(story_id)
    return user_story_to_response(story)


@router.delete("/{story_id}", response_model=dict[str, str])
def delete_user_story(story_id: int) -> dict[str, str]:
    """Delete a user story and its associated tasks."""
    StoryService.delete_user_story(story_id)
    return {"detail": "User story deleted successfully."}


@router.post("")
def create_user_story(prompt: str = Form(...)):
    """Generate and persist a user story from a prompt."""
    try:
        story_data = AIStoryManager.generate_user_story_from_prompt(prompt)
        StoryService.create_user_story(story_data)
        return RedirectResponse(url="/user-stories", status_code=303)
    except HTTPException:
        raise
    except Exception as error:
        return _redirect_with_error("/user-stories", str(error))


@router.post("/{story_id}/generate-tasks")
def generate_tasks(request: Request, story_id: int, task_count: int = Form(3)):
    """Generate tasks for a specific user story and persist them."""
    tasks_path = f"/user-stories/{story_id}/tasks"
    try:
        story = StoryService.get_user_story_by_id(story_id)
        tasks = AIStoryManager.generate_tasks_for_story(story, task_count=task_count)

        for task in tasks:
            task.user_story_id = story_id
            TaskService.create_task(task)

        if _wants_json_response(request):
            return {
                "detail": "Tasks generated successfully.",
                "tasks_created": len(tasks),
            }

        return RedirectResponse(url=tasks_path, status_code=303)
    except HTTPException:
        raise
    except LLMNotConfiguredError as error:
        if _wants_json_response(request):
            raise HTTPException(status_code=503, detail=str(error)) from error
        return _redirect_with_error(tasks_path, str(error))
    except LLMCallError as error:
        if _wants_json_response(request):
            raise HTTPException(status_code=502, detail=str(error)) from error
        return _redirect_with_error(tasks_path, str(error))
    except Exception as error:
        if _wants_json_response(request):
            raise HTTPException(status_code=500, detail=str(error)) from error
        return _redirect_with_error(tasks_path, str(error))


@router.get("/{story_id}/tasks/json", response_model=TaskSchemas)
def list_story_tasks_json(story_id: int) -> TaskSchemas:
    """Return tasks associated with a specific user story."""
    StoryService.get_user_story_by_id(story_id)
    all_tasks = TaskService.get_all_tasks()
    story_tasks = [task for task in all_tasks if task.user_story_id == story_id]
    return TaskSchemas(tasks=[task_to_response(task) for task in story_tasks])


@router.get("/{story_id}/tasks")
def list_story_tasks(story_id: int) -> FileResponse:
    """Serve the tasks HTML page for a user story."""
    return _tasks_page()
