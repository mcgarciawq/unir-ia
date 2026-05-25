---
applyTo: "**/*.py"
---
# Architecture & Clean Code

- **SOLID Principles**: Keep a single responsibility per layer.
- **Layer Separation**: API routes, business logic managers, persistence services, domain models, and **AI/LLM services** must be separate.
- **AI Layer**:
  - `src/api/ai_tasks.py` — HTTP layer for `/ai/tasks/*`
  - `src/managers/ai_task_manager.py` — orchestration and response parsing
  - `src/ai/llm_client.py` — provider client only
  - `src/ai/prompts.py` — prompt templates (no HTTP, no file I/O)
  - `src/core/completion_params.py` — filters generation kwargs via `AZURE_OPENAI_SUPPORTED_PARAMS`
- **FastAPI Best Practices**: Use `APIRouter` for route modularity and Pydantic schemas for request/response validation.
- **Single Source of Truth**: Import global configurations (file paths, API metadata) from `src.core.config` only.
- **Path Handling**: Use `pathlib.Path` for all filesystem paths and avoid manual `os.path` concatenation.
- **DRY Principle**: Do not redefine constants in multiple modules.
- **Documentation**: Use Google Style docstrings and full type hints.
- **Response Consistency**: Every endpoint must return JSON, including error responses.
- **Enum Consistency**: Share `PriorityEnum` and `StatusEnum` between domain model and Pydantic schema layers.
