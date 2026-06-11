# Prompt: Entregable 3 — Setup Phase 1

Read and execute **Phase 1** of `.github/plans/plan-3.md`.

1. Create or update project-root `.env` with MySQL connection variables and any AI configuration values required.
2. Extend `src/core/config.py` to load `.env` and expose the database URI plus SQLAlchemy configuration constants.
3. Add SQLAlchemy engine/session setup in a new module such as `src/core/database.py` or equivalent.
4. Create `src/models/user_story.py` and update `src/models/task.py` with SQLAlchemy models and columns for the new deliverable.
5. Ensure `created_at` fields are auto-generated at the database level.

Follow all instructions in `.github/instructions/`.
Do **not** modify `.github/plans/plan-1.md` or `.github/plans/plan-2.md`. Update progress only in `.github/plans/plan-3.md` after each validated step.
Stop after Phase 1 and wait for user OK before continuing to the next steps in `.github/plans/plan-3.md`.