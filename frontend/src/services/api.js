/**
 * API Service Layer
 * Provides HTTP methods for communicating with Flask backend
 */

const API_BASE_URL = 'http://localhost:8080/api';

/**
 * Base fetch wrapper with error handling
 * @param {string} endpoint - API endpoint
 * @param {object} options - fetch options
 * @returns {Promise<any>} - Response data
 */
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
      throw new Error(errorData.message || `HTTP ${response.status}: ${response.statusText}`);
    }

    // Handle empty responses
    const text = await response.text();
    return text ? JSON.parse(text) : null;
  } catch (error) {
    console.error(`API request failed: ${url}`, error);
    throw error;
  }
}

/**
 * Get all todos
 * @returns {Promise<Array>} - Array of todo objects
 */
export async function getTodos() {
  return apiRequest('/todos');
}

/**
 * Create a new todo
 * @param {string} text - Todo text content
 * @returns {Promise<object>} - Created todo object
 */
export async function createTodo(text) {
  if (!text || !text.trim()) {
    throw new Error('Todo text is required');
  }

  return apiRequest('/todos', {
    method: 'POST',
    body: JSON.stringify({ text: text.trim() }),
  });
}

/**
 * Update an existing todo
 * @param {string} id - Todo ID
 * @param {object} updates - Updates to apply (text, completed)
 * @returns {Promise<object>} - Updated todo object
 */
export async function updateTodo(id, updates) {
  if (!id) {
    throw new Error('Todo ID is required');
  }

  if (!updates || Object.keys(updates).length === 0) {
    throw new Error('Updates are required');
  }

  return apiRequest(`/todos/${id}`, {
    method: 'PUT',
    body: JSON.stringify(updates),
  });
}

/**
 * Delete a todo
 * @param {string} id - Todo ID
 * @returns {Promise<object>} - Delete confirmation
 */
export async function deleteTodo(id) {
  if (!id) {
    throw new Error('Todo ID is required');
  }

  return apiRequest(`/todos/${id}`, {
    method: 'DELETE',
  });
}

/**
 * Toggle todo completion status
 * @param {string} id - Todo ID
 * @param {boolean} completed - New completion status
 * @returns {Promise<object>} - Updated todo object
 */
export async function toggleTodo(id, completed) {
  return updateTodo(id, { completed });
}

// Export default API object
const api = {
  getTodos,
  createTodo,
  updateTodo,
  deleteTodo,
  toggleTodo,
};

export default api;