---
applyTo: "src/models/**"
---
# Task Entity Technical Specification

Strictly implement the `Task` domain model and shared enums:
- `id`: int (Primary Key)
- `title`: str
- `description`: str (Long text; may be empty before `/ai/tasks/describe`)
- `priority`: `PriorityEnum` (low, medium, high, blocking)
- `effort_hours`: float (estimated hours; may be 0 before `/ai/tasks/estimate`)
- `status`: `StatusEnum` (pending, in_progress, blocked, in_review, completed)
- `assigned_to`: str (Team member name)
- `category`: `str` or `CategoryEnum` (e.g. Frontend, Backend, Testing, Infra; empty before `/ai/tasks/categorize`)
- `risk_analysis`: str (long text; empty until `/ai/tasks/audit`)
- `risk_mitigation`: str (long text; empty until `/ai/tasks/audit`)

## Enums
- Add `CategoryEnum` in `src/models/enums.py` with at least: `frontend`, `backend`, `testing`, `infra` (extend if needed).
- Share `PriorityEnum`, `StatusEnum`, and `CategoryEnum` between domain model and Pydantic schemas.

## Required Methods
- `to_dict(self) -> dict`: Convert the `Task` instance into a dictionary for JSON serialization.
- `from_dict(cls, data: dict)`: Class method to instantiate a `Task` from a dictionary.
- **Backward compatibility**: If `category`, `risk_analysis`, or `risk_mitigation` are missing in legacy `tasks.json`, default to `""` (empty string).

## Validation
- Use Pydantic `BaseModel` schemas in `src/models/schemas.py` for CRUD and AI request bodies and all API request bodies.
- Provide optional-field or dedicated schemas for AI endpoints (e.g. `TaskDescribeRequest` without required `description`).
- Ensure enum values serialize as plain strings in JSON.
