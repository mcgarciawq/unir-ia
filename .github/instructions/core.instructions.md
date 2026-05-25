---
applyTo: "src/core/**"
---
# Core Configuration Standards

- **Settings Management**: Use `src/core/config.py` to centralize constants and environment-sensitive values.
- **Constants**: Define global constants here (e.g., `DATA_PATH`, API metadata) to avoid hardcoding in services.
- **Path Handling**: Use `pathlib.Path` to construct file system paths.
- **Security**: Ensure no sensitive data (passwords, keys) is hardcoded; use `.env` placeholders if environment variables are required.
