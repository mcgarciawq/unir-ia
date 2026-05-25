# Master AI Protocol: FastAPI & SOLID Project

## 🤖 Interaction, Protocol & Memory
- **Reference Document**: Always consult `.github/plans/plan.md` to know the current state and next step.
- **Strict Flow**: You MUST NOT proceed to a new step without explicit user validation ("OK").
- **Auto-Update**: Every time the user validates a step, your first action must be to update `.github/plans/plan.md`, marking the task as completed [x] and updating the "Project Status" section.

## 🛠️ Global Standards
- **Language**: 100% English for code, comments, and documentation.
- **Framework**: Use FastAPI.
- **Standards**: PEP 8, Google Style Docstrings, Type Hinting and SOLID principles.
- **Context**: Use specific rules in `.github/instructions/` depending on the file path.

## ⚠️ Submission & Compliance Rules
- **Naming Convention**: The final output must be structured to generate `m2_proyecto_nombre_apellido.zip`.
- **Data Integrity**: All fields (id, title, description, priority, effort_hours, status, assigned_to) must be strictly present in the `Task` class.
- **Response Consistency**: Every endpoint must return a JSON, even in case of error (e.g., `{"detail": "Task not found"}`).
- **Static Logic**: Ensure `TaskManager` uses strictly static methods for JSON persistence.

## 📂 Contextual Intelligence
- **Instruction Priority**: Before writing code in any directory, you MUST read the corresponding file in `.github/instructions/` (e.g., `api.instructions.md` for `src/api/`).
- **Cross-Layer Integrity**: Ensure that changes in `src/models/` are reflected in `src/api/` schemas and `src/services/` serialization logic.

## 🤖 Specialized Agents
- **Packager Agent**: Located in `.github/agents/packager.md`. Invoke this agent to generate the final ZIP deliverable in the root directory.