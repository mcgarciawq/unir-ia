# Master AI Protocol: FastAPI & SOLID Project

## 🤖 Interaction, Protocol & Memory
- **Active plan (entregable 2)**: Always consult `.github/plans/plan-2.md` for current state and next step.
- **Archived plan (entregable 1)**: `.github/plans/plan.md` is read-only reference for the completed CRUD baseline. Do not edit it.
- **Deliverable spec**: Read `entregable2.md` for rubric-aligned requirements (four AI endpoints, new Task fields).
- **Strict Flow**: You MUST NOT proceed to a new step without explicit user validation 
("OK").
- **Auto-Update**: AEvery time the user validates a step, your first action must be to 
update `.github/plans/plan-2.md`, marking the task as completed [x] and updating the "Project Status" section.

## 🛠️ Global Standards
- **Language**: 100% English for code, comments, and documentation (prompts to the LLM may be Spanish).
- **Framework**: FastAPI.
- **Standards**: PEP 8, Google Style Docstrings, Type Hinting, and SOLID principles.
- **Context**: Use rules in `.github/instructions/` by file path; for LLM code use `ai.instructions.md`.
- **Postman Coverage**: Every new API endpoint should also be added to `docs/task_manager_postman_collection.json` so manual API tests stay current.
- **Error Clearance**: Before marking a step complete, run editor diagnostics and/or `get_errors` on touched files and resolve all Pylance/type issues so the workspace reports no errors.

## ⚠️ Submission & Compliance Rules
- **Naming Convention**: The final output must be structured to generate `m3_proyecto_nombre_apellido.zip`.
- **CRUD preserved**: Existing endpoints must keep working after model extension (backward-compatible JSON loading).
- **Secrets**: Use a single project-root `.env` for Azure credentials (see `core.instructions.md`). The submission ZIP **includes** `.env` with obfuscated `API_KEY` / `SECRET` / `TOKEN` values via `package.sh`. Never hardcode keys in `.py` files.
- **Response consistency**: Every endpoint returns JSON, including errors (`{"detail": "..."}`).
- **Static persistence**: `TaskManager` keeps strictly static methods for JSON I/O.
- **Endpoint persistence**: Any endpoint that creates, enriches, or changes task data must persist the resulting task in `data/tasks.json` through `TaskManager`; endpoints must not return task changes that only exist in memory.

## 📂 Contextual Intelligence
- **Instruction Priority**: Before writing code in any directory, you MUST read the orresponding file in `.github/instructions/` (e.g. `api.instructions.md` → `src/api/`, `ai.instructions.md` → LLM layer).
- **Cross-Layer Integrity**: Ensure that changes in `src/models/` are reflected in `src/api/` schemas, `to_dict`/`from_dict`, managers,  API routers and `src/services/` serialization logic.
- **AI vs CRUD**: LLM logic must not live in CRUD routes or `TaskManager`; use dedicated AI service + manager + router.

## 🤖 Specialized Agents
- **Packager Agent**: Located in `.github/agents/packager.md`. Invoke this agent to generate the final ZIP deliverable in the root directory.
