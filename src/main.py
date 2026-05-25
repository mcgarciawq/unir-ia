from fastapi import FastAPI
from src.api.tasks import router as tasks_router
from src.api.ai_tasks import router as ai_tasks_router
from src.core.config import API_TITLE, API_VERSION

app = FastAPI(
    title=API_TITLE,
    version=API_VERSION
)
app.include_router(tasks_router)
app.include_router(ai_tasks_router)


@app.get("/health")
def health_check() -> dict[str, str]:
    """Return a simple health check response."""
    return {"status": "ok", "message": "Task Manager API is running."}
