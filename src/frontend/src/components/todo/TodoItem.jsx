import React, { useState } from 'react'
import PropTypes from 'prop-types'
import { useTodo } from '../../context/TodoContext'
import styles from './TodoItem.module.css'

/**
 * TodoItem Component
 * 
 * Displays an individual todo item with interactive functionality including:
 * - Completion toggle checkbox
 * - Edit and delete action buttons
 * - Priority color coding
 * - Overdue highlighting for pending items past due date
 * - Visual differentiation between completed and pending todos
 */
const TodoItem = ({ todo, onToggleComplete, onEdit, onDelete }) => {
  const [isDeleting, setIsDeleting] = useState(false)
  const { state } = useTodo()
  const { bulkSelection } = state
  const { actions } = useTodo()
  
  // Check if todo is selected for bulk operations
  const isSelected = bulkSelection.selectedIds.includes(todo.id)
  
  // Check if todo is overdue
  const isOverdue = todo.status === 'pending' && 
    todo.due_date && 
    new Date(todo.due_date) < new Date() &&
    new Date(todo.due_date).toDateString() !== new Date().toDateString()
  
  // Format date for display
  const formatDate = (dateString) => {
    const date = new Date(dateString)
    return date.toLocaleDateString('en-US', { 
      month: 'short', 
      day: 'numeric', 
      year: 'numeric' 
    })
  }
  
  // Handle completion toggle
  const handleToggleComplete = () => {
    onToggleComplete(todo.id, todo.status === 'completed' ? 'pending' : 'completed')
  }
  
  // Handle delete with confirmation
  const handleDelete = async () => {
    if (window.confirm(`Are you sure you want to delete "${todo.title}"?`)) {
      setIsDeleting(true)
      try {
        await onDelete(todo.id)
      } catch (error) {
        console.error('Failed to delete todo:', error)
        setIsDeleting(false)
      }
    }
  }
  
  // Handle edit
  const handleEdit = () => {
    onEdit(todo)
  }
  
  // Determine priority class
  const priorityClass = `priority${todo.priority.charAt(0).toUpperCase() + todo.priority.slice(1).toLowerCase()}`
  
  // Determine status class  
  const statusClass = `status${todo.status.charAt(0).toUpperCase() + todo.status.slice(1)}`
  
  return (
    <div 
      className={`
        ${styles.todoItem} 
        ${isSelected ? styles.selected : ''} 
        ${todo.status === 'completed' ? styles.completed : ''}
        ${isOverdue ? styles.overdue : ''}
        ${isDeleting ? styles.deleting : ''}
      `}
    >
      {/* Selection checkbox for bulk operations */}
      <div className={styles.todoSelection}>
        <input
          type="checkbox"
          className={styles.selectionCheckbox}
          checked={isSelected}
          onChange={() => actions.toggleBulkSelect(todo.id)}
          aria-label={`Select ${todo.title} for bulk operations`}
        />
      </div>
      
      {/* Main todo content */}
      <div className={styles.todoContent}>
        {/* Completion checkbox */}
        <div className={styles.completionContainer}>
          <input
            type="checkbox"
            id={`todo-complete-${todo.id}`}
            className={styles.completionCheckbox}
            checked={todo.status === 'completed'}
            onChange={handleToggleComplete}
            aria-label={`Mark ${todo.title} as ${todo.status === 'completed' ? 'pending' : 'completed'}`}
          />
          <label 
            htmlFor={`todo-complete-${todo.id}`}
            className={styles.completionLabel}
          >
            <span className={styles.checkmark}></span>
          </label>
        </div>
        
        {/* Todo details */}
        <div className={styles.todoDetails}>
          <div className={styles.todoHeader}>
            <h4 className={`${styles.todoTitle} ${todo.status === 'completed' ? styles.completedTitle : ''}`}>
              {todo.title}
            </h4>
            <span className={`${styles.priorityBadge} ${styles[priorityClass]}`}>
              {todo.priority}
            </span>
          </div>
          
          {todo.description && (
            <p className={styles.todoDescription}>{todo.description}</p>
          )}
          
          <div className={styles.todoMeta}>
            <span className={`${styles.statusBadge} ${styles[statusClass]}`}>
              {todo.status === 'completed' ? '✓ Completed' : '○ Pending'}
            </span>
            
            {todo.due_date && (
              <span className={`${styles.dueDate} ${isOverdue ? styles.overdueDueDate : ''}`}>
                {isOverdue && <span className={styles.overdueIcon}>⚠️</span>}
                Due: {formatDate(todo.due_date)}
              </span>
            )}
            
            <span className={styles.createdDate}>
              Created: {formatDate(todo.created_at)}
            </span>
          </div>
        </div>
      </div>
      
      {/* Action buttons */}
      <div className={styles.todoActions}>
        <button 
          className={`${styles.actionButton} ${styles.editButton}`}
          onClick={handleEdit}
          title="Edit todo"
          disabled={isDeleting}
          aria-label={`Edit ${todo.title}`}
        >
          ✏️
        </button>
        
        <button 
          className={`${styles.actionButton} ${styles.deleteButton}`}
          onClick={handleDelete}
          title="Delete todo"
          disabled={isDeleting}
          aria-label={`Delete ${todo.title}`}
        >
          {isDeleting ? '...' : '🗑️'}
        </button>
      </div>
    </div>
  )
}

// PropTypes validation
TodoItem.propTypes = {
  todo: PropTypes.shape({
    id: PropTypes.number.isRequired,
    title: PropTypes.string.isRequired,
    description: PropTypes.string,
    priority: PropTypes.oneOf(['low', 'medium', 'high']).isRequired,
    status: PropTypes.oneOf(['pending', 'completed']).isRequired,
    due_date: PropTypes.string,
    created_at: PropTypes.string,
    updated_at: PropTypes.string
  }).isRequired,
  onToggleComplete: PropTypes.func.isRequired,
  onEdit: PropTypes.func.isRequired,
  onDelete: PropTypes.func.isRequired
}

export default TodoItem