# Software Design Document (SDD) - Task Manager + AI (Module 3)

**Project Status**: Phase 1 - Completed ✓
**Framework**: FastAPI | **Persistence**: JSON File | **AI Provider**: Azure OpenAI
**Reference deliverable**: `entregable2.md`

## AI Endpoints Specification

All AI routes live under prefix `/ai/tasks`, method **`POST`**, body = task JSON, response = same task JSON enriched and persisted in `data/tasks.json`. If the request includes an existing `id`, update that stored task. If no `id` is provided, create a new task with the next available ID.

| Endpoint | Preconditions (input) | LLM behaviour | Output field(s) | HTTP errors |
|----------|----------------------|---------------|-----------------|-------------|
| `POST /ai/tasks/describe` | `description` empty; at least `title` set | One call: generate description from other fields | `description` | `400` if description already set; `502` empty LLM text; `503` not configured |
| `POST /ai/tasks/categorize` | `category` empty | One call: classify into allowed categories (Frontend, Backend, Testing, Infra, …) | `category` | `400` if category set; `422` unknown category; `502` / `503` |
| `POST /ai/tasks/estimate` | `effort_hours` empty or 0; `title`, `description`, `category` recommended | One call: return hours as number; parse to **float** | `effort_hours` | `400` if already set; `422` non-numeric parse; `502` / `503` |
| `POST /ai/tasks/audit` | All core fields filled; `risk_analysis` and `risk_mitigation` empty | **Two calls**: (1) risk analysis → (2) mitigation using task + analysis | `risk_analysis`, `risk_mitigation` | `400` if risk fields set; `502` / `503` |

**Shared rules**
- Routes delegate to `AITaskManager`; never call the LLM client directly from `src/api/`.
- Register router in `src/main.py`; keep existing CRUD under `/tasks` unchanged.
- OpenAPI `/docs` must list all four AI endpoints with examples.
- Every current or future endpoint that creates, enriches, or modifies task data must persist the resulting task through `TaskManager`; no endpoint should return task changes that only exist in memory.

## Model generation parameters (`.env`)

Configurable via `.env`, loaded in `src/core/config.py`, applied only through `src/core/completion_params.build_completion_kwargs()`:

| Variable | Purpose |
|----------|---------|
| `AZURE_OPENAI_TEMPERATURE` | Sampling temperature |
| `AZURE_OPENAI_MAX_TOKENS` | Default max output tokens |
| `AZURE_OPENAI_TOP_P` | Nucleus sampling |
| `AZURE_OPENAI_FREQUENCY_PENALTY` | Optional; leave empty to omit |
| `AZURE_OPENAI_PRESENCE_PENALTY` | Optional; leave empty to omit |
| `AZURE_OPENAI_SUPPORTED_PARAMS` | Comma-separated allowlist (e.g. `temperature,max_tokens,top_p`) |

If a parameter is **not** in `AZURE_OPENAI_SUPPORTED_PARAMS`, it is never sent to Azure (even if set in `.env` or passed as a per-call override). Per-call overrides (e.g. higher `max_tokens` for audit) use the same filter. See `ai.instructions.md` for LLM service usage.

## Phase 1: Environment & AI Configuration
- [x] **Step 1.1**: Extend `requirements.txt` with `openai` and `python-dotenv`. ✓
- [x] **Step 1.2**: Create project-root `.env` with Azure connection + generation variables (see table above). ✓
- [x] **Step 1.3**: Extend `src/core/config.py` with `load_dotenv()`, connection constants, generation settings, and `AZURE_OPENAI_SUPPORTED_PARAMS`. ✓
- [x] **Step 1.4**: Implement `src/core/completion_params.py` with `build_completion_kwargs()` to filter unsupported parameters. ✓

## Phase 2: Domain Model Extension
- [x] **Step 2.1**: Add new fields to `Task` in `src/models/task.py`:
    - `category`: `str` or `CategoryEnum` (e.g. Frontend, Backend, Testing, Infra).
    - `risk_analysis`: `str` (long text, default empty).
    - `risk_mitigation`: `str` (long text, default empty).
