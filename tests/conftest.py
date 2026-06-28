import sys
from pathlib import Path

# Add the project root to Python path so pytest can find src module
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from unittest.mock import patch

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import Session, sessionmaker
from sqlalchemy.pool import StaticPool

from src.core.database import Base
from src.main import app
from src.models.enums import PriorityEnum
from src.models.schemas import UserStoryCreate
from src.models.user_story import UserStory


def sample_user_story_create() -> UserStoryCreate:
    return UserStoryCreate(
        project="ExpenseApp",
        role="Usuario",
        goal="Registrar gastos",
        reason="Llevar control financiero",
        description="Como usuario quiero poder registrar mis gastos",
        priority=PriorityEnum.medium,
        story_points=3,
        effort_hours=4.0,
    )


def persist_user_story(session: Session, **overrides: object) -> UserStory:
    data = sample_user_story_create().model_dump()
    data.update(overrides)
    story = UserStory(**data)
    session.add(story)
    session.commit()
    session.refresh(story)
    return story


@pytest.fixture
def sqlite_db():
    """Provide an isolated in-memory SQLite database for story and task persistence tests."""
    engine = create_engine(
        "sqlite:///:memory:",
        connect_args={"check_same_thread": False},
        poolclass=StaticPool,
        future=True,
    )
    Base.metadata.create_all(bind=engine)
    session_factory = sessionmaker(bind=engine, autoflush=False, autocommit=False, future=True)

    with (
        patch("src.core.database.SessionLocal", session_factory),
        patch("src.core.database.engine", engine),
        patch("src.main.engine", engine),
        patch("src.services.story_manager.SessionLocal", session_factory),
        patch("src.services.task_manager.SessionLocal", session_factory),
    ):
        yield session_factory

    Base.metadata.drop_all(bind=engine)


@pytest.fixture
def api_client():
    """HTTP client with app lifespan bound to the isolated SQLite database."""
    with TestClient(app) as test_client:
        yield test_client
