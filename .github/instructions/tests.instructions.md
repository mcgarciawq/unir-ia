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

## AI Endpoint Tests
- **No live LLM calls**: Always mock `LLMService.complete` (or `AITaskManager` methods) in integration tests.
- **Coverage targets**:
  - `describe` / `categorize` / `audit`: assert response JSON contains filled fields.
  - Invalid LLM output → expect `422` or `502` per `ai.instructions.md`.
- **Fixtures**: Sample task dicts with empty `description`, `category`, or risk fields as required per endpoint.
- **Optional**: `tests/unit/test_prompts.py` for prompt string content; `tests/unit/test_parsers.py` for effort/category normalization.
- **Required**: `tests/unit/test_completion_params.py` — verify `AZURE_OPENAI_SUPPORTED_PARAMS` filtering.
