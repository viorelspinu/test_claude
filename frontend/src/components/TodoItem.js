import React, { useState } from 'react';
import ConfirmDialog from './ConfirmDialog';

/**
 * TodoItem Component
 * Represents an individual todo item with actions
 * 
 * @param {Object} props - Component props
 * @param {Object} props.todo - Todo object {id, text, completed, created_at}
 * @param {Function} props.onToggle - Callback for toggling completion status
 * @param {Function} props.onDelete - Callback for deleting todo
 * @param {Function} props.onUpdate - Callback for updating todo text
 */
function TodoItem({ todo, onToggle, onDelete, onUpdate }) {
  const [isToggling, setIsToggling] = useState(false);
  const [isDeleting, setIsDeleting] = useState(false);
  const [isEditing, setIsEditing] = useState(false);
  const [isUpdating, setIsUpdating] = useState(false);
  const [editText, setEditText] = useState(todo.text);
  const [error, setError] = useState(null);
  const [showDeleteConfirm, setShowDeleteConfirm] = useState(false);

  /**
   * Handle toggle completion status
   */
  const handleToggle = async () => {
    if (isToggling || isDeleting) return;

    try {
      setIsToggling(true);
      setError(null);
      await onToggle(todo.id);
    } catch (err) {
      console.error('Failed to toggle todo:', err);
      setError('Failed to update todo');
    } finally {
      setIsToggling(false);
    }
  };

  /**
   * Handle delete button click
   */
  const handleDeleteClick = () => {
    if (isToggling || isDeleting) return;
    setShowDeleteConfirm(true);
  };

  /**
   * Handle todo deletion confirmation
   */
  const handleDeleteConfirm = async () => {
    setShowDeleteConfirm(false);
    
    try {
      setIsDeleting(true);
      setError(null);
      await onDelete(todo.id);
    } catch (err) {
      console.error('Failed to delete todo:', err);
      setError('Failed to delete todo');
      setIsDeleting(false);
    }
  };

  /**
   * Handle delete cancellation
   */
  const handleDeleteCancel = () => {
    setShowDeleteConfirm(false);
  };

  /**
   * Handle edit button click
   */
  const handleEditClick = () => {
    if (isToggling || isDeleting || isUpdating) return;
    setIsEditing(true);
    setEditText(todo.text);
    setError(null);
  };

  /**
   * Handle edit save
   */
  const handleEditSave = async () => {
    const trimmedText = editText.trim();
    
    // Validation
    if (!trimmedText) {
      setError('Todo text cannot be empty');
      return;
    }

    if (trimmedText === todo.text) {
      // No changes, just exit edit mode
      setIsEditing(false);
      return;
    }

    if (trimmedText.length > 500) {
      setError('Todo text must be less than 500 characters');
      return;
    }

    try {
      setIsUpdating(true);
      setError(null);
      await onUpdate(todo.id, { text: trimmedText });
      setIsEditing(false);
    } catch (err) {
      console.error('Failed to update todo:', err);
      setError(err.message || 'Failed to update todo');
    } finally {
      setIsUpdating(false);
    }
  };

  /**
   * Handle edit cancel
   */
  const handleEditCancel = () => {
    setIsEditing(false);
    setEditText(todo.text);
    setError(null);
  };

  /**
   * Handle edit input change
   */
  const handleEditInputChange = (e) => {
    setEditText(e.target.value);
    if (error) setError(null);
  };

  /**
   * Handle edit input key press
   */
  const handleEditKeyPress = (e) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault();
      handleEditSave();
    } else if (e.key === 'Escape') {
      handleEditCancel();
    }
  };

  /**
   * Format creation date for display
   */
  const formatDate = (dateString) => {
    try {
      const date = new Date(dateString);
      return date.toLocaleDateString();
    } catch {
      return '';
    }
  };

  return (
    <div className={`todo-item ${todo.completed ? 'completed' : 'pending'}`}>
      <div className="todo-content">
        <button
          className={`toggle-button ${todo.completed ? 'completed' : ''}`}
          onClick={handleToggle}
          disabled={isToggling || isDeleting}
          aria-label={todo.completed ? 'Mark as pending' : 'Mark as completed'}
        >
          {isToggling ? '⏳' : (todo.completed ? '✅' : '⭕')}
        </button>
        
        {isEditing ? (
          <div className="todo-edit-container">
            <input
              type="text"
              value={editText}
              onChange={handleEditInputChange}
              onKeyDown={handleEditKeyPress}
              className="todo-edit-input"
              disabled={isUpdating}
              maxLength={500}
              autoFocus
            />
            <div className="edit-actions">
              <button
                className="edit-save-button"
                onClick={handleEditSave}
                disabled={isUpdating || !editText.trim()}
                aria-label="Save changes"
              >
                {isUpdating ? '⏳' : '💾'}
              </button>
              <button
                className="edit-cancel-button"
                onClick={handleEditCancel}
                disabled={isUpdating}
                aria-label="Cancel editing"
              >
                ✕
              </button>
            </div>
          </div>
        ) : (
          <div className="todo-text-container">
            <span className={`todo-text ${todo.completed ? 'completed' : ''}`}>
              {todo.text}
            </span>
            {todo.created_at && (
              <span className="todo-date">
                {formatDate(todo.created_at)}
              </span>
            )}
          </div>
        )}
        
        {!isEditing && (
          <>
            <button
              className="edit-button"
              onClick={handleEditClick}
              disabled={isToggling || isDeleting || isUpdating}
              aria-label="Edit todo"
            >
              ✏️
            </button>
            <button
              className="delete-button"
              onClick={handleDeleteClick}
              disabled={isToggling || isDeleting || isUpdating}
              aria-label="Delete todo"
            >
              {isDeleting ? '⏳' : '🗑️'}
            </button>
          </>
        )}
      </div>
      
      {error && (
        <div className="todo-error">
          <span className="error-message">{error}</span>
          <button 
            className="retry-button"
            onClick={() => setError(null)}
          >
            ✕
          </button>
        </div>
      )}

      <ConfirmDialog
        isOpen={showDeleteConfirm}
        title="Delete Todo"
        message={`Are you sure you want to delete "${todo.text}"? This action cannot be undone.`}
        confirmText="Delete"
        cancelText="Cancel"
        variant="danger"
        onConfirm={handleDeleteConfirm}
        onCancel={handleDeleteCancel}
      />
    </div>
  );
}

export default TodoItem;