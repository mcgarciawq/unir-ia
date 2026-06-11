from __future__ import annotations

from datetime import datetime
from sqlalchemy import DateTime, Enum as SQLEnum, Float, Integer, String, Text, func
from sqlalchemy.orm import Mapped, mapped_column, relationship
from typing import TYPE_CHECKING

from src.core.database import Base
from src.models.enums import PriorityEnum

if TYPE_CHECKING:
    from src.models.task import TaskORM


class UserStory(Base):
    """SQLAlchemy model representing a user story."""

    __tablename__ = "user_stories"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    project: Mapped[str] = mapped_column(String(128), nullable=False)
    role: Mapped[str] = mapped_column(String(128), nullable=False)
    goal: Mapped[str] = mapped_column(Text, nullable=False)
    reason: Mapped[str] = mapped_column(Text, nullable=False)
    description: Mapped[str] = mapped_column(Text, nullable=False)
    priority: Mapped[PriorityEnum] = mapped_column(
        SQLEnum(PriorityEnum, name="user_story_priority_enum", native_enum=False),
        nullable=False,
        default=PriorityEnum.medium,
    )
    story_points: Mapped[int] = mapped_column(Integer, nullable=False)
    effort_hours: Mapped[float] = mapped_column(Float, nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now(), nullable=False)

    tasks: Mapped[list["TaskORM"]] = relationship("TaskORM", back_populates="user_story", cascade="all, delete-orphan")
