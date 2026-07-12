# Task Manager API

A FastAPI task manager with Azure SQL persistence (or MySQL fallback), CRUD task operations, AI-assisted user story generation, and a Bootstrap UI served as static HTML with JavaScript.

## Project structure

- `src/main.py` - FastAPI application entry point.
- `src/api/` - API router and endpoints.
- `src/models/` - Domain model and Pydantic schemas.
- `src/services/` - Persistence services using SQLAlchemy and Azure SQL (with MySQL fallback).
- `src/managers/` - Business logic layer connecting API routes and services.
- `src/core/` - Core utilities and shared configuration.
- `static/` - Bootstrap UI (`user-stories.html`, `tasks.html`, CSS and JavaScript).
- `tests/` - Unit and integration tests.

## Installation

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

## Docker

### Using Docker Compose (Recommended)

**Build the image:**
```bash
docker-compose build
```

**Initialize database tables (run once after first build):**
```bash
docker-compose run --rm uniria python init_db.py
```

**Run the application:**
```bash
docker-compose up
```

The application will be available at:
- UI: http://localhost:8000/user-stories
- API Docs: http://localhost:8000/docs

**Stop the container:**
```bash
docker-compose down
```

## Azure Container Registry

The project is configured to publish the Docker image automatically to Azure Container Registry (ACR) using GitHub Actions.

Container Registry: uniria.azurecr.io

The publication process is fully automated after every push to the `main` branch.
Each image is published with two tags: `latest` and the Git commit SHA. Azure Container Apps is deployed with the SHA tag so every deployment can be traced back to the exact source revision.

## Continuous Integration

The repository includes a GitHub Actions workflow that automatically:

- Checks out the source code.
- Installs Python 3.13.
- Installs development dependencies from `requirements-dev.txt`.
- Executes all automated tests using pytest.
- Builds the Docker image.
- Starts the built Docker image and validates `GET /health` before publishing it.
- Publishes the image to Azure Container Registry.
- Deploys the image tagged with the commit SHA to Azure Container Apps.
- Validates the deployed application with smoke tests against `/health`, `/health/db`, `/tasks/`, and `/user-stories/json`.

The Docker image is only published if all tests complete successfully and the container starts correctly. The final runtime image installs `requirements.txt`; test tools such as pytest and httpx are kept in `requirements-dev.txt`.

## GitHub Secrets

Sensitive information is never stored in the repository.

The pipeline uses GitHub Secrets to authenticate against Azure, publish to Azure Container Registry, and deploy the Azure Container App.

Required GitHub Secrets for the workflow:

- RESOURCE_GROUP
- CONTAINER_APP_NAME
- ACR_LOGIN_SERVER
- ACR_USERNAME
- ACR_PASSWORD
- IMAGE_REPOSITORY
- AZURE_SUBSCRIPTION_ID
- AZURE_BEARER_TOKEN
- AZURE_SQL_CONNECTION_STRING
- AZURE_OPENAI_API_KEY
- AZURE_OPENAI_ENDPOINT
- AZURE_OPENAI_DEPLOYMENT_NAME

Optional GitHub Secrets for the app runtime:

- AZURE_OPENAI_API_VERSION (defaults to `2024-02-15-preview` in the workflow)
- AZURE_OPENAI_MAX_TOKENS (defaults to `2048` in the app)
- AZURE_OPENAI_TEMPERATURE (defaults to `0.7` in the app)
- AZURE_OPENAI_TOP_P (defaults to `0.9` in the app)
- AZURE_OPENAI_SUPPORTED_PARAMS (useful for deployments that require `max_completion_tokens`)

Azure Container App secrets are created or updated by the workflow from these GitHub Secrets. The deployment metadata secrets (`RESOURCE_GROUP`, `CONTAINER_APP_NAME`, `IMAGE_REPOSITORY`, `AZURE_SUBSCRIPTION_ID`, and `AZURE_BEARER_TOKEN`) are needed only in GitHub Actions, not inside the running app.

## CI/CD Architecture

