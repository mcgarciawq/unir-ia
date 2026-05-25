from pydantic import BaseModel, ConfigDict, Field

from src.models.enums import CategoryEnum, PriorityEnum, StatusEnum


class TaskBase(BaseModel):
    title: str
    description: str
    priority: PriorityEnum
    effort_hours: float = Field(..., ge=0)
    status: StatusEnum
    assigned_to: str
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
    category: CategoryEnum | None = None
    risk_analysis: str | None = None
    risk_mitigation: str | None = None


class TaskResponse(TaskBase):
    id: int

    model_config = ConfigDict(from_attributes=True)


class AITaskPayload(BaseModel):
    id: int | None = None
    title: str
    description: str | None = None
    priority: PriorityEnum
    effort_hours: float | None = None
    status: StatusEnum
    assigned_to: str
    category: CategoryEnum | None = None
    risk_analysis: str | None = None
    risk_mitigation: str | None = None


class AITaskResponse(AITaskPayload):
    model_config = ConfigDict(from_attributes=True)
