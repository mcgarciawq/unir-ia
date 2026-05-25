---
applyTo: "tests/**"
---
# Testing Standards

- **Framework**: Use `pytest` for all tests.
- **Naming**: All test files must start with `test_` and all test functions must start with `test_`.
- **Structure**:
    - `tests/unit/`: Test individual functions in `models` and `services`.
    - `tests/integration/`: Test API endpoints using `fastapi.testclient.TestClient`.
- **Mocking**: Mock the file system or the `TaskManager` when testing the API layer to avoid writing real files in `data/` during tests.
- **Monkeypatching**: Use `monkeypatch.setattr` to redirect `src.services.task_manager.DATA_PATH` to a `tmp_path` during service tests.
