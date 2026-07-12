from contextlib import asynccontextmanager
from pathlib import Path
from typing import Any

from fastapi import FastAPI, HTTPException
from fastapi.staticfiles import StaticFiles
from sqlalchemy import text
from src.api.tasks import router as tasks_router
from src.api.ai_tasks import router as ai_tasks_router
from src.api.user_stories import router as user_stories_router
from src.core.config import API_TITLE, API_VERSION, SKIP_RAG_INIT
from src.core import database
from src.rag.rag_manager import RAGManager

engine = database.engine


@asynccontextmanager
async def lifespan(_: FastAPI):
    """Initialize application resources on startup."""
    database.Base.metadata.create_all(bind=database.engine)
    if not SKIP_RAG_INIT:
        RAGManager.initialize()
    yield


app = FastAPI(
    title=API_TITLE,
    version=API_VERSION,
    lifespan=lifespan,
)
static_dir = Path(__file__).resolve().parent.parent / "static"
app.mount("/static", StaticFiles(directory=static_dir), name="static")
app.include_router(tasks_router)
app.include_router(ai_tasks_router)
app.include_router(user_stories_router)


@app.get("/.well-known/appspecific/com.chrome.devtools.json", include_in_schema=False)
def chrome_devtools_manifest() -> dict[str, Any]:
    """Return a small JSON to satisfy Chrome DevTools' appspecific manifest request and avoid 404 logs."""
    # Chrome (and some other tools) sometimes request this path when opening DevTools.
    # Returning an empty JSON with 200 avoids noisy 404 entries in the server log.
    return {}


@app.get("/", include_in_schema=False)
def root() -> dict[str, str]:
    """Return a simple JSON message at the root path.

    Tests expect a JSON body with a "message" key, so return a small
    JSON object instead of redirecting to the UI.
    """
    return {"status": "ok", "message": "Task Manager API is running."}


@app.get("/health")
def health_check() -> dict[str, str]:
    """Return a simple health check response."""
    return {"status": "ok", "message": "Task Manager API is running."}


@app.get("/health/db")
def database_health_check() -> dict[str, str]:
    """Return a database connectivity health check response."""
    try:
        with database.SessionLocal() as session:
            session.execute(text("SELECT 1"))
    except Exception as error:
        raise HTTPException(status_code=503, detail=f"Database connection failed: {type(error).__name__}") from error
    return {"status": "ok", "message": "Database connection is healthy."}
