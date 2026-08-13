const loadingEl = document.getElementById("loading");
const errorEl = document.getElementById("error");
const detailCard = document.getElementById("detailCard");

function getTodoIdFromUrl() {
  const params = new URLSearchParams(window.location.search);
  return params.get("id");
}

function findCachedTodo(id) {
  const cache = sessionStorage.getItem("todos-cache");
  if (!cache) return null;

  const todos = JSON.parse(cache);
  return todos.find((todo) => todo.id === Number(id)) || null;
}

function renderTodo(todo) {
  document.getElementById("detailTitle").textContent = todo.title;
  document.getElementById("detailId").textContent = todo.id;
  document.getElementById("detailUserId").textContent = todo.userId;
  document.getElementById("detailTitleField").textContent = todo.title;

  const completedEl = document.getElementById("detailCompleted");
  completedEl.innerHTML = "";
  const badge = document.createElement("span");
  badge.className = `badge ${todo.completed ? "completed" : "incomplete"}`;
  badge.textContent = todo.completed ? "დასრულებული" : "დაუსრულებელი";
  completedEl.appendChild(badge);

  detailCard.classList.remove("hidden");
}

async function init() {
  const id = getTodoIdFromUrl();

  if (!id) {
    errorEl.textContent = "todo-ს id მითითებული არ არის URL-ში.";
    errorEl.classList.remove("hidden");
    loadingEl.classList.add("hidden");
    return;
  }

  try {
    const cached = findCachedTodo(id);
    const todo = cached || (await fetchTodoById(id));
    renderTodo(todo);
  } catch (err) {
    errorEl.textContent = err.message;
    errorEl.classList.remove("hidden");
  } finally {
    loadingEl.classList.add("hidden");
  }
}

init();
