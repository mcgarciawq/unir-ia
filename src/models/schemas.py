from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field

from src.models.enums import CategoryEnum, PriorityEnum, StatusEnum


class UserStoryBase(BaseModel):
    project: str
    role: str
    goal: str
    reason: str
    description: str
    priority: PriorityEnum
    story_points: int = Field(..., ge=1, le=8)
    effort_hours: float = Field(..., ge=0)


class UserStoryCreate(UserStoryBase):
    """Schema for creating a new user story."""


class UserStoryResponse(UserStoryBase):
    id: int
    created_at: datetime | None = None

    model_config = ConfigDict(from_attributes=True)


class UserStorySchema(UserStoryResponse):
    """Schema for returning a user story."""


class UserStorySchemas(BaseModel):
    user_stories: list[UserStorySchema]


class TaskBase(BaseModel):
    title: str
    description: str
    priority: PriorityEnum
    effort_hours: float = Field(..., ge=0)
    status: StatusEnum
    assigned_to: str
    user_story_id: int | None = None
    category: CategoryEnum | None = None
    risk_analysis: str = ""
    risk_mitigation: str = ""


class TaskCreate(TaskBase):
    """Schema for creating a new task."""


class TaskUpdate(BaseModel):
    title: str | None = None
    description: str | None = None
    priority: PriorityEnum | None = None
    effort_hours: float | None = Field(None, ge=0)
    status: StatusEnum | None = None
    assigned_to: str | None = None
    user_story_id: int | None = None
    category: CategoryEnum | None = None
    risk_analysis: str | None = None
    risk_mitigation: str | None = None


class TaskSchema(TaskBase):
    """Schema for returning a task."""

    id: int
    created_at: datetime | None = None

    model_config = ConfigDict(from_attributes=True)


class TaskSchemas(BaseModel):
    tasks: list[TaskSchema]


TaskResponse = TaskSchema


class AITaskPayload(BaseModel):
    id: int | None = None
    title: str
    description: str | None = None
    priority: PriorityEnum
    effort_hours: float | None = None
    status: StatusEnum
    assigned_to: str
    user_story_id: int | None = None
    category: CategoryEnum | None = None
    risk_analysis: str | None = None
    risk_mitigation: str | None = None


class AITaskResponse(AITaskPayload):
    created_at: datetime | None = None

    model_config = ConfigDict(from_attributes=True)
