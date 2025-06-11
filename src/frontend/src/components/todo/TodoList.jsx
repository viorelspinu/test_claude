import React, { useEffect, useState } from 'react'
import { useTodo } from '../../context/TodoContext'
import BulkActions from './BulkActions'
import TodoItem from './TodoItem'
import styles from './TodoList.module.css'

const TodoList = () => {
  const { state, actions } = useTodo()
  const { todos, loading, error, bulkSelection } = state
  const [editingTodo, setEditingTodo] = useState(null)

  // Fetch todos on component mount
  useEffect(() => {
    actions.fetchTodos()
  }, [])

  // Loading state
  if (loading) {
    return (
      <div className={styles.todoList}>
        <div className={styles.loadingState}>
          <div className={styles.spinner}></div>
          <p>Loading your todos...</p>
        </div>
      </div>
    )
  }

  // Error state
  if (error) {
    return (
      <div className={styles.todoList}>
        <div className={styles.errorState}>
          <div className={styles.errorIcon}>⚠️</div>
          <h3>Something went wrong</h3>
          <p>{error}</p>
          <button 
            className={styles.retryButton}
            onClick={() => {
              actions.clearError()
              actions.fetchTodos()
            }}
          >
            Try Again
          </button>
        </div>
      </div>
    )
  }

  // Empty state
  if (!todos || todos.length === 0) {
    return (
      <div className={styles.todoList}>
        <div className={styles.emptyState}>
          <div className={styles.emptyIcon}>📝</div>
          <h3>No todos yet</h3>
          <p>Start by adding your first todo item above!</p>
        </div>
      </div>
    )
  }

  // Handle select all functionality
  const handleSelectAll = () => {
    if (bulkSelection.selectedIds.length === todos.length) {
      actions.clearBulkSelection()
    } else {
      actions.selectAllTodos()
    }
  }

  // Render todo list
  return (
    <div className={styles.todoList}>
      <div className={styles.todoListHeader}>
        <div className={styles.headerContent}>
          <div className={styles.headerLeft}>
            <h3>Your Todos ({todos.length})</h3>
          </div>
          <div className={styles.headerRight}>
            <label className={styles.selectAllContainer}>
              <input
                type="checkbox"
                className={styles.selectAllCheckbox}
                checked={bulkSelection.selectedIds.length === todos.length && todos.length > 0}
                onChange={handleSelectAll}
              />
              <span className={styles.selectAllLabel}>
                {bulkSelection.selectedIds.length > 0 
                  ? `${bulkSelection.selectedIds.length} selected` 
                  : 'Select all'
                }
              </span>
            </label>
          </div>
        </div>
      </div>

      {/* Bulk Actions Toolbar */}
      {bulkSelection.isSelecting && (
        <BulkActions selectedIds={bulkSelection.selectedIds} />
      )}
      
      <div className={styles.todoItems}>
        {todos.map((todo) => (
          <TodoItem
            key={todo.id}
            todo={todo}
            onToggleComplete={async (todoId, newStatus) => {
              try {
                await actions.updateTodoById(todoId, { status: newStatus })
              } catch (error) {
                console.error('Failed to update todo status:', error)
              }
            }}
            onEdit={(todo) => {
              // TODO: Implement edit functionality
              // For now, we'll set the editing todo state
              setEditingTodo(todo)
              console.log('Edit todo:', todo)
            }}
            onDelete={async (todoId) => {
              await actions.deleteTodoById(todoId)
            }}
          />
        ))}
      </div>
    </div>
  )
}

export default TodoList