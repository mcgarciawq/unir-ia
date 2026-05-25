from typing import Optional

from pydantic import BaseModel, ConfigDict, Field

from src.models.enums import PriorityEnum, StatusEnum


class TaskBase(BaseModel):
    title: str
    description: str
    priority: PriorityEnum
    effort_hours: float = Field(..., ge=0)
    status: StatusEnum
    assigned_to: str


class TaskCreate(TaskBase):
    """Schema for creating a new task."""


class TaskUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    priority: Optional[PriorityEnum] = None
    effort_hours: Optional[float] = Field(None, ge=0)
    status: Optional[StatusEnum] = None
    assigned_to: Optional[str] = None


class TaskResponse(TaskBase):
    id: int

    model_config = ConfigDict(from_attributes=True)
