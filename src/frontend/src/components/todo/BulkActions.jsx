import React, { useState } from 'react'
import { useTodo } from '../../context/TodoContext'
import ConfirmationDialog from './ConfirmationDialog'
import ProgressIndicator from './ProgressIndicator'
import styles from './BulkActions.module.css'

const BulkActions = ({ selectedIds }) => {
  const { state, actions } = useTodo()
  const { bulkOperation } = state
  const [showDeleteDialog, setShowDeleteDialog] = useState(false)
  const [showStatusDialog, setShowStatusDialog] = useState(false)
  const [pendingStatus, setPendingStatus] = useState(null)

  // Maximum 50 items validation
  const isOverLimit = selectedIds.length > 50
  const selectedCount = selectedIds.length

  const handleDeleteClick = () => {
    if (isOverLimit) {
      alert('You can only delete up to 50 items at once. Please select fewer items.')
      return
    }
    setShowDeleteDialog(true)
  }

  const handleStatusClick = (status) => {
    if (isOverLimit) {
      alert('You can only update up to 50 items at once. Please select fewer items.')
      return
    }
    setPendingStatus(status)
    setShowStatusDialog(true)
  }

  const handleConfirmDelete = async () => {
    try {
      await actions.bulkDeleteTodos(selectedIds)
      setShowDeleteDialog(false)
    } catch (error) {
      // Error is handled in the context
    }
  }

  const handleConfirmStatusUpdate = async () => {
    try {
      await actions.bulkUpdateTodoStatus(selectedIds, pendingStatus)
      setShowStatusDialog(false)
      setPendingStatus(null)
    } catch (error) {
      // Error is handled in the context
    }
  }

  const handleClearSelection = () => {
    actions.clearBulkSelection()
  }

  return (
    <div className={styles.bulkActions}>
      <div className={styles.bulkActionsContent}>
        <div className={styles.selectionInfo}>
          <span className={styles.selectedCount}>
            {selectedCount} item{selectedCount !== 1 ? 's' : ''} selected
          </span>
          {isOverLimit && (
            <span className={styles.limitWarning}>
              (Maximum 50 items allowed)
            </span>
          )}
        </div>

        <div className={styles.actionButtons}>
          <button
            className={`${styles.actionButton} ${styles.deleteButton}`}
            onClick={handleDeleteClick}
            disabled={bulkOperation.loading || isOverLimit}
            title={isOverLimit ? 'Too many items selected' : 'Delete selected todos'}
          >
            Delete Selected
          </button>

          <button
            className={`${styles.actionButton} ${styles.statusButton}`}
            onClick={() => handleStatusClick('completed')}
            disabled={bulkOperation.loading || isOverLimit}
            title={isOverLimit ? 'Too many items selected' : 'Mark selected as completed'}
          >
            Mark as Complete
          </button>

          <button
            className={`${styles.actionButton} ${styles.statusButton}`}
            onClick={() => handleStatusClick('pending')}
            disabled={bulkOperation.loading || isOverLimit}
            title={isOverLimit ? 'Too many items selected' : 'Mark selected as pending'}
          >
            Mark as Pending
          </button>

          <button
            className={`${styles.actionButton} ${styles.clearButton}`}
            onClick={handleClearSelection}
            disabled={bulkOperation.loading}
            title="Clear selection"
          >
            Clear Selection
          </button>
        </div>
      </div>

      {/* Progress Indicator for operations > 10 items */}
      {bulkOperation.loading && selectedCount > 10 && (
        <ProgressIndicator 
          progress={bulkOperation.progress}
          message={`Processing ${selectedCount} items...`}
        />
      )}

      {/* Error Display */}
      {bulkOperation.error && (
        <div className={styles.errorMessage}>
          {bulkOperation.error}
          <button 
            className={styles.dismissError}
            onClick={() => actions.setBulkOperationError(null)}
          >
            ×
          </button>
        </div>
      )}

      {/* Delete Confirmation Dialog */}
      {showDeleteDialog && (
        <ConfirmationDialog
          title="Confirm Delete"
          message={`Are you sure you want to delete ${selectedCount} todo${selectedCount !== 1 ? 's' : ''}? This action cannot be undone.`}
          confirmText="Delete"
          confirmClass="danger"
          onConfirm={handleConfirmDelete}
          onCancel={() => setShowDeleteDialog(false)}
          loading={bulkOperation.loading}
        />
      )}

      {/* Status Update Confirmation Dialog */}
      {showStatusDialog && (
        <ConfirmationDialog
          title="Confirm Status Update"
          message={`Are you sure you want to mark ${selectedCount} todo${selectedCount !== 1 ? 's' : ''} as ${pendingStatus}?`}
          confirmText={`Mark as ${pendingStatus}`}
          confirmClass="primary"
          onConfirm={handleConfirmStatusUpdate}
          onCancel={() => {
            setShowStatusDialog(false)
            setPendingStatus(null)
          }}
          loading={bulkOperation.loading}
        />
      )}
    </div>
  )
}

export default BulkActions