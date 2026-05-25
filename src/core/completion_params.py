"""
Completion parameters builder for Azure OpenAI API calls.

This module filters generation parameters based on the allowlist defined in
`AZURE_OPENAI_SUPPORTED_PARAMS` to ensure only supported parameters are sent
to the Azure OpenAI API.
"""

from src.core import config


def build_completion_kwargs(**overrides: float | int | None) -> dict[str, float | int]:
    """
    Build completion API keyword arguments with support filtering.

    Merges default parameters from `.env` with per-call overrides, then filters
    based on the `AZURE_OPENAI_SUPPORTED_PARAMS` allowlist. Parameters not in
    the allowlist are never sent to Azure, even if set in `.env` or overrides.
    Empty or None values are omitted.

    Args:
        **overrides: Per-call parameter overrides (e.g., max_tokens=2048).
                     Keys must match parameter names without 'AZURE_OPENAI_' prefix.

    Returns:
        Dict: Filtered kwargs ready for `chat.completions.create(**kwargs)`.

    Example:
        >>> kwargs = build_completion_kwargs(max_tokens=2048)
        >>> # kwargs will contain only supported parameters with non-empty values
    """
    # Build the allowlist of supported parameters.
    raw = config.AZURE_OPENAI_SUPPORTED_PARAMS

    if isinstance(raw, str):
        supported_params = {
            p.strip().lower()
            for p in raw.split(",")
            if p.strip()
        }
    else:
        supported_params = {
            str(p).strip().lower()
            for p in raw
            if p
        }
    # Map config names to parameter names (remove 'AZURE_OPENAI_' prefix and lowercase)
    param_map: dict[str, float | int | None] = {
        "temperature": config.AZURE_OPENAI_TEMPERATURE,
        "max_tokens": config.AZURE_OPENAI_MAX_TOKENS,
        "top_p": config.AZURE_OPENAI_TOP_P,
        "frequency_penalty": config.AZURE_OPENAI_FREQUENCY_PENALTY,
        "presence_penalty": config.AZURE_OPENAI_PRESENCE_PENALTY,
    }

    # Start with config defaults
    kwargs: dict[str, float | int] = {}
    for param_name, param_value in param_map.items():
        # Check if parameter is supported
        if param_name.lower() not in supported_params:
            continue

        # Skip empty or None values
        if param_value is None or (isinstance(param_value, str) and not param_value.strip()):
            continue

        kwargs[param_name] = param_value

    # Apply per-call overrides (filtered by allowlist)
    for override_name, override_value in overrides.items():
        param_key = override_name.lower()

        # Skip if not in supported params
        if param_key not in supported_params:
            continue

        # Skip if override is None or empty
        if override_value is None or (isinstance(override_value, str) and not override_value.strip()):
            continue

        kwargs[param_key] = override_value

    return kwargs
