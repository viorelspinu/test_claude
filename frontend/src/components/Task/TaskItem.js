import React, { useState } from 'react';
import { formatDate, formatRelativeTime, formatPriority, formatStatus, truncateText } from '../../utils/formatters.js';
import { MESSAGES } from '../../utils/constants.js';
import './TaskItem.css';

const TaskItem = ({ 
  task, 
  onUpdate, 
  onDelete, 
  onEdit,
  isEditing = false 
}) => {
  const [isExpanded, setIsExpanded] = useState(false);
  const [isUpdating, setIsUpdating] = useState(false);
  const [showDeleteConfirm, setShowDeleteConfirm] = useState(false);

  const priorityInfo = formatPriority(task.priority);
  const statusInfo = formatStatus(task.completed, task.completed_at);

  // Handle task completion toggle
  const handleToggleComplete = async () => {
    if (isUpdating) return;
    
    setIsUpdating(true);
    try {
      await onUpdate(task.id, { completed: !task.completed });
    } catch (error) {
      console.error('Error toggling task completion:', error);
    } finally {
      setIsUpdating(false);
    }
  };

  // Handle task deletion
  const handleDelete = async () => {
    if (isUpdating) return;
    
    setIsUpdating(true);
    try {
      await onDelete(task.id);
      setShowDeleteConfirm(false);
    } catch (error) {
      console.error('Error deleting task:', error);
      setIsUpdating(false);
    }
  };

  // Handle edit button click
  const handleEdit = () => {
    if (onEdit) {
      onEdit(task);
    }
  };

  // Toggle expanded view for long descriptions
  const toggleExpanded = () => {
    setIsExpanded(!isExpanded);
  };

  const shouldTruncateDescription = task.description && task.description.length > 150;
  const displayDescription = shouldTruncateDescription && !isExpanded 
    ? truncateText(task.description, 150)
    : task.description;

  return (
    <div className={`task-item ${task.completed ? 'completed' : ''} ${isEditing ? 'editing' : ''}`}>
      {/* Task Header */}
      <div className="task-header">
        <div className="task-main-content">
          {/* Completion Checkbox */}
          <button
            className={`task-checkbox ${task.completed ? 'checked' : ''}`}
            onClick={handleToggleComplete}
            disabled={isUpdating}
            aria-label={task.completed ? 'Mark as incomplete' : 'Mark as complete'}
          >
            {task.completed && <span className="checkmark">✓</span>}
          </button>

          {/* Task Title */}
          <div className="task-title-section">
            <h3 className={`task-title ${task.completed ? 'completed-text' : ''}`}>
              {task.title}
            </h3>
            
            {/* Task Meta Information */}
            <div className="task-meta">
              <span className={`priority-badge ${priorityInfo.className}`}>
                {priorityInfo.text}
              </span>
              <span className={`status-badge ${statusInfo.className}`}>
                {statusInfo.text}
              </span>
              <span className="task-date" title={formatDate(task.created_at)}>
                Created {formatRelativeTime(task.created_at)}
              </span>
              {task.updated_at !== task.created_at && (
                <span className="task-date" title={formatDate(task.updated_at)}>
                  Updated {formatRelativeTime(task.updated_at)}
                </span>
              )}
            </div>
          </div>
        </div>

        {/* Action Buttons */}
        <div className="task-actions">
          {!isEditing && (
            <>
              <button
                className="action-btn edit-btn"
                onClick={handleEdit}
                disabled={isUpdating}
                title="Edit task"
                aria-label="Edit task"
              >
                <span className="icon">✏️</span>
              </button>
              
              <button
                className="action-btn delete-btn"
                onClick={() => setShowDeleteConfirm(true)}
                disabled={isUpdating}
                title="Delete task"
                aria-label="Delete task"
              >
                <span className="icon">🗑️</span>
              </button>
            </>
          )}
          
          {isUpdating && (
            <div className="updating-indicator">
              <span className="spinner"></span>
            </div>
          )}
        </div>
      </div>

      {/* Task Description */}
      {task.description && (
        <div className="task-description">
          <p className={task.completed ? 'completed-text' : ''}>
            {displayDescription}
          </p>
          
          {shouldTruncateDescription && (
            <button
              className="expand-btn"
              onClick={toggleExpanded}
              aria-label={isExpanded ? 'Show less' : 'Show more'}
            >
              {isExpanded ? 'Show less' : 'Show more'}
            </button>
          )}
        </div>
      )}

      {/* Task Timestamps (expanded view) */}
      {isExpanded && (
        <div className="task-timestamps">
          <div className="timestamp-row">
            <span className="timestamp-label">Created:</span>
            <span className="timestamp-value">{formatDate(task.created_at)}</span>
          </div>
          
          {task.updated_at !== task.created_at && (
            <div className="timestamp-row">
              <span className="timestamp-label">Updated:</span>
              <span className="timestamp-value">{formatDate(task.updated_at)}</span>
            </div>
          )}
          
          {task.completed && task.completed_at && (
            <div className="timestamp-row">
              <span className="timestamp-label">Completed:</span>
              <span className="timestamp-value">{formatDate(task.completed_at)}</span>
            </div>
          )}
        </div>
      )}

      {/* Delete Confirmation Modal */}
      {showDeleteConfirm && (
        <div className="delete-confirm-overlay">
          <div className="delete-confirm-modal">
            <h4>Confirm Delete</h4>
            <p>{MESSAGES.CONFIRM_DELETE}</p>
            <p className="task-title-preview">"{task.title}"</p>
            
            <div className="confirm-actions">
              <button
                className="confirm-btn cancel-btn"
                onClick={() => setShowDeleteConfirm(false)}
                disabled={isUpdating}
              >
                Cancel
              </button>
              <button
                className="confirm-btn delete-btn"
                onClick={handleDelete}
                disabled={isUpdating}
              >
                {isUpdating ? 'Deleting...' : 'Delete'}
              </button>
            </div>
          </div>
        </div>
      )}
    </div>
  );
};

export default TaskItem;