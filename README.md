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

## Azure OpenAI Configuration

Edit `src/.env` file in the project root with the following values:

```ini
AZURE_OPENAI_API_KEY=your-api-key-here
AZURE_OPENAI_API_VERSION=2024-02-15-preview
AZURE_OPENAI_ENDPOINT=https://your-resource.openai.azure.com/
AZURE_OPENAI_DEPLOYMENT_NAME=your-deployment-name
AZURE_OPENAI_TEMPERATURE=0.7
AZURE_OPENAI_MAX_TOKENS=2048
AZURE_OPENAI_TOP_P=0.9
AZURE_OPENAI_FREQUENCY_PENALTY=
AZURE_OPENAI_PRESENCE_PENALTY=
AZURE_OPENAI_SUPPORTED_PARAMS=
```

The application loads these values automatically from `.env` when it starts.
Leave `AZURE_OPENAI_SUPPORTED_PARAMS` empty for models that reject optional generation parameters such as `temperature`, `top_p`, or `max_tokens`.

## Run

```bash
python -m uvicorn src.main:app --reload
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
| POST | `/ai/tasks/describe` | Generate or enrich task description and persist the task. |
| POST | `/ai/tasks/categorize` | Classify task category and persist the task. |
| POST | `/ai/tasks/estimate` | Estimate `effort_hours` and persist the task. |
| POST | `/ai/tasks/audit` | Generate `risk_analysis` and `risk_mitigation` and persist the task. |

## Task payload

Use this body for `POST /tasks/` and optional fields for `PUT /tasks/{id}`:

```json
{
  "title": "Design API",
  "description": "Create the CRUD endpoints for the task manager.",
  "priority": "high",
  "effort_hours": 3.5,
  "status": "pending",
  "assigned_to": "Product Team",
  "category": "Backend",
  "risk_analysis": "",
  "risk_mitigation": ""
}
```

For manual curl tests, keep the trailing slash in collection endpoints:

```bash
curl -s http://127.0.0.1:8000/tasks/
```

Task IDs are generated from the current contents of `data/tasks.json`, so do not assume the next task will be `1`. Use an existing ID from `GET /tasks/` or capture the `id` returned by `POST /tasks/` before calling `GET`, `PUT`, or `DELETE`.

AI endpoints also persist their enriched task results. If the request includes an existing `id`, the stored task is updated. If no `id` is provided, a new task is created with the next available ID.

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
- **Solution:** Use a different port: `python -m uvicorn src.main:app --port 8001`

**Problem:** Virtual environment not activating
- **Solution:** Ensure you're using the correct Python version and the `.venv` folder exists in the project root.
