const state = {
  todos: [],
  filtered: [],
  page: 1,
  perPage: 10,
  search: "",
  userId: "all",
  status: "all",
};

const searchInput = document.getElementById("search");
const userFilter = document.getElementById("userFilter");
const statusFilter = document.getElementById("statusFilter");
const perPageSelect = document.getElementById("perPage");
const todoListEl = document.getElementById("todoList");
const paginationEl = document.getElementById("pagination");
const resultCountEl = document.getElementById("resultCount");
const loadingEl = document.getElementById("loading");
const errorEl = document.getElementById("error");

function populateUserFilter(todos) {
  const userIds = [...new Set(todos.map((todo) => todo.userId))].sort((a, b) => a - b);
  for (const userId of userIds) {
    const option = document.createElement("option");
    option.value = String(userId);
    option.textContent = `User ${userId}`;
    userFilter.appendChild(option);
  }
}

function applyFilters() {
  const search = state.search.trim().toLowerCase();

  state.filtered = state.todos.filter((todo) => {
    const matchesSearch = !search || todo.title.toLowerCase().includes(search);
    const matchesUser = state.userId === "all" || todo.userId === Number(state.userId);
    const matchesStatus =
      state.status === "all" ||
      (state.status === "completed" && todo.completed) ||
      (state.status === "incomplete" && !todo.completed);

    return matchesSearch && matchesUser && matchesStatus;
  });

  state.page = 1;
  renderList();
  renderPagination();
}

function renderList() {
  const totalPages = Math.max(1, Math.ceil(state.filtered.length / state.perPage));
  if (state.page > totalPages) state.page = totalPages;

  const start = (state.page - 1) * state.perPage;
  const pageItems = state.filtered.slice(start, start + state.perPage);

  resultCountEl.textContent = `ნაპოვნია ${state.filtered.length} todo`;

  todoListEl.innerHTML = "";
  for (const todo of pageItems) {
    const li = document.createElement("li");
    li.className = "todo-item";

    const dot = document.createElement("span");
    dot.className = `status-dot ${todo.completed ? "completed" : "incomplete"}`;

    const link = document.createElement("a");
    link.href = `todo.html?id=${todo.id}`;
    link.textContent = todo.title;

    const badge = document.createElement("span");
    badge.className = "user-badge";
    badge.textContent = `User ${todo.userId}`;

    li.append(dot, link, badge);
    todoListEl.appendChild(li);
  }
}

function goToPage(page) {
  state.page = page;
  renderList();
  renderPagination();
}

function renderPagination() {
  const totalPages = Math.max(1, Math.ceil(state.filtered.length / state.perPage));
  paginationEl.innerHTML = "";

  if (totalPages <= 1) return;

  const prevBtn = document.createElement("button");
  prevBtn.textContent = "‹ წინა";
  prevBtn.disabled = state.page === 1;
  prevBtn.addEventListener("click", () => goToPage(state.page - 1));
  paginationEl.appendChild(prevBtn);

  const pageNumbers = getPageNumbers(state.page, totalPages);
  for (const entry of pageNumbers) {
    if (entry === "...") {
      const span = document.createElement("span");
      span.className = "ellipsis";
      span.textContent = "...";
      paginationEl.appendChild(span);
      continue;
    }

    const btn = document.createElement("button");
    btn.textContent = String(entry);
    if (entry === state.page) btn.classList.add("active");
    btn.addEventListener("click", () => goToPage(entry));
    paginationEl.appendChild(btn);
  }

  const nextBtn = document.createElement("button");
  nextBtn.textContent = "შემდეგი ›";
  nextBtn.disabled = state.page === totalPages;
  nextBtn.addEventListener("click", () => goToPage(state.page + 1));
  paginationEl.appendChild(nextBtn);
}

function getPageNumbers(current, total) {
  const delta = 1;
  const range = [];
  for (let i = 1; i <= total; i++) {
    if (i === 1 || i === total || (i >= current - delta && i <= current + delta)) {
      range.push(i);
    }
  }

  const result = [];
  let prev = 0;
  for (const page of range) {
    if (prev && page - prev > 1) result.push("...");
    result.push(page);
    prev = page;
  }
  return result;
}

let searchDebounceTimer;
searchInput.addEventListener("input", (event) => {
  clearTimeout(searchDebounceTimer);
  searchDebounceTimer = setTimeout(() => {
    state.search = event.target.value;
    applyFilters();
  }, 250);
});

userFilter.addEventListener("change", (event) => {
  state.userId = event.target.value;
  applyFilters();
});

statusFilter.addEventListener("change", (event) => {
  state.status = event.target.value;
  applyFilters();
});

perPageSelect.addEventListener("change", (event) => {
  state.perPage = Number(event.target.value);
  applyFilters();
});

async function init() {
  try {
    const todos = await fetchAllTodos();
    state.todos = todos;
    sessionStorage.setItem("todos-cache", JSON.stringify(todos));

    populateUserFilter(todos);
    applyFilters();
  } catch (err) {
    errorEl.textContent = err.message;
    errorEl.classList.remove("hidden");
  } finally {
    loadingEl.classList.add("hidden");
  }
}

init();
