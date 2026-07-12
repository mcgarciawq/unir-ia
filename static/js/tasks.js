function getStoryIdFromPath() {
  const match = window.location.pathname.match(/\/user-stories\/(\d+)\/tasks/);
  return match ? Number(match[1]) : null;
}

function setText(id, value) {
  const element = document.getElementById(id);
  if (element) element.textContent = value;
}

function renderTasks(tasks) {
  const list = document.getElementById("tasks-list");
  const empty = document.getElementById("tasks-empty");
  const header = document.getElementById("tasks-header");
  const count = document.getElementById("tasks-count");

  if (!tasks.length) {
    header.classList.add("d-none");
    list.innerHTML = "";
    empty.classList.remove("d-none");
    return;
  }

  header.classList.remove("d-none");
  empty.classList.add("d-none");
  count.textContent = `${tasks.length} tarea(s)`;

  list.innerHTML = tasks
    .map(
      (task) => `
      <div class="col-md-6">
        <div class="card h-100 border-0 shadow-sm">
          <div class="card-body">
            <div class="d-flex justify-content-between align-items-start gap-2 mb-2">
              <div>
                <h3 class="h6 fw-bold mb-1">${task.title}</h3>
                <span class="badge text-bg-light text-muted border">${task.category || "General"}</span>
              </div>
              <span class="badge text-bg-success">${task.status}</span>
            </div>
            <p class="card-text text-muted small mb-3">${task.description}</p>
            <div class="d-flex flex-wrap gap-2 mb-3">
              <span class="badge text-bg-primary">Prioridad: ${task.priority}</span>
              <span class="badge text-bg-secondary">Esfuerzo: ${task.effort_hours} h</span>
              <span class="badge text-bg-light text-dark border">
                <i class="bi bi-person me-1"></i>${task.assigned_to || "Sin asignar"}
              </span>
            </div>
            <button
              type="button"
              class="btn btn-outline-danger btn-sm"
              data-delete-task-id="${task.id}"
            >
              <i class="bi bi-trash me-1"></i>Eliminar tarea
            </button>
          </div>
        </div>
      </div>
    `
    )
    .join("");
}

function showPageError(message) {
  const container = document.getElementById("page-error");
  container.classList.remove("d-none");
  container.innerHTML = `
    <div class="alert alert-danger d-flex align-items-center" role="alert">
      <i class="bi bi-exclamation-triangle-fill me-2"></i>
      <div>${message}</div>
    </div>
  `;
}

function clearPageError() {
  const container = document.getElementById("page-error");
  container.classList.add("d-none");
  container.innerHTML = "";
}

function formatApiError(detail) {
  if (!detail) return "No se pudieron generar las tareas.";
  if (typeof detail === "string") return detail;
  if (Array.isArray(detail)) {
    return detail.map((item) => item.msg || String(item)).join(", ");
  }
  return String(detail);
}

function setButtonLoading(button, isLoading, label) {
  if (!button) return;
  button.disabled = isLoading;
  if (isLoading && button.dataset.defaultLabel) {
    button.innerHTML = `<span class="spinner-border spinner-border-sm me-1"></span>${label}`;
  } else if (!isLoading && button.dataset.defaultLabel) {
    button.innerHTML = button.dataset.defaultLabel;
  }
}

function setPageLoading(isLoading, label = "Procesando...") {
  const overlay = document.getElementById("task-loading-overlay");
  if (overlay) {
    const labelElement = overlay.querySelector(".loading-text");
    if (labelElement) {
      labelElement.textContent = label;
    }

    overlay.classList.toggle("d-none", !isLoading);
    overlay.classList.toggle("d-flex", isLoading);
    overlay.style.display = isLoading ? "flex" : "none";
    overlay.style.visibility = isLoading ? "visible" : "hidden";
  }

  document.body.style.cursor = isLoading ? "wait" : "";
  document.body.classList.toggle("overflow-hidden", isLoading);

  ["generate-tasks-btn", "generate-tasks-btn-side", "delete-story-btn"].forEach((id) => {
    const button = document.getElementById(id);
    if (!button) return;
    setButtonLoading(button, isLoading, button.dataset.defaultLabel?.replace(/<.*?>/g, "") || button.textContent.trim());
  });
}

function setGenerateButtonsLoading(isLoading) {
  setPageLoading(isLoading, isLoading ? "Generando tareas..." : "Procesando...");
}

