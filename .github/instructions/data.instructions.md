---
applyTo: "data/**"
---
# Data Storage Standards

- **File Format**: All data must be stored in valid JSON format.
- **File Name**: The primary storage file is `tasks.json`.
- **Persistence Rule**: Do not edit files in this folder manually; all changes must be made via the `TaskManager` service.
- **Git Policy**: This folder's `.json` files are ignored by `.gitignore`, but the directory must contain a `.gitkeep` file to ensure the folder structure is preserved in the repository.
