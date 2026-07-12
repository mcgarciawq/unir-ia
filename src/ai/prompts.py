from src.models.task import Task
from src.models.enums import CategoryEnum, PriorityEnum, StatusEnum
from src.models.user_story import UserStory


def build_user_story_prompt(
    prompt: str,
    context: str = "",
) -> str:
    """Create a prompt for generating a full user story using RAG context."""

    priorities = "\n".join(priority.value for priority in PriorityEnum)

    return f"""
You are a Senior Product Owner.

The following information has been retrieved from the company's internal software engineering knowledge base.

Treat this information as the primary source of guidance when generating the user story.

==============================
Internal Development Guidelines
==============================

{context}

==============================
Instructions
==============================

The knowledge base is written in English.

The user's request may be written in Spanish.

Generate the final response ONLY in Spanish.

While generating the user story:

- Use the retrieved knowledge whenever applicable.
- Apply the internal writing guidelines.
- Follow the INVEST principles.
- Consider acceptance criteria when writing the description.
- Use the estimation guidance for story_points and effort_hours.
- Keep story_points and effort_hours consistent.
- The generated user story should:
  - be clear and concise;
  - follow professional Agile writing practices;
  - be suitable for immediate use in a Scrum backlog;
  - use natural Spanish;
  - avoid unnecessary repetition.

Do not mention or reference the knowledge base.

Return ONLY valid JSON.

The response must be valid JSON that can be parsed directly using json.loads().

The JSON must contain exactly these fields:

project
role
goal
reason
description
priority
story_points
effort_hours

Priority values must be:

{priorities}

Story points must be between 1 and 8.

Do not include explanations.

Do not include markdown.

Do not include comments.

User request:

{prompt}
"""


def build_tasks_from_story_prompt(
    user_story: UserStory,
    task_count: int = 3,
    context: str = "",
) -> str:
    """Create a prompt for generating implementation tasks using RAG context."""

    categories = ", ".join(category.value for category in CategoryEnum)
    priorities = "\n".join(priority.value for priority in PriorityEnum)
    statuses = "\n".join(status.value for status in StatusEnum)

    return f"""
You are a Senior Software Project Manager.

The following information has been retrieved from the company's internal task management knowledge base.

Treat this information as the primary source of guidance when generating the implementation tasks.

==============================
Internal Task Management Guidelines
==============================

{context}

==============================
Instructions
==============================

The knowledge base is written in English.

Generate the final response entirely in Spanish.

Use the retrieved guidance whenever applicable.

Generate exactly {task_count} implementation tasks.

Return ONLY a valid JSON array.

The response must be valid JSON that can be parsed directly using json.loads().

Each task object must contain:

- title
- description
- priority
- effort_hours
- status
- assigned_to
- category

Allowed priorities:

{priorities}

Allowed statuses:

{statuses}

Allowed categories:

{categories}

Each task should:

- represent a single implementation activity;
- have a clear and concise title;
- include a useful implementation description;
- have a realistic effort estimate;
- use exactly one of the allowed categories;
- have a priority consistent with its importance.

Never invent new category names.

Always use one of the allowed categories exactly as provided.

Do not mention or reference the knowledge base.

Do not include explanations.

Do not include markdown.

Do not include comments.

User Story

Project: {user_story.project}
Role: {user_story.role}
Goal: {user_story.goal}
Reason: {user_story.reason}
Description: {user_story.description}
Priority: {user_story.priority.value}
Story points: {user_story.story_points}
Effort hours: {user_story.effort_hours}
"""


def build_describe_prompt(task: Task) -> str:
    """Create a prompt to generate a task description from existing task fields."""
    return (
        "You are an expert project manager. "
        "Generate a concise but informative task description using the information below. "
        "Write only the description; do not add numbering or extra sections.\n\n"
        f"Title: {task.title}\n"
        f"Priority: {task.priority.value}\n"
        f"Status: {task.status.value}\n"
        f"Assigned to: {task.assigned_to}\n"
        f"Effort hours: {task.effort_hours}\n"
        f"Category: {task.category or 'None'}\n"
    )


def build_categorize_prompt(task: Task) -> str:
    """Create a prompt to classify the task into an allowed category."""
    categories = ", ".join(category.value for category in CategoryEnum)
    return (
        "You are a task classifier."
        "Choose the best single category for the task from the list below."
        "Respond with exactly one category label and nothing else.\n\n"
        f"Allowed categories: {categories}\n\n"
        f"Task title: {task.title}\n"
        f"Task description: {task.description or 'No description provided.'}\n"
        f"Priority: {task.priority.value}\n"
        f"Status: {task.status.value}\n"
        f"Assigned to: {task.assigned_to}\n"
        f"Effort hours: {task.effort_hours}\n"
    )


def build_estimate_prompt(task: Task) -> str:
    """Create a prompt to estimate effort hours for a task."""
    return (
        "You are a project estimator."
        "Read the task details below and provide only a single numeric value representing the estimated effort in hours."
        "Do not add text or units.\n\n"
        f"Title: {task.title}\n"
        f"Description: {task.description or 'No description provided.'}\n"
        f"Category: {task.category or 'None'}\n"
        f"Priority: {task.priority.value}\n"
        f"Status: {task.status.value}\n"
        f"Assigned to: {task.assigned_to}\n"
    )


def build_risk_analysis_prompt(task: Task) -> str:
    """Create a prompt to generate risk analysis from a full task context."""
    return (
        "You are a risk analyst."
        "Identify the main technical, schedule and dependency risks for the following task."
        "Write a single concise paragraph.\n\n"
        f"Title: {task.title}\n"
        f"Description: {task.description}\n"
        f"Category: {task.category or 'None'}\n"
        f"Priority: {task.priority.value}\n"
        f"Status: {task.status.value}\n"
        f"Assigned to: {task.assigned_to}\n"
        f"Effort hours: {task.effort_hours}\n"
    )


def build_risk_mitigation_prompt(task: Task, risk_analysis: str) -> str:
    """Create a prompt to generate mitigation actions from an existing risk analysis."""

    return (
        "You are a project risk mitigation specialist. "
        "Suggest practical mitigation actions for the risks described below. "
        "Return plain text only.\n\n"
        f"Task title: {task.title}\n"
        f"Task description: {task.description}\n"
        f"Risk analysis: {risk_analysis}\n"
    )
