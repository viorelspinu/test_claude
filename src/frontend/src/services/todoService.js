import api from './api'

export const todoService = {
  // Get all todos with optional filters and pagination
  getTodos: async (params = {}) => {
    const response = await api.get('/todos', { params })
    return response.data
  },

  // Get a specific todo by ID
  getTodo: async (id) => {
    const response = await api.get(`/todos/${id}`)
    return response.data
  },

  // Create a new todo
  createTodo: async (todoData) => {
    const response = await api.post('/todos', todoData)
    return response.data
  },

  // Update an existing todo
  updateTodo: async (id, todoData) => {
    const response = await api.put(`/todos/${id}`, todoData)
    return response.data
  },

  // Delete a todo
  deleteTodo: async (id) => {
    const response = await api.delete(`/todos/${id}`)
    return response.data
  },

  // Get todo statistics
  getStats: async () => {
    const response = await api.get('/todos/stats')
    return response.data
  },

  // Bulk operations
  bulkOperation: async (operation, todoIds, options = {}) => {
    const response = await api.post('/todos/bulk', {
      operation,
      todo_ids: todoIds,
      options,
    })
    return response.data
  },
}

export default todoService