- [x] **Step 2.2**: Update `to_dict()` and `from_dict()` for the new fields. Handle missing keys in legacy JSON gracefully.
- [x] **Step 2.3**: Create or extend `CategoryEnum` in `src/models/enums.py` and mirror it in Pydantic schemas.
- [x] **Step 2.4**: Update `src/models/schemas.py` with request/response schemas that include all fields. Provide lean schemas for AI endpoints (e.g. task without `description` for describe).

## Phase 3: LLM Service Layer
- [x] **Step 3.1**: Create `src/ai/llm_client.py` with a single responsibility: call the LLM API.
- [x] **Step 3.2**: Implement `complete(system_prompt, user_prompt, **overrides) -> str` using `build_completion_kwargs(**overrides)` for every API call.
- [x] **Step 3.3**: Create `src/ai/prompts.py` with dedicated prompt templates per use case: describe, categorize, estimate, risk_analysis, risk_mitigation.
- [x] **Step 3.4**: Apply prompt engineering: clear role, output format constraints, few-shot examples where helpful, and explicit language (Spanish or English, consistent across endpoints).

## Phase 4: AI Business Logic (Managers)
- [x] **Step 4.1**: Create `src/managers/ai_task_manager.py` to orchestrate LLM calls and map responses back to `Task` fields.
- [x] **Step 4.2**: **`describe`**: Build prompt from `title`, `priority`, `status`, etc.; return task with `description` filled.
- [x] **Step 4.3**: **`categorize`**: Classify into allowed categories (Frontend, Backend, Testing, Infra, …); validate/normalize LLM output against `CategoryEnum`.
- [x] **Step 4.4**: **`estimate`**: Parse LLM output to `float` for `effort_hours`; handle invalid numbers with `HTTPException` 422.
- [x] **Step 4.5**: **`audit`**: Two sequential LLM calls — (1) `risk_analysis` from full task context; (2) `risk_mitigation` using task + `risk_analysis`. Return task with both fields filled.

## Phase 5: AI API Routes
- [x] **Step 5.1**: Create `src/api/ai_tasks.py` with `APIRouter(prefix="/ai/tasks", tags=["AI Tasks"])`.
- [x] **Step 5.2**: Implement the four endpoints per **AI Endpoints Specification** above.
- [x] **Step 5.3**: Register the router in `src/main.py`. Keep existing CRUD routes unchanged under `/tasks`.
- [x] **Step 5.4**: Validate preconditions and map errors per specification table (`400`, `422`, `502`, `503`).

## Phase 6: Quality Assurance & Documentation
- [x] **Step 6.1**: Unit tests for prompt builders and parsers (`effort_hours`, category normalization). ✓
- [x] **Step 6.2**: Integration tests for AI routes with mocked `LLMService` (no real API calls in CI). ✓
- [x] **Step 6.3**: Manual verification with Postman or Swagger (`/docs`): all four AI endpoints + existing CRUD. ✓
- [x] **Step 6.4**: Update `README.md`: new fields table, AI endpoints table, `.env` setup, Azure configuration, and rubric-aligned examples. ✓
- [x] **Step 6.5**: Add Postman collection at `docs/task_manager_postman_collection.json` (excluded from ZIP if credentials present).

## Phase 7: Final Packaging (Entregable 2)
- [x] **Step 7.1**: Verify the endpoints described in `README.md` and `docs/task_manager_postman_collection.json`, correcting any errors. Explain the steps so the user can repeat the tests manually in terminal and Postman. If anything is missing, propose a solution before continuing to step 7.2 and explicitly wait for the user's approval. ✓
- [x] **Step 7.2**: Run full test suite: `pytest`. ✓
- [x] **Step 7.3**: Run `.github/agents/packager.md` / `.github/scripts/package.sh` to generate `m3_proyecto_carmen_garcia-peral.zip` in project root. ✓
- [x] **Step 7.4**: Verify ZIP contains obfuscated `.env`, no `venv`/`__pycache__`, and no plaintext API keys in the archived `.env`. ✓

---
**Current Task**: Entregable 2 complete — maintenance and final cleanup
**AI Instruction**: This file is the source of truth for endpoints and delivery phases. Use `.github/instructions/ai.instructions.md` for LLM client, prompts, and `build_completion_kwargs()`. Do not modify `.github/plans/plan.md` (entregable 1 archive).
