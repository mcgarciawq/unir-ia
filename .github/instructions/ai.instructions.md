---
applyTo: "src/ai/**,src/managers/ai_task_manager.py,src/api/ai_tasks.py,src/core/completion_params.py"
---
# AI / LLM Layer Standards (Entregable 2)

**Endpoint contracts, preconditions, and HTTP status codes** are defined in `.github/plans/plan-2.md` (section *AI Endpoints Specification*). This file covers LLM implementation only.

## Architecture
- **Separation**: LLM HTTP calls live in `src/ai/llm_client.py`. Prompt text in `src/ai/prompts.py`. Orchestration in `src/managers/ai_task_manager.py`. HTTP in `src/api/ai_tasks.py`.
- **Persistence boundary**: LLM and manager code return enriched task objects only. API routes are responsible for persisting every successful task enrichment to `data/tasks.json` through `TaskManager`.
- **Provider**: Azure OpenAI via official `openai` SDK (`AzureOpenAI`) and `AZURE_OPENAI_*` from `src/core/config.py`.

## Configuration
- Import connection and generation settings from `src.core.config` — do not call `os.getenv` in the AI layer.
- **Every** `chat.completions.create` call must spread kwargs from `build_completion_kwargs()` in `src/core/completion_params.py`.
- Submission ZIP includes obfuscated `.env` (see `package.sh`).

## Generation parameters
- Defaults come from `.env` (`AZURE_OPENAI_TEMPERATURE`, `MAX_TOKENS`, `TOP_P`, penalties).
- **Allowlist**: `AZURE_OPENAI_SUPPORTED_PARAMS` lists which kwargs the deployment accepts. Parameters not in the allowlist are **never** sent, even from `.env` or per-call overrides.
- Per-call overrides: `complete(..., max_tokens=2048)` — useful for audit; filtered by the allowlist.
- Leave a `.env` value empty or `none` to omit that parameter entirely.

```python
from src.core.completion_params import build_completion_kwargs

kwargs = build_completion_kwargs(max_tokens=2048)
client.chat.completions.create(
    model=AZURE_OPENAI_DEPLOYMENT_NAME,
    messages=[...],
    **kwargs,
)
```

## LLM client
- Entry point: `complete(system_prompt: str, user_prompt: str, **overrides) -> str`.
- Always use `build_completion_kwargs(**overrides)` before the API call.
- Wrap provider exceptions; map to HTTP 502/503 in the API layer.
- Do not catch and retry by stripping parameters at runtime — configuration via `AZURE_OPENAI_SUPPORTED_PARAMS` is the supported approach.

## Prompt engineering
- One template per use case: describe, categorize, estimate, risk_analysis, risk_mitigation.
- Structured output: plain text or minimal format (single number, single category label).
- Audit: two sequential calls — analysis first, then mitigation including `risk_analysis`.
- Consistent language across prompts; document choice in `README.md`.

## Response parsing (manager layer)
- **effort_hours**: parse to `float`; `422` on failure.
- **category**: normalize to `CategoryEnum`; `422` if unrecognizable.
- **description / risk fields**: trim; `502` if empty LLM response.

## Testing
- Mock `complete()` in integration tests; no real API calls in `pytest`.
- Unit-test `build_completion_kwargs()` filtering (`tests/unit/test_completion_params.py`).
- Unit-test parsers separately.
