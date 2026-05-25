---
applyTo: "src/services/**"
---
# Services Layer: Persistence & TaskManager

This layer is responsible for low-level data operations and communication with the storage system.

## 🛠️ TaskManager Implementation
- **Class Name**: `TaskManager`.
- **Mandatory Pattern**: Use strictly **static methods** (`@staticmethod`) for all operations.
- **Storage**: Must interact with `data/tasks.json` and use `DATA_PATH` from `src.core.config`.

## ⚙️ Required Methods
- **`load_tasks()`**: 
    - Purpose: Read the JSON file and return a list of `Task` objects.
    - Logic: Must instantiate `Task` objects from raw dictionary data using `Task.from_dict()`.
- **`save_tasks(tasks: list[Task])`**: 
    - Purpose: Persist the current state to disk.
    - Logic: Must serialize the list of `Task` objects into JSON and overwrite `data/tasks.json`.

## 🛡️ Reliability
- **File Handling**: If `tasks.json` is missing or corrupted, `load_tasks` must return an empty list `[]` instead of crashing.
- **Independence**: This service must not contain API logic or Pydantic schemas; it only handles the `Task` domain model.
- **Directory Safety**: Ensure the `data/` directory exists before writing the JSON file.
