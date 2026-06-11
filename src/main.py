from contextlib import asynccontextmanager
from pathlib import Path
from typing import Any

from fastapi import FastAPI
from fastapi.responses import RedirectResponse
from fastapi.staticfiles import StaticFiles
from src.api.tasks import router as tasks_router
from src.api.ai_tasks import router as ai_tasks_router
from src.api.user_stories import router as user_stories_router
from src.core.config import API_TITLE, API_VERSION
from src.core.database import Base, engine


@asynccontextmanager
async def lifespan(_: FastAPI):
    """Create database tables on application startup."""
    Base.metadata.create_all(bind=engine)
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
def root() -> RedirectResponse:
    """Redirect the root path to the user stories interface."""
    return RedirectResponse(url="/user-stories")


@app.get("/health")
def health_check() -> dict[str, str]:
    """Return a simple health check response."""
    return {"status": "ok", "message": "Task Manager API is running."}