let currentStoryId = null;

async function deleteTask(taskId) {
  const confirmed = window.confirm(`¿Eliminar la tarea #${taskId}?`);
  if (!confirmed) return;

  clearPageError();
  setPageLoading(true, "Eliminando tarea...");

  try {
    const response = await fetch(`/tasks/${taskId}`, { method: "DELETE" });
    if (!response.ok) {
      const payload = await response.json().catch(() => ({}));
      throw new Error(payload.detail || "No se pudo eliminar la tarea.");
    }
    await loadStoryAndTasks(currentStoryId);
  } catch (error) {
    showPageError(error.message);
  } finally {
    setPageLoading(false);
  }
}

async function generateTasks(storyId) {
  setGenerateButtonsLoading(true);
  clearPageError();

  try {
    const formData = new FormData();
    formData.append("task_count", "3");

    const response = await fetch(`/user-stories/${storyId}/generate-tasks`, {
      method: "POST",
      headers: { Accept: "application/json" },
      body: formData,
    });

    if (!response.ok) {
      const payload = await response.json().catch(() => ({}));
      throw new Error(formatApiError(payload.detail));
    }

    await loadStoryAndTasks(storyId);
  } catch (error) {
    showPageError(error.message);
  } finally {
    setGenerateButtonsLoading(false);
  }
}

async function deleteStory(storyId) {
  const confirmed = window.confirm(
    `¿Eliminar la historia #${storyId}? También se borrarán todas sus tareas.`
  );
  if (!confirmed) return;

  clearPageError();
  setPageLoading(true, "Eliminando historia...");

  try {
    const response = await fetch(`/user-stories/${storyId}`, { method: "DELETE" });
    if (!response.ok) {
      const payload = await response.json().catch(() => ({}));
      throw new Error(payload.detail || "No se pudo eliminar la historia.");
    }
    window.location.href = "/user-stories";
  } catch (error) {
    showPageError(error.message);
    setPageLoading(false);
  }
}

async function loadStoryAndTasks(storyId) {
  currentStoryId = storyId;
  const [storyResponse, tasksResponse] = await Promise.all([
    fetch(`/user-stories/${storyId}`),
    fetch(`/user-stories/${storyId}/tasks/json`),
  ]);

  if (!storyResponse.ok) throw new Error("No se encontró la historia solicitada.");
  if (!tasksResponse.ok) throw new Error("No se pudieron cargar las tareas.");

  const story = await storyResponse.json();
  const tasksData = await tasksResponse.json();

  document.title = `Tareas — Historia #${story.id}`;
  setText("breadcrumb-story", `Historia #${story.id}`);
  setText("page-title", `Tareas de la historia #${story.id}`);
  setText("page-subtitle", `${story.project} — ${story.role} quiere ${story.goal}`);
  setText("story-project", story.project);
  setText("story-priority", story.priority);
  setText("story-points", String(story.story_points));
  setText("story-hours", `${story.effort_hours} h`);
  setText("story-description", story.description);

  renderTasks(tasksData.tasks || []);
}

document.addEventListener("DOMContentLoaded", () => {
  const storyId = getStoryIdFromPath();
  if (!storyId) {
    showPageError("Identificador de historia no válido.");
    return;
  }

  const params = new URLSearchParams(window.location.search);
  const error = params.get("error");
  if (error) showPageError(decodeURIComponent(error));

  ["generate-tasks-btn", "generate-tasks-btn-side", "delete-story-btn"].forEach((id) => {
    const button = document.getElementById(id);
    if (!button) return;
    button.dataset.defaultLabel = button.innerHTML;
  });

  ["generate-tasks-btn", "generate-tasks-btn-side"].forEach((id) => {
    const button = document.getElementById(id);
    if (!button) return;
    button.addEventListener("click", () => generateTasks(storyId));
  });

  const deleteStoryButton = document.getElementById("delete-story-btn");
  if (deleteStoryButton) {
    deleteStoryButton.addEventListener("click", () => {
      deleteStory(storyId);
    });
  }

  document.getElementById("tasks-list").addEventListener("click", (event) => {
    const button = event.target.closest("[data-delete-task-id]");
    if (!button) return;
    deleteTask(button.dataset.deleteTaskId);
  });

  loadStoryAndTasks(storyId).catch((error) => showPageError(error.message));
});
