from dataclasses import dataclass
from typing import Any

from src.models.enums import PriorityEnum, StatusEnum


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
        }

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> "Task":
        """Instantiate a Task from a dictionary representation."""
        return cls(
            id=int(data["id"]),
            title=str(data["title"]),
            description=str(data["description"]),
            priority=PriorityEnum(str(data["priority"])),
            effort_hours=float(data["effort_hours"]),
            status=StatusEnum(str(data["status"])),
            assigned_to=str(data["assigned_to"]),
        )
