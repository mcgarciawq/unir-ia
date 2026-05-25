from src.models.task import Task
from src.models.enums import CategoryEnum


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
    categories = ", ".join([c.value for c in CategoryEnum])
    return (
        "You are a task classifier. Choose the best single category for the task from the list below. "
        "Respond with exactly one category label and nothing else.\n\n"
        f"Allowed categories: {categories}.\n\n"
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
        "You are a project estimator. Read the task details below and provide only a single numeric value "
        "representing the estimated effort in hours. Do not add text or units.\n\n"
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
        "You are a risk analyst. Identify the main risks for this task and write a short risk analysis. "
        "Focus on technical, schedule, and dependency risks. Provide one paragraph.\n\n"
        f"Title: {task.title}\n"
        f"Description: {task.description}\n"
        f"Category: {task.category or 'None'}\n"
        f"Priority: {task.priority.value}\n"
        f"Status: {task.status.value}\n"
        f"Assigned to: {task.assigned_to}\n"
        f"Effort hours: {task.effort_hours}\n"
    )


def build_risk_mitigation_prompt(task: Task, risk_analysis: str) -> str:
    """Create a prompt to generate risk mitigation steps based on the risk analysis."""
    return (
        "You are a project risk mitigation specialist. Suggest clear mitigation actions for the risks described below. "
        "Return a concise plan with bullet-style sentences if appropriate, but keep the response as plain text only.\n\n"
        f"Task title: {task.title}\n"
        f"Task description: {task.description}\n"
        f"Risk analysis: {risk_analysis}\n"
    )
