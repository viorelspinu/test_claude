const API_BASE_URL = 'http://localhost:8080/api';

async function apiRequest(endpoint, options = {}) {
  const url = `${API_BASE_URL}${endpoint}`;
  
  const config = {
    headers: {
      'Content-Type': 'application/json',
      ...options.headers,
    },
    ...options,
  };

  try {
    const response = await fetch(url, config);
    
    if (!response.ok) {
      const errorData = await response.json().catch(() => ({}));
      throw new Error(errorData.error || `HTTP error! status: ${response.status}`);
    }
    
    return await response.json();
  } catch (error) {
    console.error('API request failed:', error);
    throw error;
  }
}

export async function fetchTodos() {
  return apiRequest('/todos');
}

export async function createTodo(text) {
  return apiRequest('/todos', {
    method: 'POST',
    body: JSON.stringify({ text }),
  });
}

export async function updateTodo(id, updates) {
  return apiRequest(`/todos/${id}`, {
    method: 'PUT',
    body: JSON.stringify(updates),
  });
}

export async function updateTodoText(id, text) {
  return apiRequest(`/todos/${id}`, {
    method: 'PUT',
    body: JSON.stringify({ text }),
  });
}

export async function deleteTodo(id) {
  return apiRequest(`/todos/${id}`, {
    method: 'DELETE',
  });
}