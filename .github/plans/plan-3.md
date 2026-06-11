# Software Design Document (SDD) - User Stories + Tasks UI (Module 4)

**Project Status**: Implementation — Phase 5 complete
**Framework**: FastAPI | **Persistence**: MySQL + SQLAlchemy | **UI**: Static Bootstrap HTML + JavaScript
**Reference deliverable**: `docs/deliverables/deliverable3.md`

## Objective
Deliver a FastAPI application that stores user stories and tasks in MySQL, exposes HTML views for user stories and tasks, and supports AI-assisted generation of user stories and tasks.

## Requirements Summary
- MySQL connection and SQLAlchemy models for `UserStory` and `Task`
- Pydantic schemas for `UserStorySchema`, `UserStorySchemas`, `TaskSchema`, `TaskSchemas`
- UI endpoints and templates:
  - `GET /user-stories` → list user stories + prompt form
  - `POST /user-stories` → create user story from prompt
  - `POST /user-stories/{id}/generate-tasks` → generate associated tasks
  - `GET /user-stories/{id}/tasks` → display tasks for a story
- Persist all generated entities in `data/tasks.json` only for backward compatibility if existing routes remain, but new DB-backed entities must use MySQL.

## Phase 1: Database & Configuration
- [x] Add project-root `.env` with MySQL connection variables and any AI configuration variables required.
- [x] Extend `src/core/config.py` to load `.env` and expose database URI constants.
- [x] Add SQLAlchemy engine/session setup, ideally in a new module such as `src/core/database.py` or equivalent.
- [x] Create `src/models/user_story.py` and extend `src/models/task.py` with SQLAlchemy models and columns described in the deliverable.
- [x] Ensure `created_at` fields are auto-generated at the database level.

## Phase 2: Pydantic Schemas and Persistence
- [x] Create/extend `src/models/schemas.py` with `UserStorySchema`, `UserStorySchemas`, `TaskSchema`, `TaskSchemas`.
- [x] Add CRUD support for user stories and tasks in the service layer (`src/services/task_manager.py` and/or a new `src/services/story_manager.py`).
- [x] Keep compatibility with existing JSON-based storage by preserving `TaskManager` static JSON load/save if current API still depends on it.

## Phase 3: UI Endpoints & Static Pages
- [x] Create HTML pages under `static/`:
  - `user-stories.html` with story list, prompt textarea, and `Generate tasks` buttons
  - `tasks.html` with task list for a given user story
- [x] Implement route handlers in `src/api/user_stories.py` for:
  - `GET /user-stories`
  - `POST /user-stories`
  - `POST /user-stories/{id}/generate-tasks`
  - `GET /user-stories/{id}/tasks`
- [x] Serve UI pages with `FileResponse` and load data via JSON endpoints + JavaScript.
- [x] Keep API routes returning JSON; HTML pages are served as static files as required by the deliverable.

## Phase 4: AI Story and Task Generation
- [x] Extend AI prompt logic in `src/ai/prompts.py` and `src/managers/ai_task_manager.py` to support:
  - generating a complete `UserStory` from a single prompt
  - generating multiple `Task` objects from an existing `UserStory`
- [x] Ensure generated entities are persisted in MySQL and linked with the correct `user_story_id`.
- [x] If needed, keep an abstraction layer so the same AI manager can support both JSON and DB-backed tasks/stories.

## Phase 5: Integration, Routing and Documentation
- [x] Register new UI routes and any new managers in `src/main.py`.
- [x] Add or update `docs/task_manager_postman_collection.json` with the new endpoints listed in `deliverable3.md`.
- [x] Update `README.md` with:
  - MySQL setup instructions
  - new `GET`/`POST` routes
  - HTML UI usage notes
  - database migration/initialization guidance if applicable

## Phase 6: Testing and Validation
- [x] Write tests for new story and task generation flows (added a basic integration test `tests/integration/test_user_stories.py`).
  - `GET /user-stories` renders stories
  - `POST /user-stories` persists a generated story
  - `POST /user-stories/{id}/generate-tasks` persists tasks linked to the story
  - `GET /user-stories/{id}/tasks` shows created tasks
- [x] Use a test database or SQLite in-memory DB for route tests to avoid depending on production MySQL (tests run with `DATABASE_URL="sqlite+pysqlite:///:memory:"`).
- [x] Run static diagnostics and `get_errors` for touched files.


## Delivery Checklist
- [x] Ensure the final project structure is ready for packaging as `m4_proyecto_carmen_garcia-peral.zip`.
- [x] Verify no hardcoded secrets exist in Python source files.
- [x] Confirm `data/tasks.json` remains compatible if legacy endpoints are preserved.
- [x] Validate the final UI works end-to-end with MySQL persistence.

---
**Current Task**: Create a roadmap to implement the Deliverable 3 scope and keep the project aligned with the existing FastAPI architecture.
