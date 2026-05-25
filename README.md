# Task Manager API

A FastAPI task manager with JSON persistence and CRUD task operations.

## Project structure

- `src/main.py` - FastAPI application entry point.
- `src/api/` - API router and endpoints.
- `src/models/` - Domain model and Pydantic schemas.
- `src/services/` - Persistence service using `data/tasks.json`.
- `src/managers/` - Business logic layer connecting API routes and services.
- `src/core/` - Core utilities and shared configuration.
- `data/` - JSON storage for persisted tasks.
- `tests/` - Unit and integration tests.

## Installation

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

## Run

```bash
uvicorn src.main:app --reload
```

## API documentation

After the server starts, open the Swagger UI catalog at:

`http://127.0.0.1:8000/docs`

This page shows the available endpoints, request schemas, response schemas, and allows you to test the API interactively.

## Health check

`GET /health`

Returns a simple API status response with JSON body:

```json
{
  "status": "ok",
  "message": "Task Manager API is running."
}
```

## API Endpoints

| Method | Path | Description |
| --- | --- | --- |
| GET | `/health` | Returns API status. |
| GET | `/tasks/` | Returns all tasks. |
| POST | `/tasks/` | Creates a new task. |
| GET | `/tasks/{id}` | Returns task by ID. |
| PUT | `/tasks/{id}` | Updates an existing task. |
| DELETE | `/tasks/{id}` | Deletes a task. |

## Task payload

Use this body for `POST /tasks/` and optional fields for `PUT /tasks/{id}`:

```json
{
  "title": "Design API",
  "description": "Create the CRUD endpoints for the task manager.",
  "priority": "high",
  "effort_hours": 3.5,
  "status": "pending",
  "assigned_to": "Product Team"
}
```

## Persistence

Tasks are stored in `data/tasks.json` as a JSON array. The project ensures the service returns an empty list if the file is missing or invalid.

## Tests

Run all tests with:

```bash
pytest tests
```

Or with verbose output:

```bash
pytest tests -v
```

The project includes:
- **Unit tests** (`tests/unit/`): Test Task model and TaskManager persistence
- **Integration tests** (`tests/integration/`): Test API endpoints with mocking

**Note:** The `tests/conftest.py` file automatically configures Python's path for pytest, so tests can import from the `src` module without additional configuration.

## Notes

- `TaskManager` uses static methods for JSON persistence.
- `Task` implements `to_dict()` and `from_dict()` for serialization.
- The API layer is implemented with `APIRouter` and Pydantic request validation.

## Troubleshooting

**Problem:** `ModuleNotFoundError: No module named 'src'` when running tests
- **Solution:** Make sure you're running pytest from the project root directory where `tests/` folder is located. The `tests/conftest.py` file will automatically configure the Python path.

**Problem:** Port 8000 already in use
- **Solution:** Use a different port: `uvicorn src.main:app --port 8001`

**Problem:** Virtual environment not activating
- **Solution:** Ensure you're using the correct Python version and the `.venv` folder exists in the project root.
