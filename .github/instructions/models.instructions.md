---
applyTo: "src/models/**"
---
# Task Entity Technical Specification

Strictly implement the `Task` domain model and shared enums:
- `id`: int (Primary Key)
- `title`: str
- `description`: str (Long text)
- `priority`: `PriorityEnum` (low, medium, high, blocking)
- `effort_hours`: float (Decimal representing estimated hours)
- `status`: `StatusEnum` (pending, in_progress, in_review, completed)
- `assigned_to`: str (Team member name)

## Required Methods
- `to_dict(self) -> dict`: Convert the `Task` instance into a dictionary for JSON serialization.
- `from_dict(cls, data: dict)`: Class method to instantiate a `Task` from a dictionary.

## Validation
- Use Pydantic `BaseModel` schemas in `src/models/schemas.py` for all API request bodies.
- Ensure the `Task` domain model serializes enum values as plain strings in JSON.
