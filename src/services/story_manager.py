from fastapi import HTTPException
from sqlalchemy import select

from src.core.database import SessionLocal
from src.models.user_story import UserStory
from src.models.schemas import UserStoryCreate


class StoryService:
    """Business logic for user story persistence and retrieval."""

    @staticmethod
    def get_all_user_stories() -> list[UserStory]:
        with SessionLocal() as session:
            result = session.execute(select(UserStory)).scalars().all()
            return list(result)

    @staticmethod
    def get_user_story_by_id(user_story_id: int) -> UserStory:
        with SessionLocal() as session:
            user_story = session.get(UserStory, user_story_id)
            if user_story is None:
                raise HTTPException(status_code=404, detail="User story not found")
            return user_story

    @staticmethod
    def create_user_story(story_data: UserStoryCreate) -> UserStory:
        with SessionLocal() as session:
            user_story = UserStory(
                project=story_data.project,
                role=story_data.role,
                goal=story_data.goal,
                reason=story_data.reason,
                description=story_data.description,
                priority=story_data.priority,
                story_points=story_data.story_points,
                effort_hours=story_data.effort_hours,
            )
            session.add(user_story)
            session.commit()
            session.refresh(user_story)
            return user_story

    @staticmethod
    def delete_user_story(user_story_id: int) -> None:
        with SessionLocal() as session:
            user_story = session.get(UserStory, user_story_id)
            if user_story is None:
                raise HTTPException(status_code=404, detail="User story not found")
            session.delete(user_story)
            session.commit()