```text
Developer
    │
git push
    │
    ▼
GitHub Actions
    │
    ├── Validate required secrets
    ├── Install dependencies
    ├── Execute pytest
    ├── Build Docker image
    ├── Smoke test local container (/health)
    ├── Push image to Azure Container Registry
    ├── Deploy commit-SHA image to Azure Container Apps
    └── Validate deployed endpoints
```

## Quick start

1. Create and activate the virtual environment.
2. Install dependencies with `pip install -r requirements-dev.txt` for local development and testing. Use `requirements.txt` for runtime-only installations.
3. Copy `.env.example` to `.env` and fill in the required values.
4. The compiled stylesheet is already available at `static/css/style.css`, so you can start the app directly.

   If you want to edit SCSS and recompile it, use Dart Sass (recommended). The Python "sass" package may not be compatible with newer Python versions (for example Python 3.13). Dart Sass is distributed as a standalone executable and via npm — choose the option that fits your platform.

   Installation options:

   - Using npm (requires Node.js):
     ```bash
     # install globally
     npm install -g sass
     # or run without installing globally
     npx sass static/scss/style.scss static/css/style.css --no-source-map
     ```

   - Using Homebrew on macOS:
     ```bash
     brew tap sass/sass
     # if Dart is required, also tap and install dart-lang/dart
     brew tap dart-lang/dart
     brew install dart
     brew install sass
     ```

   Compile SCSS to CSS:
   ```bash
   sass static/scss/style.scss static/css/style.css --no-source-map
   ```

   Optional: watch for changes during development:
   ```bash
   sass --watch static/scss:static/css --no-source-map
   ```

   Verify the installation:
   ```bash
   sass --version
   ```

5. Start the application with:

```bash
python -m uvicorn src.main:app --reload
```

6. Open the browser at:

- `http://127.0.0.1:8000/user-stories` for the UI
- `http://127.0.0.1:8000/docs` for the API docs

## Azure OpenAI Configuration

Edit `.env.example` and rename to `.env` file in the project root with the following values:

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

## Database configuration

The project supports **Azure SQL** as primary database, with **MySQL as fallback**. The database choice is determined by priority in `src/core/config.py`:

1. **Azure SQL** (if `AZURE_SQL_CONNECTION_STRING` is set in `.env`)
2. **DATABASE_URL** (if set)
3. **MySQL** (default fallback)

### Azure SQL Configuration (Recommended)

Set the `AZURE_SQL_CONNECTION_STRING` in `.env`:

```ini
AZURE_SQL_CONNECTION_STRING=Driver={ODBC Driver 18 for SQL Server};Server=tcp:your-server.database.windows.net,1433;Database=your-db;Uid=your-user;Pwd=your-password;Encrypt=yes;TrustServerCertificate=no;Connection Timeout=30;
```

**Requirements:**
- ODBC Driver 18 for SQL Server installed on your system
- Azure SQL Database created and accessible

### MySQL Configuration (Fallback)

If `AZURE_SQL_CONNECTION_STRING` is not set, the application uses these MySQL environment variables:

```ini
MYSQL_HOST=localhost
MYSQL_PORT=3306
MYSQL_USER=task_manager
MYSQL_PASSWORD=mi_password
MYSQL_DATABASE=task_manager
```

**Docker deployment:**
When deployed in Docker (Linux), the application connects to Azure SQL perfectly via pyodbc.

### Cloud persistence and runtime secrets

In Azure Container Apps, the application is stateless: the container can be restarted or replaced at any time. Persistent data is stored outside the container in the configured relational database.

- In cloud deployments, the workflow injects `AZURE_SQL_CONNECTION_STRING` as an Azure Container App secret, so user stories and tasks are stored in Azure SQL.
- Data survives container restarts because it is persisted in Azure SQL, not in the container filesystem.
- Azure OpenAI credentials are also injected as Container App secrets: `AZURE_OPENAI_API_KEY`, `AZURE_OPENAI_ENDPOINT`, and `AZURE_OPENAI_DEPLOYMENT_NAME`.
- Optional generation settings such as `AZURE_OPENAI_API_VERSION`, `AZURE_OPENAI_MAX_TOKENS`, `AZURE_OPENAI_TEMPERATURE`, `AZURE_OPENAI_TOP_P`, and `AZURE_OPENAI_SUPPORTED_PARAMS` can be configured through GitHub Secrets.
- Without Azure OpenAI credentials, health checks and database-backed read/write endpoints can still be tested, but AI generation endpoints return a configuration error.

