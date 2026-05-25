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
    