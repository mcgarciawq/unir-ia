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
- **Error Handling**: Always raise `fastapi.HTTPException` with clear JSON details for 404 (Not Found) or 400 (Bad Request) errors.
