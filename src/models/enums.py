from enum import Enum


class PriorityEnum(str, Enum):
    """Allowed priority values for a task."""

    low = "low"
    medium = "medium"
    high = "high"
    blocking = "blocking"


class StatusEnum(str, Enum):
    """Allowed status values for a task."""

    pending = "pending"
    in_progress = "in_progress"
    blocked = "blocked"
    in_review = "in_review"
    completed = "completed"


class CategoryEnum(str, Enum):
    """Allowed category values for a task."""

    frontend = "Frontend"
    backend = "Backend"
    testing = "Testing"
    infra = "Infra"
    research = "Research"
    design = "Design"
    documentation = "Documentation"
    other = "Other"
