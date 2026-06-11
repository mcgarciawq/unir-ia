from __future__ import annotations

import json
import re
from typing import Any, cast

from src.ai.exceptions import LLMCallError, LLMNotConfiguredError
from src.ai.llm_client import complete
from src.ai.prompts import build_tasks_from_story_prompt, build_user_story_prompt
from src.managers.ai_task_manager import AIValidationError
from src.models.enums import CategoryEnum, PriorityEnum, StatusEnum
from src.models.schemas import TaskCreate, UserStoryCreate
from src.models.user_story import UserStory


class AIStoryManager:
    """Orchestrates AI-powered user story and task generation."""

    @staticmethod
    def generate_user_story_from_prompt(prompt: str) -> UserStoryCreate:
        try:
            response = complete(
                system_prompt="You are a product owner who writes clear user stories.",
                user_prompt=build_user_story_prompt(prompt),
            )
        except LLMNotConfiguredError:
            raise
        except LLMCallError as exc:
            raise exc

        payload = AIStoryManager._parse_json_object(response)
        return UserStoryCreate(**payload)

    @staticmethod
    def generate_tasks_for_story(user_story: UserStory, task_count: int = 3) -> list[TaskCreate]:
        try:
            response = complete(
                system_prompt="You are a project manager generating technical tasks from a user story.",
                user_prompt=build_tasks_from_story_prompt(user_story, task_count),
            )
        except LLMNotConfiguredError:
            raise
        except LLMCallError as exc:
            raise exc

        raw_tasks = AIStoryManager._parse_json_array(response)
        task_list: list[TaskCreate] = []

        for task_data in raw_tasks:
            sanitized = AIStoryManager._sanitize_task_payload(task_data)
            task_list.append(TaskCreate(**sanitized))

        return task_list

    @staticmethod
    def _parse_json_object(text: str) -> dict[str, Any]:
        try:
            return json.loads(text)
        except json.JSONDecodeError:
            return AIStoryManager._extract_json_object(text)

    @staticmethod
    def _parse_json_array(text: str) -> list[dict[str, Any]]:
        try:
            loaded = json.loads(text)
            if isinstance(loaded, list):
                return cast(list[dict[str, Any]], loaded)
            raise AIValidationError("The AI response did not contain a JSON array.")
        except json.JSONDecodeError:
            return AIStoryManager._extract_json_array(text)

    @staticmethod
    def _extract_json_object(text: str) -> dict[str, Any]:
        match = re.search(r"\{.*\}", text, re.S)
        if not match:
            raise AIValidationError("Could not find a JSON object in the AI response.")

        try:
            return json.loads(match.group(0))
        except json.JSONDecodeError as exc:
            raise AIValidationError("Failed to parse JSON object from AI response.") from exc

    @staticmethod
    def _extract_json_array(text: str) -> list[dict[str, Any]]:
        match = re.search(r"\[.*\]", text, re.S)
        if not match:
            raise AIValidationError("Could not find a JSON array in the AI response.")

        try:
            loaded = json.loads(match.group(0))
            if isinstance(loaded, list):
                return cast(list[dict[str, Any]], loaded)
            raise AIValidationError("Parsed AI output is not a JSON array.")
        except json.JSONDecodeError as exc:
            raise AIValidationError("Failed to parse JSON array from AI response.") from exc

    @staticmethod
    def _sanitize_task_payload(raw_task: dict[str, Any]) -> dict[str, Any]:
        if "status" not in raw_task:
            raw_task["status"] = StatusEnum.pending.value

        if "priority" not in raw_task:
            raw_task["priority"] = PriorityEnum.medium.value

        raw_task["category"] = AIStoryManager._normalize_category(raw_task.get("category"))

        if "priority" in raw_task and raw_task["priority"] is not None:
            raw_task["priority"] = AIStoryManager._normalize_priority(raw_task["priority"])

        if "assigned_to" not in raw_task or not str(raw_task.get("assigned_to", "")).strip():
            raw_task["assigned_to"] = "Team"

        if "effort_hours" not in raw_task:
            raw_task["effort_hours"] = 1.0

        if "description" not in raw_task:
            raw_task["description"] = "Task generated from user story."

        return raw_task

    @staticmethod
    def _normalize_category(category: Any) -> str:
        if category is None:
            return CategoryEnum.other.value

        normalized = str(category).strip().lower()
        for allowed_category in CategoryEnum:
            if normalized in {allowed_category.value.lower(), allowed_category.name.lower()}:
                return allowed_category.value

        return CategoryEnum.other.value

    @staticmethod
    def _normalize_priority(priority: Any) -> str:
        normalized = str(priority).strip().lower()
        if normalized == "blocker":
            return PriorityEnum.blocking.value

        for allowed_priority in PriorityEnum:
            if normalized in {allowed_priority.value.lower(), allowed_priority.name.lower()}:
                return allowed_priority.value

        return PriorityEnum.medium.value
