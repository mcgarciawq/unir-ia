---
applyTo: "**/*.py"
---
# Architecture & Clean Code

- **SOLID Principles**: Keep a single responsibility per layer.
- **Layer Separation**: API routes, business logic managers, persistence services, and domain models must be separate.
- **FastAPI Best Practices**: Use `APIRouter` for route modularity and Pydantic schemas for request/response validation.
- **Single Source of Truth**: Import global configurations (file paths, API metadata) from `src.core.config` only.
- **Path Handling**: Use `pathlib.Path` for all filesystem paths and avoid manual `os.path` concatenation.
- **DRY Principle**: Do not redefine constants in multiple modules.
- **Documentation**: Use Google Style docstrings and full type hints.
- **Response Consistency**: Every endpoint must return JSON, including error responses.
- **Enum Consistency**: Share `PriorityEnum` and `StatusEnum` between domain model and Pydantic schema layers.
