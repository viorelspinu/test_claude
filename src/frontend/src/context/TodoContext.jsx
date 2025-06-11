import React, { createContext, useContext, useReducer, useEffect } from 'react'
import todoService from '../services/todoService'

// Initial state
const initialState = {
  todos: [],
  loading: false,
  error: null,
  filters: {
    status: null,
    priority: null,
    dateRange: null,
  },
  pagination: {
    page: 1,
    perPage: 20,
    total: 0,
    pages: 0,
  },
  stats: {
    total_count: 0,
    completed_count: 0,
    pending_count: 0,
    overdue_count: 0,
    completion_rate: 0,
  },
  bulkSelection: {
    selectedIds: [],
    isSelecting: false,
  },
  bulkOperation: {
    loading: false,
    progress: 0,
    error: null,
  },
}

// Action types
export const actionTypes = {
  SET_LOADING: 'SET_LOADING',
  SET_ERROR: 'SET_ERROR',
  SET_TODOS: 'SET_TODOS',
  ADD_TODO: 'ADD_TODO',
  UPDATE_TODO: 'UPDATE_TODO',
  DELETE_TODO: 'DELETE_TODO',
  SET_FILTERS: 'SET_FILTERS',
  SET_PAGINATION: 'SET_PAGINATION',
  SET_STATS: 'SET_STATS',
  CLEAR_ERROR: 'CLEAR_ERROR',
  SET_BULK_SELECTION: 'SET_BULK_SELECTION',
  TOGGLE_BULK_SELECT: 'TOGGLE_BULK_SELECT',
  CLEAR_BULK_SELECTION: 'CLEAR_BULK_SELECTION',
  SET_BULK_OPERATION_LOADING: 'SET_BULK_OPERATION_LOADING',
  SET_BULK_OPERATION_PROGRESS: 'SET_BULK_OPERATION_PROGRESS',
  SET_BULK_OPERATION_ERROR: 'SET_BULK_OPERATION_ERROR',
  BULK_UPDATE_TODOS: 'BULK_UPDATE_TODOS',
  BULK_DELETE_TODOS: 'BULK_DELETE_TODOS',
}

// Reducer function
const todoReducer = (state, action) => {
  switch (action.type) {
    case actionTypes.SET_LOADING:
      return {
        ...state,
        loading: action.payload,
      }

    case actionTypes.SET_ERROR:
      return {
        ...state,
        error: action.payload,
        loading: false,
      }

    case actionTypes.CLEAR_ERROR:
      return {
        ...state,
        error: null,
      }

    case actionTypes.SET_TODOS:
      return {
        ...state,
        todos: action.payload,
        loading: false,
        error: null,
      }

    case actionTypes.ADD_TODO:
      return {
        ...state,
        todos: [action.payload, ...state.todos],
        error: null,
      }

    case actionTypes.UPDATE_TODO:
      return {
        ...state,
        todos: state.todos.map((todo) =>
          todo.id === action.payload.id ? action.payload : todo
        ),
        error: null,
      }

    case actionTypes.DELETE_TODO:
      return {
        ...state,
        todos: state.todos.filter((todo) => todo.id !== action.payload),
        error: null,
      }

    case actionTypes.SET_FILTERS:
      return {
        ...state,
        filters: { ...state.filters, ...action.payload },
      }

    case actionTypes.SET_PAGINATION:
      return {
        ...state,
        pagination: { ...state.pagination, ...action.payload },
      }

    case actionTypes.SET_STATS:
      return {
        ...state,
        stats: action.payload,
      }

    case actionTypes.SET_BULK_SELECTION:
      return {
        ...state,
        bulkSelection: {
          ...state.bulkSelection,
          selectedIds: action.payload.selectedIds,
          isSelecting: action.payload.selectedIds.length > 0,
        },
      }

    case actionTypes.TOGGLE_BULK_SELECT:
      const { todoId } = action.payload
      const isSelected = state.bulkSelection.selectedIds.includes(todoId)
      const newSelectedIds = isSelected
        ? state.bulkSelection.selectedIds.filter(id => id !== todoId)
        : [...state.bulkSelection.selectedIds, todoId]
      
      return {
        ...state,
        bulkSelection: {
          selectedIds: newSelectedIds,
          isSelecting: newSelectedIds.length > 0,
        },
      }

    case actionTypes.CLEAR_BULK_SELECTION:
      return {
        ...state,
        bulkSelection: {
          selectedIds: [],
          isSelecting: false,
        },
      }

    case actionTypes.SET_BULK_OPERATION_LOADING:
      return {
        ...state,
        bulkOperation: {
          ...state.bulkOperation,
          loading: action.payload,
        },
      }

    case actionTypes.SET_BULK_OPERATION_PROGRESS:
      return {
        ...state,
        bulkOperation: {
          ...state.bulkOperation,
          progress: action.payload,
        },
      }

    case actionTypes.SET_BULK_OPERATION_ERROR:
      return {
        ...state,
        bulkOperation: {
          ...state.bulkOperation,
          error: action.payload,
          loading: false,
        },
      }

    case actionTypes.BULK_UPDATE_TODOS:
      return {
        ...state,
        todos: state.todos.map(todo => {
          const updatedTodo = action.payload.find(updated => updated.id === todo.id)
          return updatedTodo ? updatedTodo : todo
        }),
        bulkSelection: {
          selectedIds: [],
          isSelecting: false,
        },
        bulkOperation: {
          loading: false,
          progress: 0,
          error: null,
        },
      }

    case actionTypes.BULK_DELETE_TODOS:
      return {
        ...state,
        todos: state.todos.filter(todo => !action.payload.includes(todo.id)),
        bulkSelection: {
          selectedIds: [],
          isSelecting: false,
        },
        bulkOperation: {
          loading: false,
          progress: 0,
          error: null,
        },
      }

    default:
      return state
  }
}

