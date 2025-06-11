import React, { useState } from 'react';

function TodoItem({ todo, onToggle, onDelete, onEdit, disabled = false }) {
  const [isUpdating, setIsUpdating] = useState(false);
  const [isDeleting, setIsDeleting] = useState(false);
  const [isEditing, setIsEditing] = useState(false);
  const [editText, setEditText] = useState(todo.text);
  const formattedDate = new Date(todo.created_at).toLocaleDateString();

  const handleToggle = async () => {
    setIsUpdating(true);
    try {
      await onToggle(todo.id, !todo.completed);
    } catch (error) {
      console.error('Failed to toggle todo:', error);
    } finally {
      setIsUpdating(false);
    }
  };

  const handleDelete = async () => {
    if (window.confirm('Are you sure you want to delete this todo?')) {
      setIsDeleting(true);
      try {
        await onDelete(todo.id);
      } catch (error) {
        console.error('Failed to delete todo:', error);
        setIsDeleting(false);
      }
    }
  };

  const handleEdit = () => {
    if (!disabled) {
      setIsEditing(true);
      setEditText(todo.text);
    }
  };

  const handleSave = async () => {
    const trimmedText = editText.trim();
    if (!trimmedText) {
      // Just focus back to input instead of alert
      return;
    }
    if (trimmedText.length > 200) {
      // Just trim to 200 chars instead of alert
      setEditText(trimmedText.substring(0, 200));
      return;
    }
    if (trimmedText === todo.text) {
      setIsEditing(false);
      return;
    }

    setIsUpdating(true);
    try {
      await onEdit(todo.id, trimmedText);
      setIsEditing(false);
    } catch (error) {
      console.error('Failed to edit todo:', error);
      // Error will be handled by parent component's toast
    } finally {
      setIsUpdating(false);
    }
  };

  const handleCancel = () => {
    setIsEditing(false);
    setEditText(todo.text);
  };

  const handleKeyDown = (e) => {
    if (e.key === 'Enter') {
      e.preventDefault();
      handleSave();
    } else if (e.key === 'Escape') {
      e.preventDefault();
      handleCancel();
    }
  };

  const handleBlur = () => {
    // Auto-save on blur for modern UX
    const trimmedText = editText.trim();
    if (trimmedText && trimmedText !== todo.text) {
      handleSave();
    } else {
      handleCancel();
    }
  };

  return (
    <li className={`todo-item ${todo.completed ? 'completed' : ''}`}>
      <div className="todo-content">
        <div className="todo-main">
          <button 
            className={`toggle-btn ${todo.completed ? 'completed' : ''}`}
            onClick={handleToggle}
            disabled={isUpdating || isDeleting || disabled}
            title={disabled ? 'Offline - cannot modify' : (todo.completed ? 'Mark as incomplete' : 'Mark as complete')}
          >
            {isUpdating ? '...' : todo.completed ? '✓' : '○'}
          </button>
          {isEditing ? (
            <div className="todo-edit-container">
              <input
                type="text"
                value={editText}
                onChange={(e) => setEditText(e.target.value)}
                onKeyDown={handleKeyDown}
                onBlur={handleBlur}
                className="todo-edit-input"
                disabled={isUpdating}
                autoFocus
                maxLength={200}
                placeholder="Enter todo text..."
              />
              <div className="edit-hint">
                {editText.length}/200 • Enter to save • Esc to cancel
              </div>
            </div>
          ) : (
            <span 
              className={`todo-text ${disabled ? '' : 'editable'}`}
              onClick={handleEdit}
              title={disabled ? '' : 'Click to edit'}
            >
              {todo.text}
            </span>
          )}
        </div>
        <div className="todo-meta">
          <span className="todo-date">Created: {formattedDate}</span>
          <div className="todo-actions">
            {isEditing ? (
              <div className="editing-indicator">
                {isUpdating ? (
                  <span className="saving-indicator">💾 Saving...</span>
                ) : (
                  <span className="edit-mode-indicator">✏️ Editing</span>
                )}
              </div>
            ) : (
              <>
                <span className={`todo-status ${todo.completed ? 'completed' : 'pending'}`}>
                  {todo.completed ? 'Completed' : 'Pending'}
                </span>
                <button 
                  className="delete-btn"
                  onClick={handleDelete}
                  disabled={isUpdating || isDeleting || disabled}
                  title={disabled ? 'Offline - cannot delete' : 'Delete todo'}
                >
                  {isDeleting ? '...' : '🗑️'}
                </button>
              </>
            )}
          </div>
        </div>
      </div>
    </li>
  );
}

export default TodoItem;