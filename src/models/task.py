from dataclasses import dataclass
from typing import Any

from src.models.enums import CategoryEnum, PriorityEnum, StatusEnum


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
        }

    @classmethod
    def from_dict(cls, data: dict):
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

        try:
            category = CategoryEnum(category_raw).value if category_raw else ""
        except ValueError:
            category = CategoryEnum.other.value

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
        )
