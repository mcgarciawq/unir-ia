import re

from src.ai.exceptions import LLMCallError, LLMNotConfiguredError
from src.ai.llm_client import complete
from src.ai.prompts import (
    build_categorize_prompt,
    build_describe_prompt,
    build_estimate_prompt,
    build_risk_analysis_prompt,
    build_risk_mitigation_prompt,
)
from src.models.enums import CategoryEnum
from src.models.task import Task


class AIValidationError(Exception):
    """Raised when AI output cannot be validated or parsed."""


class AITaskManager:
    """Orchestrates AI enrichment operations for task objects."""

    @staticmethod
    def describe(task: Task) -> Task:
        """Fill the task description using the AI service."""
        prompt = build_describe_prompt(task)
        try:
            description = complete(
                system_prompt="You are a task description generator.",
                user_prompt=prompt,
            )
        except LLMNotConfiguredError:
            raise
        except LLMCallError as exc:
            raise exc

        if not description.strip():
            raise AIValidationError("The LLM returned an empty description.")

        task.description = description.strip()
        return task

    @staticmethod
    def categorize(task: Task) -> Task:
        """Classify the task into a configured category."""
        prompt = build_categorize_prompt(task)
        try:
            category_text = complete(
                system_prompt="You are a task category classifier.",
                user_prompt=prompt,
            )
        except LLMNotConfiguredError:
            raise
        except LLMCallError as exc:
            raise exc

        normalized = AITaskManager._normalize_category(category_text)
        if normalized is None:
            raise AIValidationError("The LLM returned an unknown category.")

        task.category = normalized.value
        return task

    @staticmethod
    def estimate(task: Task) -> Task:
        """Estimate effort_hours for the task using AI output."""
        prompt = build_estimate_prompt(task)
        try:
            estimate_text = complete(
                system_prompt="You are a project effort estimator.",
                user_prompt=prompt,
            )
        except LLMNotConfiguredError:
            raise
        except LLMCallError as exc:
            raise exc

        effort_hours = AITaskManager._parse_effort_hours(estimate_text)
        if effort_hours is None:
            raise AIValidationError("The LLM returned a non-numeric effort estimate.")

        task.effort_hours = effort_hours
        return task

    @staticmethod
    def audit(task: Task) -> Task:
        """Generate risk analysis and mitigation based on the task content."""
        try:
            risk_analysis = complete(
                system_prompt="You are a risk analyst.",
                user_prompt=build_risk_analysis_prompt(task),
            )
        except LLMNotConfiguredError:
            raise
        except LLMCallError as exc:
            raise exc

        if not risk_analysis.strip():
            raise AIValidationError("The LLM returned an empty risk analysis.")

        try:
            risk_mitigation = complete(
                system_prompt="You are a risk mitigation specialist.",
                user_prompt=build_risk_mitigation_prompt(task, risk_analysis),
            )
        except LLMNotConfiguredError:
            raise
        except LLMCallError as exc:
            raise exc

        if not risk_mitigation.strip():
            raise AIValidationError("The LLM returned an empty risk mitigation plan.")

        task.risk_analysis = risk_analysis.strip()
        task.risk_mitigation = risk_mitigation.strip()
        return task

    @staticmethod
    def _normalize_category(category_text: str) -> CategoryEnum | None:
        normalized = category_text.strip().lower()
        if not normalized:
            return None

        for category in CategoryEnum:
            if normalized == category.value.lower() or normalized == category.name.lower():
                return category

        return None

    @staticmethod
    def _parse_effort_hours(text: str) -> float | None:
        cleaned = text.strip()
        if not cleaned:
            return None

        match = re.search(r"[-+]?[0-9]*\.?[0-9]+", cleaned)
        if not match:
            return None

        try:
            return float(match.group(0))
        except ValueError:
            return None
