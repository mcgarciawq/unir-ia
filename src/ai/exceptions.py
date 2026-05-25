class LLMServiceError(Exception):
    """Base exception for the LLM service layer."""


class LLMNotConfiguredError(LLMServiceError):
    """Raised when Azure OpenAI is not configured."""


class LLMCallError(LLMServiceError):
    """Raised when the LLM provider returns an error."""