The deployment workflow validates both the basic application health and the database-backed story listing endpoint after each Azure Container Apps deployment.

Once connected to your database, create the required tables:

```bash
.venv/bin/python - <<'PY'
from src.core.database import engine, Base
import src.models.user_story
import src.models.task

Base.metadata.create_all(bind=engine)
print('Tables created successfully.')
PY
```

## Run

```bash
python -m uvicorn src.main:app --reload
```

Then open the UI at:

`http://127.0.0.1:8000/user-stories`

The root path also redirects to the user stories interface.

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
| GET | `/user-stories` | Serve the user stories HTML page (`static/user-stories.html`). |
| GET | `/user-stories/json` | Return all user stories as JSON. |
| GET | `/user-stories/{id}` | Return a single user story as JSON. |
| DELETE | `/user-stories/{id}` | Delete a user story and its associated tasks. |
| POST | `/user-stories` | Generate a `UserStory` from a prompt and persist it. |
| POST | `/user-stories/{id}/generate-tasks` | Generate tasks for a story via AI and persist them. |
| GET | `/user-stories/{id}/tasks` | Serve the tasks HTML page (`static/tasks.html`). |
| GET | `/user-stories/{id}/tasks/json` | Return tasks for a user story as JSON. |

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

Task IDs are generated by the database, so do not assume the next task will be `1`. Use an existing ID from `GET /tasks/` or capture the `id` returned by `POST /tasks/` before calling `GET`, `PUT`, or `DELETE`.

AI endpoints also persist their enriched task results. If the request includes an existing `id`, the stored task is updated. If no `id` is provided, a new task is created with the next available ID.

## Persistence

User stories and tasks are stored in the configured database (Azure SQL or MySQL) through SQLAlchemy models.

## Tests

Run all tests with:

```bash
pip install -r requirements-dev.txt
pytest tests
```

Or with verbose output:

```bash
pytest tests -v
```

The project includes:
- **Unit tests** (`tests/unit/`): Test models, schemas, services, and AI managers
- **Integration tests** (`tests/integration/`): Test API endpoints with mocking

**Note:** The `tests/conftest.py` file automatically configures Python's path for pytest, so tests can import from the `src` module without additional configuration.

## Notes

- `TaskManager` uses SQLAlchemy with Azure SQL or MySQL for application persistence.
- `Task` implements `to_dict()` and `from_dict()` to bridge domain objects and API schemas.
- The API layer is implemented with `APIRouter` and Pydantic request validation.

## Troubleshooting

**Problem:** `ModuleNotFoundError: No module named 'src'` when running tests
- **Solution:** Make sure you're running pytest from the project root directory where `tests/` folder is located. The `tests/conftest.py` file will automatically configure the Python path.

**Problem:** Port 8000 already in use
- **Solution:** Use a different port: `python -m uvicorn src.main:app --port 8001`

**Problem:** Virtual environment not activating
- **Solution:** Ensure you're using the correct Python version and the `.venv` folder exists in the project root.

**Problem:** `pyodbc` timeout when connecting to Azure SQL on macOS
- **Cause:** pyodbc has known issues with SQL Server connections on macOS
- **Solution for testing:** Use `sqlcmd` to verify connectivity:
  ```bash
  sqlcmd -S uniria.database.windows.net -U sqladmin -P 'Root1234' -d unirIA -Q "SELECT @@version"
  ```
- **Solution for production:** Docker/Linux deployments work perfectly with pyodbc. No issues in containerized environments.
- **Workaround for local development:** Keep JSON persistence in `.env` (remove `AZURE_SQL_CONNECTION_STRING`) during development, then switch to Azure SQL when deploying.
