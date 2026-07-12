from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime
from typing import Any, TYPE_CHECKING

from sqlalchemy import DateTime, Enum as SQLEnum, Float, ForeignKey, Integer, String, Text, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.core.database import Base
from src.models.enums import CategoryEnum, PriorityEnum, StatusEnum

if TYPE_CHECKING:
    from src.models.user_story import UserStory


class TaskORM(Base):
    """SQLAlchemy model representing a task persisted to MySQL."""

    __tablename__ = "tasks"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    title: Mapped[str] = mapped_column(String(256), nullable=False)
    description: Mapped[str] = mapped_column(Text, nullable=False)
    priority: Mapped[PriorityEnum] = mapped_column(
        SQLEnum(PriorityEnum, name="task_priority_enum", native_enum=False),
        nullable=False,
        default=PriorityEnum.medium,
    )
    effort_hours: Mapped[float] = mapped_column(Float, nullable=False)
    status: Mapped[StatusEnum] = mapped_column(
        SQLEnum(StatusEnum, name="task_status_enum", native_enum=False),
        nullable=False,
        default=StatusEnum.pending,
    )
    assigned_to: Mapped[str] = mapped_column(String(128), nullable=False)
    category: Mapped[str | None] = mapped_column(String(64), nullable=True)
    risk_analysis: Mapped[str] = mapped_column(Text, nullable=False, default="")
    risk_mitigation: Mapped[str] = mapped_column(Text, nullable=False, default="")
    user_story_id: Mapped[int | None] = mapped_column(Integer, ForeignKey("user_stories.id"), nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now(), nullable=False)

    user_story: Mapped["UserStory"] = relationship("UserStory", back_populates="tasks")


@dataclass
class Task:
    """Domain model representing a task in the task manager."""

    id: int
    title: str
    description: str
    priority: PriorityEnum
    effort_hours: float
    status: StatusEnum
    assigned_to: str
    category: str = ""
    risk_analysis: str = ""
    risk_mitigation: str = ""
    user_story_id: int | None = None
    created_at: str | None = None

    def to_dict(self) -> dict[str, Any]:
        """Convert the Task instance into a dictionary for JSON serialization."""
        return {
            "id": self.id,
            "title": self.title,
            "description": self.description,
            "priority": self.priority.value,
            "effort_hours": self.effort_hours,
            "status": self.status.value,
            "assigned_to": self.assigned_to,
            "category": self.category or None,
            "risk_analysis": self.risk_analysis,
            "risk_mitigation": self.risk_mitigation,
            "user_story_id": self.user_story_id,
            "created_at": self.created_at,
        }

    @staticmethod
    def _normalize_category(category_raw: Any) -> str:
        if not category_raw:
            return ""

        normalized = str(category_raw).strip()
        lowered = normalized.lower()
        for allowed_category in CategoryEnum:
            if lowered in {allowed_category.value.lower(), allowed_category.name.lower()}:
                return allowed_category.value

        return CategoryEnum.other.value

    @classmethod
    def from_dict(cls, data: dict[str, Any]):
        priority_raw = data.get("priority", "medium")
        status_raw = data.get("status", "pending")
        category_raw = data.get("category", "")

        try:
            priority = PriorityEnum(priority_raw)
        except ValueError:
            priority = PriorityEnum.medium

        try:
            status = StatusEnum(status_raw)
        except ValueError:
            status = StatusEnum.pending

        category = cls._normalize_category(category_raw)

        return cls(
            id=data["id"],
            title=data["title"],
            description=data["description"],
            priority=priority,
            effort_hours=data["effort_hours"],
            status=status,
            assigned_to=data["assigned_to"],
            category=category,
            risk_analysis=data.get("risk_analysis", ""),
            risk_mitigation=data.get("risk_mitigation", ""),
            user_story_id=data.get("user_story_id"),
            created_at=data.get("created_at"),
        )