// Create context
const TodoContext = createContext()

// Context provider component
export const TodoProvider = ({ children }) => {
  const [state, dispatch] = useReducer(todoReducer, initialState)

  // Action creators
  const actions = {
    setLoading: (loading) => 
      dispatch({ type: actionTypes.SET_LOADING, payload: loading }),

    setError: (error) => 
      dispatch({ type: actionTypes.SET_ERROR, payload: error }),

    clearError: () => 
      dispatch({ type: actionTypes.CLEAR_ERROR }),

    setTodos: (todos) => 
      dispatch({ type: actionTypes.SET_TODOS, payload: todos }),

    addTodo: (todo) => 
      dispatch({ type: actionTypes.ADD_TODO, payload: todo }),

    updateTodo: (todo) => 
      dispatch({ type: actionTypes.UPDATE_TODO, payload: todo }),

    deleteTodo: (todoId) => 
      dispatch({ type: actionTypes.DELETE_TODO, payload: todoId }),

    setFilters: (filters) => 
      dispatch({ type: actionTypes.SET_FILTERS, payload: filters }),

    setPagination: (pagination) => 
      dispatch({ type: actionTypes.SET_PAGINATION, payload: pagination }),

    setStats: (stats) => 
      dispatch({ type: actionTypes.SET_STATS, payload: stats }),

    // Bulk selection actions
    setBulkSelection: (selectedIds) => 
      dispatch({ type: actionTypes.SET_BULK_SELECTION, payload: { selectedIds } }),

    toggleBulkSelect: (todoId) => 
      dispatch({ type: actionTypes.TOGGLE_BULK_SELECT, payload: { todoId } }),

    clearBulkSelection: () => 
      dispatch({ type: actionTypes.CLEAR_BULK_SELECTION }),

    selectAllTodos: () => {
      const allIds = state.todos.map(todo => todo.id)
      dispatch({ type: actionTypes.SET_BULK_SELECTION, payload: { selectedIds: allIds } })
    },

    setBulkOperationLoading: (loading) => 
      dispatch({ type: actionTypes.SET_BULK_OPERATION_LOADING, payload: loading }),

    setBulkOperationProgress: (progress) => 
      dispatch({ type: actionTypes.SET_BULK_OPERATION_PROGRESS, payload: progress }),

    setBulkOperationError: (error) => 
      dispatch({ type: actionTypes.SET_BULK_OPERATION_ERROR, payload: error }),

    // Async actions
    fetchTodos: async (params = {}) => {
      try {
        actions.setLoading(true)
        const response = await todoService.getTodos(params)
        actions.setTodos(response.todos || response)
        if (response.pagination) {
          actions.setPagination(response.pagination)
        }
      } catch (error) {
        actions.setError('Failed to fetch todos')
        console.error('Fetch todos error:', error)
      } finally {
        actions.setLoading(false)
      }
    },

    fetchStats: async () => {
      try {
        const stats = await todoService.getStats()
        actions.setStats(stats)
      } catch (error) {
        console.error('Fetch stats error:', error)
      }
    },

    createTodo: async (todoData) => {
      try {
        actions.setLoading(true)
        const newTodo = await todoService.createTodo(todoData)
        actions.addTodo(newTodo)
        actions.fetchStats() // Refresh stats
        return newTodo
      } catch (error) {
        actions.setError('Failed to create todo')
        console.error('Create todo error:', error)
        throw error
      } finally {
        actions.setLoading(false)
      }
    },

    updateTodoById: async (id, todoData) => {
      try {
        const updatedTodo = await todoService.updateTodo(id, todoData)
        actions.updateTodo(updatedTodo)
        actions.fetchStats() // Refresh stats
        return updatedTodo
      } catch (error) {
        actions.setError('Failed to update todo')
        console.error('Update todo error:', error)
        throw error
      }
    },

    deleteTodoById: async (id) => {
      try {
        await todoService.deleteTodo(id)
        actions.deleteTodo(id)
        actions.fetchStats() // Refresh stats
      } catch (error) {
        actions.setError('Failed to delete todo')
        console.error('Delete todo error:', error)
        throw error
      }
    },

    // Bulk operations
    bulkDeleteTodos: async (todoIds) => {
      try {
        actions.setBulkOperationLoading(true)
        actions.setBulkOperationError(null)
        
        // Show progress for operations > 10 items
        if (todoIds.length > 10) {
          actions.setBulkOperationProgress(0)
        }

        const result = await todoService.bulkOperation('delete', todoIds)
        
        // Update progress
        if (todoIds.length > 10) {
          actions.setBulkOperationProgress(100)
        }

        // Handle partial failures
        if (result.failed && result.failed.length > 0) {
          const failedCount = result.failed.length
          const totalCount = todoIds.length
          const successCount = totalCount - failedCount
          actions.setBulkOperationError(
            `${successCount} of ${totalCount} todos deleted. ${failedCount} failed.`
          )
        }

        // Update state with successful deletions
        const successfulIds = result.successful || todoIds.filter(id => 
          !result.failed?.some(failed => failed.id === id)
        )
        dispatch({ type: actionTypes.BULK_DELETE_TODOS, payload: successfulIds })
        
        actions.fetchStats() // Refresh stats
        return result
      } catch (error) {
        actions.setBulkOperationError('Failed to delete selected todos')
        console.error('Bulk delete error:', error)
        throw error
      } finally {
        actions.setBulkOperationLoading(false)
        if (todoIds.length > 10) {
          setTimeout(() => actions.setBulkOperationProgress(0), 2000)
        }
      }
    },

    bulkUpdateTodoStatus: async (todoIds, status) => {
      try {
        actions.setBulkOperationLoading(true)
        actions.setBulkOperationError(null)
        
        // Show progress for operations > 10 items
        if (todoIds.length > 10) {
          actions.setBulkOperationProgress(0)
        }

        const result = await todoService.bulkOperation('update', todoIds, { status })
        
        // Update progress
        if (todoIds.length > 10) {
          actions.setBulkOperationProgress(100)
        }

        // Handle partial failures
        if (result.failed && result.failed.length > 0) {
          const failedCount = result.failed.length
          const totalCount = todoIds.length
          const successCount = totalCount - failedCount
          actions.setBulkOperationError(
            `${successCount} of ${totalCount} todos updated. ${failedCount} failed.`
          )
        }

        // Update state with successful updates
        if (result.successful && result.successful.length > 0) {
          dispatch({ type: actionTypes.BULK_UPDATE_TODOS, payload: result.successful })
        }
        
        actions.fetchStats() // Refresh stats
        return result
      } catch (error) {
        actions.setBulkOperationError('Failed to update selected todos')
        console.error('Bulk update error:', error)
        throw error
      } finally {
        actions.setBulkOperationLoading(false)
        if (todoIds.length > 10) {
          setTimeout(() => actions.setBulkOperationProgress(0), 2000)
        }
      }
    },
  }

  return (
    <TodoContext.Provider value={{ state, actions }}>
      {children}
    </TodoContext.Provider>
  )
}

// Hook to use the todo context
export const useTodo = () => {
  const context = useContext(TodoContext)
  if (!context) {
    throw new Error('useTodo must be used within a TodoProvider')
  }
  return context
}

export default TodoContext