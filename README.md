# Task Manager API

A FastAPI task manager with MySQL persistence, CRUD task operations, AI-assisted user story generation, and a Bootstrap UI served as static HTML with JavaScript.

## Project structure

- `src/main.py` - FastAPI application entry point.
- `src/api/` - API router and endpoints.
- `src/models/` - Domain model and Pydantic schemas.
- `src/services/` - Persistence services using SQLAlchemy and MySQL.
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

### Build image

```bash
docker build -t unir-ia .
```

### Run container

```bash
docker run -p 8000:8000 --env-file .env unir-ia
```

The application will be available at:
http://localhost:8000/user-stories
http://localhost:8000/docs

## Azure Container Registry

The project is configured to publish the Docker image automatically to Azure Container Registry (ACR) using GitHub Actions.

Container Registry: uniria.azurecr.io

The publication process is fully automated after every push to the `main` branch.

## Continuous Integration

The repository includes a GitHub Actions workflow that automatically:

- Checks out the source code.
- Installs Python 3.13.
- Installs project dependencies.
- Executes all automated tests using pytest.
- Builds the Docker image.
- Publishes the image to Azure Container Registry.

The Docker image is only published if all tests complete successfully.

## GitHub Secrets

Sensitive information is never stored in the repository.

The pipeline uses GitHub Secrets to authenticate against Azure Container Registry.

Required secrets:

- ACR_LOGIN_SERVER
- ACR_USERNAME
- ACR_PASSWORD


##CI/CD Architecture

```text
Developer
    │
git push
    │
    ▼
GitHub Actions
    │
    ├── Install dependencies
    ├── Build Docker image
    ├── Execute tests
    └── Push image to Azure Container Registry
```

## Quick start

1. Create and activate the virtual environment.
2. Install dependencies with `pip install -r requirements.txt`.
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

## Database (MySQL) configuration

The project supports a MySQL backend via SQLAlchemy. Copy `.env.example` to `.env` and update the MySQL values for your local environment.

A recommended configuration is:

```ini
MYSQL_HOST=localhost
MYSQL_PORT=3306
MYSQL_USER=task_manager
MYSQL_PASSWORD=mi_password
MYSQL_DATABASE=task_manager
SQLALCHEMY_ECHO=false
```

If you prefer to use `root`, set `MYSQL_USER=root` and `MYSQL_PASSWORD=<your-root-password>`.

The connection URI is assembled in `src/core/config.py` as `SQLALCHEMY_DATABASE_URI`.

### Create the database and tables

1. Create the database in MySQL:

```bash
mysql -u root -p -e "CREATE DATABASE IF NOT EXISTS task_manager CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;"
```

2. (Recommended) Create a dedicated MySQL user for the project:

```bash
mysql -u root -p -e "CREATE USER IF NOT EXISTS 'task_manager'@'localhost' IDENTIFIED BY 'mi_password'; GRANT ALL PRIVILEGES ON task_manager.* TO 'task_manager'@'localhost'; FLUSH PRIVILEGES;"
```

3. Create the required tables from the project root:

```bash
.venv/bin/python - <<'PY'
from src.core.database import engine, Base
import src.models.user_story
import src.models.task

Base.metadata.create_all(bind=engine)
print('Tables created successfully.')
PY
```

If your virtual environment is already active, `python - <<'PY'` also works.

### Troubleshooting

- `Access denied` means the MySQL user/password in `.env` are incorrect for the configured host.
- `Table 'task_manager.user_stories' doesn't exist` means the database exists but the SQLAlchemy tables were not created yet.
- Use the table creation command above to create `user_stories` and `tasks`.

If you prefer migrations, integrate Alembic and generate migrations against `src/core/database.py`.

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

User stories and tasks are stored in the configured MySQL database through SQLAlchemy models.

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
- **Unit tests** (`tests/unit/`): Test models, schemas, services, and AI managers
- **Integration tests** (`tests/integration/`): Test API endpoints with mocking

**Note:** The `tests/conftest.py` file automatically configures Python's path for pytest, so tests can import from the `src` module without additional configuration.

## Notes

- `TaskManager` uses SQLAlchemy/MySQL for application persistence.
- `Task` implements `to_dict()` and `from_dict()` to bridge domain objects and API schemas.
- The API layer is implemented with `APIRouter` and Pydantic request validation.

## Troubleshooting

**Problem:** `ModuleNotFoundError: No module named 'src'` when running tests
- **Solution:** Make sure you're running pytest from the project root directory where `tests/` folder is located. The `tests/conftest.py` file will automatically configure the Python path.

**Problem:** Port 8000 already in use
- **Solution:** Use a different port: `python -m uvicorn src.main:app --port 8001`

**Problem:** Virtual environment not activating
- **Solution:** Ensure you're using the correct Python version and the `.venv` folder exists in the project root.
