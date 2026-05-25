---
applyTo: "src/managers/**"
---
# Business Logic & Coordination (Managers)

- **Role**: Act as an intermediary between the FastAPI routes and the `TaskManager` service.
- **Responsibility**: 
    - Handle complex business rules that don't belong in the raw data model or the persistence layer.
    - Orchestrate calls to `TaskManager` methods (load/save).
- **Rules**:
    - **No Direct I/O**: Managers must NEVER read or write directly to `tasks.json`. They must call `TaskManager.load_tasks()` or `TaskManager.save_tasks()`.
    - **Task Processing**: Before saving, the Manager should ensure the `Task` object is valid according to the interface (id, title, priority, etc.).
    - **State Management**: Manage the "in-memory" list of tasks during a request lifecycle before committing changes via the Service.

## AI Task Manager
- **File**: `src/managers/ai_task_manager.py` (class name e.g. `AITaskManager`).
- **Role**: Orchestrate LLM calls for describe, categorize, estimate, and audit; map raw LLM text to `Task` fields.
- **Dependencies**: Inject or import `LLMService` and prompt builders — no direct `openai` calls in managers if a service exists.
- **Audit**: Implement as two sequential `complete()` calls; pass `risk_analysis` from call 1 into the prompt for call 2.
- **Parsing**: Numeric and enum parsing belongs here (or in dedicated parser helpers), not in API routes.
- **No file I/O**: Same rule as CRUD managers — do not read/write `tasks.json` directly.
