function formatDate(isoDate) {
  if (!isoDate) return "—";
  const date = new Date(isoDate);
  if (Number.isNaN(date.getTime())) return "—";
  return date.toLocaleDateString("es-ES", { day: "2-digit", month: "2-digit" });
}

function showError(message) {
  const container = document.getElementById("error-alert");
  if (!message) {
    container.classList.add("d-none");
    container.innerHTML = "";
    return;
  }
  container.classList.remove("d-none");
  container.innerHTML = `
    <div class="alert alert-danger d-flex align-items-center mb-0" role="alert">
      <i class="bi bi-exclamation-triangle-fill me-2"></i>
      <div><strong>Error:</strong> ${message}</div>
    </div>
  `;
}

function renderStories(stories) {
  const list = document.getElementById("stories-list");
  const empty = document.getElementById("stories-empty");
  const header = document.getElementById("stories-header");
  const count = document.getElementById("stories-count");

  if (!stories.length) {
    header.classList.add("d-none");
    list.innerHTML = "";
    empty.classList.remove("d-none");
    return;
  }

  header.classList.remove("d-none");
  empty.classList.add("d-none");
  count.textContent = `${stories.length} historia(s)`;

  list.innerHTML = stories
    .map(
      (story) => `
      <div class="col-md-6 col-xl-4">
        <div class="card h-100 border-0 shadow-sm">
          <div class="card-header bg-white d-flex justify-content-between align-items-start gap-2">
            <div>
              <span class="badge text-bg-secondary mb-2">#${story.id}</span>
              <h3 class="h6 fw-bold mb-1">${story.project}</h3>
              <p class="small text-muted mb-0">${story.role} — ${story.goal}</p>
            </div>
            <span class="badge text-bg-primary">${story.priority}</span>
          </div>
          <div class="card-body">
            <div class="row g-2 mb-3">
              <div class="col-4">
                <div class="bg-primary-subtle rounded-3 p-2 text-center">
                  <div class="small text-muted">Puntos</div>
                  <div class="fw-bold text-primary">${story.story_points}</div>
                </div>
              </div>
              <div class="col-4">
                <div class="bg-primary-subtle rounded-3 p-2 text-center">
                  <div class="small text-muted">Horas</div>
                  <div class="fw-bold text-primary">${story.effort_hours}</div>
                </div>
              </div>
              <div class="col-4">
                <div class="bg-primary-subtle rounded-3 p-2 text-center">
                  <div class="small text-muted">Creada</div>
                  <div class="fw-bold text-primary small">${formatDate(story.created_at)}</div>
                </div>
              </div>
            </div>
            <p class="card-text small text-muted">${story.description}</p>
          </div>
          <div class="card-footer bg-white border-top-0 pt-0 pb-3 px-3">
            <div class="d-grid gap-2 d-sm-flex mb-2">
              <form method="post" action="/user-stories/${story.id}/generate-tasks" class="flex-fill">
                <button type="submit" class="btn btn-primary w-100">
                  <i class="bi bi-list-task me-1"></i>Generar tareas
                </button>
              </form>
              <a href="/user-stories/${story.id}/tasks" class="btn btn-outline-primary flex-fill">
                <i class="bi bi-eye me-1"></i>Ver tareas
              </a>
            </div>
            <button
              type="button"
              class="btn btn-outline-danger w-100"
              data-delete-story-id="${story.id}"
            >
              <i class="bi bi-trash me-1"></i>Eliminar historia
            </button>
          </div>
        </div>
      </div>
    `
    )
    .join("");
}

async function loadStories() {
  document.getElementById("stories-empty").classList.add("d-none");
  try {
    const response = await fetch("/user-stories/json");
    if (!response.ok) throw new Error("No se pudieron cargar las historias.");
    const data = await response.json();
    renderStories(data.user_stories || []);
  } catch (error) {
    showError(error.message);
  }
}

async function deleteStory(storyId) {
  const confirmed = window.confirm(
    `¿Eliminar la historia #${storyId}? También se borrarán todas sus tareas.`
  );
  if (!confirmed) return;

  try {
    const response = await fetch(`/user-stories/${storyId}`, { method: "DELETE" });
    if (!response.ok) {
      const payload = await response.json().catch(() => ({}));
      throw new Error(payload.detail || "No se pudo eliminar la historia.");
    }
    await loadStories();
  } catch (error) {
    showError(error.message);
  }
}

document.addEventListener("DOMContentLoaded", () => {
  const params = new URLSearchParams(window.location.search);
  const error = params.get("error");
  if (error) showError(decodeURIComponent(error));

  document.getElementById("stories-list").addEventListener("click", (event) => {
    const button = event.target.closest("[data-delete-story-id]");
    if (!button) return;
    deleteStory(button.dataset.deleteStoryId);
  });

  loadStories();
});
