from fastapi import HTTPException

from src.ai.exceptions import LLMCallError, LLMNotConfiguredError
from src.managers.ai_task_manager import AIValidationError


def map_ai_error(error: Exception, default_status: int) -> HTTPException:
    """Map AI service exceptions to consistent HTTP JSON errors."""
    if isinstance(error, LLMNotConfiguredError):
        return HTTPException(status_code=503, detail="Azure OpenAI is not configured.")
    if isinstance(error, LLMCallError):
        return HTTPException(status_code=502, detail=str(error))
    if isinstance(error, AIValidationError):
        return HTTPException(status_code=default_status, detail=str(error))
    return HTTPException(status_code=500, detail="Unexpected AI error.")
