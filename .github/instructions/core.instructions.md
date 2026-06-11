---
applyTo: "src/core/**"
---
# Core Configuration Standards

- **Settings Management**: Use `src/core/config.py` to centralize constants and environment-sensitive values.
- **Constants**: Define global constants here (e.g., `DATA_PATH`, API metadata) to avoid hardcoding in services.
- **Path Handling**: Use `pathlib.Path` to construct file system paths.
- **Security**: Never hardcode API keys in Python. Load Azure settings from the project-root `.env` via `python-dotenv` (`load_dotenv` in `config.py`).
- **`.env.example`**: keep a project-root `.env.example` updated with placeholder values for required environment variables. Do not commit real secrets in `.env`.
- **Editor support and dependencies**: When adding new third-party libraries such as SQLAlchemy, install them into the project `.venv`.
- **Pylance policy**: Never introduce new Pylance diagnostics in generated or edited code. Before committing changes, run editor diagnostics or `get_errors` on all touched Python files and fix every reported issue until zero diagnostics remain.
- **`config.py`**: connection + generation constants, `is_azure_openai_configured()`.
- **`completion_params.py`**: `build_completion_kwargs()` — merges `.env` values and per-call overrides, drops params not in `AZURE_OPENAI_SUPPORTED_PARAMS`.
- **Startup check**: Use `is_azure_openai_configured()` before LLM calls; return HTTP 503 if missing.
