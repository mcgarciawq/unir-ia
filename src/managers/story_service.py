from src.models.schemas import UserStoryCreate
from src.models.user_story import UserStory
from src.services.story_manager import StoryService as StoryPersistenceService


class StoryService:
    """Business logic coordinator between API routes and story persistence."""

    @staticmethod
    def get_all_user_stories() -> list[UserStory]:
        return StoryPersistenceService.get_all_user_stories()

    @staticmethod
    def get_user_story_by_id(user_story_id: int) -> UserStory:
        return StoryPersistenceService.get_user_story_by_id(user_story_id)

    @staticmethod
    def create_user_story(story_data: UserStoryCreate) -> UserStory:
        return StoryPersistenceService.create_user_story(story_data)

    @staticmethod
    def delete_user_story(user_story_id: int) -> None:
        StoryPersistenceService.delete_user_story(user_story_id)
