from src.api.serializers import user_story_to_response
from src.managers.story_service import StoryService
from src.models.enums import PriorityEnum, StatusEnum
from src.models.schemas import UserStorySchema
from src.models.task import TaskORM
from src.models.user_story import UserStory
from tests.conftest import persist_user_story, sample_user_story_create


def test_user_story_model_persists_expected_fields(sqlite_db) -> None:
    session = sqlite_db()
    try:
        story = persist_user_story(
            session,
            project="TaskApp",
            role="Admin",
            goal="Gestionar tareas",
            reason="Organizar el trabajo",
            description="Como admin quiero gestionar tareas del equipo",
            priority=PriorityEnum.high,
            story_points=5,
            effort_hours=8.0,
        )
    finally:
        session.close()

    assert story.id == 1
    assert story.project == "TaskApp"
    assert story.role == "Admin"
    assert story.goal == "Gestionar tareas"
    assert story.reason == "Organizar el trabajo"
    assert story.description == "Como admin quiero gestionar tareas del equipo"
    assert story.priority == PriorityEnum.high
    assert story.story_points == 5
    assert story.effort_hours == 8.0
    assert story.created_at is not None


def test_user_story_tasks_relationship(sqlite_db) -> None:
    session = sqlite_db()
    try:
        story = persist_user_story(session)
        task = TaskORM(
            title="Crear formulario",
            description="Implementar el formulario de gastos",
            priority=PriorityEnum.medium,
            effort_hours=3.0,
            status=StatusEnum.pending,
            assigned_to="Frontend Dev",
            user_story_id=story.id,
        )
        session.add(task)
        session.commit()
        session.refresh(story)
        tasks = list(story.tasks)
        story_id = story.id
    finally:
        session.close()

    assert len(tasks) == 1
    assert tasks[0].title == "Crear formulario"
    assert tasks[0].user_story_id == story_id


def test_story_service_create_and_retrieve(sqlite_db) -> None:
    created = StoryService.create_user_story(sample_user_story_create())

    assert created.id is not None
    assert created.project == "ExpenseApp"

    stories = StoryService.get_all_user_stories()
    assert len(stories) == 1
    assert stories[0].id == created.id

    fetched = StoryService.get_user_story_by_id(created.id)
    assert fetched.id == created.id
    assert fetched.goal == "Registrar gastos"


def test_user_story_to_response_maps_schema(sqlite_db) -> None:
    story = StoryService.create_user_story(sample_user_story_create())

    response = user_story_to_response(story)

    assert isinstance(response, UserStorySchema)
    assert response.id == story.id
    assert response.project == story.project
    assert response.role == story.role
    assert response.priority == story.priority
    assert response.story_points == story.story_points
