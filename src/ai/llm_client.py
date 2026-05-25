from typing import Any

from openai import AzureOpenAI

from src.core import config
from src.core.completion_params import build_completion_kwargs
from src.ai.exceptions import LLMCallError, LLMNotConfiguredError


def complete(system_prompt: str, user_prompt: str, **overrides: Any) -> str:
    """Call Azure OpenAI chat completion and return the assistant response."""

    if not config.is_azure_openai_configured():
        raise LLMNotConfiguredError("Azure OpenAI is not fully configured.")

    assert config.AZURE_OPENAI_API_KEY is not None
    assert config.AZURE_OPENAI_ENDPOINT is not None
    assert config.AZURE_OPENAI_DEPLOYMENT_NAME is not None
    assert config.AZURE_OPENAI_API_VERSION is not None

    client = AzureOpenAI(
        api_key=config.AZURE_OPENAI_API_KEY,
        azure_endpoint=config.AZURE_OPENAI_ENDPOINT,
        api_version=config.AZURE_OPENAI_API_VERSION,
    )

    # Build safe kwargs (already filtered)
    kwargs: dict[str, Any] = build_completion_kwargs(**overrides)

    # Keep messages untyped to avoid SDK strict typing issues
    messages = [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": user_prompt},
    ]

    try:
        model = str(config.AZURE_OPENAI_DEPLOYMENT_NAME)

        call_kwargs = {
            "model": model,
            "messages": messages,
        }

        response = client.chat.completions.create(**call_kwargs, **kwargs)

    except Exception as error:
        raise LLMCallError("Azure OpenAI request failed.") from error

    try:
        content = response.choices[0].message.content

        if content is None:
            raise LLMCallError("Empty response content from Azure OpenAI.")

        result = content.strip()

    except (AttributeError, IndexError, KeyError, TypeError) as error:
        raise LLMCallError("Invalid response format from Azure OpenAI.") from error

    if not result:
        raise LLMCallError("Azure OpenAI returned an empty response.")

    return result
