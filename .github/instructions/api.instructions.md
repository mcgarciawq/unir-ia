---
applyTo: "src/api/**"
---
# API Layer Standards (Controllers)

- **Routing**: Use `APIRouter` to modularize endpoints.
- **Dependency Injection**: Inject `Managers` or `Services` into the endpoints to maintain decoupled logic.
- **Request Validation**: Use Pydantic schemas from `src/models/` for all `POST` and `PUT` bodies.
- **Mandatory Endpoints**:
    - `POST /tasks`: Create task.
    - `GET /tasks`: List all.
    - `GET /tasks/{id}`: Get specific.
    - `PUT /tasks/{id}`: Update task.
    - `DELETE /tasks/{id}`: Delete task.
- **Documentation**: Ensure the app exposes FastAPI's OpenAPI docs for a Swagger UI catalog, available at `/docs` after the server starts.
- **Error Handling**: Always raise `fastapi.HTTPException` with clear JSON details for 400 (Not Found) or 400 (Bad Request) errors.

## AI Endpoints
- **Router**: `src/api/ai_tasks.py`, `prefix="/ai/tasks"`, `tags=["AI Tasks"]`; register in `src/main.py`.
- **Delegation**: Routes call `AITaskManager` only, not the LLM client.
- **Persistence required**: Every endpoint that creates, enriches, or modifies task data must persist the resulting task in `data/tasks.json` via `TaskManager`. If the request includes an existing `id`, update that stored task; otherwise create a new task with the next available ID.
