const API_BASE_URL = "https://jsonplaceholder.typicode.com/todos";

async function fetchAllTodos() {
  const response = await fetch(API_BASE_URL);
  if (!response.ok) {
    throw new Error(`ვერ მოხერხდა მონაცემების წამოღება (სტატუსი: ${response.status})`);
  }
  return response.json();
}

async function fetchTodoById(id) {
  const response = await fetch(`${API_BASE_URL}/${id}`);
  if (!response.ok) {
    throw new Error(`ვერ მოიძებნა todo id=${id} (სტატუსი: ${response.status})`);
  }
  return response.json();
}
