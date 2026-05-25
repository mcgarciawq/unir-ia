from pathlib import Path
from dotenv import load_dotenv
import os

# Load environment variables from .env (if present)
load_dotenv()

# Base directory of the project (three levels up from this file)
BASE_DIR: Path = Path(__file__).resolve().parent.parent.parent
DATA_PATH: Path = BASE_DIR / "data" / "tasks.json"

API_TITLE: str = "Task Manager API"
API_VERSION: str = "1.0.0"


# Azure OpenAI Configuration
AZURE_OPENAI_API_KEY: str | None = os.getenv("AZURE_OPENAI_API_KEY")
AZURE_OPENAI_API_VERSION: str = os.getenv("AZURE_OPENAI_API_VERSION", "2024-02-15-preview")
AZURE_OPENAI_ENDPOINT: str | None = os.getenv("AZURE_OPENAI_ENDPOINT")
AZURE_OPENAI_DEPLOYMENT_NAME: str | None = os.getenv("AZURE_OPENAI_DEPLOYMENT_NAME")


# Helper to parse optional floats from environment variables
def _opt_float(value: str | None) -> float | None:
    if value is None or value == "":
        return None
    try:
        return float(value)
    except (TypeError, ValueError):
        return None


# Generation Parameters (with safer parsing and typing)
AZURE_OPENAI_TEMPERATURE: float = float(os.getenv("AZURE_OPENAI_TEMPERATURE", "0.7"))
AZURE_OPENAI_MAX_TOKENS: int = int(os.getenv("AZURE_OPENAI_MAX_TOKENS", "2048"))
AZURE_OPENAI_TOP_P: float = float(os.getenv("AZURE_OPENAI_TOP_P", "0.9"))
AZURE_OPENAI_FREQUENCY_PENALTY: float | None = _opt_float(os.getenv("AZURE_OPENAI_FREQUENCY_PENALTY"))
AZURE_OPENAI_PRESENCE_PENALTY: float | None = _opt_float(os.getenv("AZURE_OPENAI_PRESENCE_PENALTY"))

# Supported params as a list for easier checking in code
_supported_params_raw: str = os.getenv(
    "AZURE_OPENAI_SUPPORTED_PARAMS",
    "temperature,max_tokens,top_p",
)
AZURE_OPENAI_SUPPORTED_PARAMS: list[str] = [p.strip() for p in _supported_params_raw.split(",") if p.strip()]


def is_azure_openai_configured() -> bool:
    """
    Check if all required Azure OpenAI settings are configured.

    Returns:
        bool: True if API key, endpoint, and deployment name are set.
    """
    return bool(
        AZURE_OPENAI_API_KEY
        and AZURE_OPENAI_ENDPOINT
        and AZURE_OPENAI_DEPLOYMENT_NAME
    )
