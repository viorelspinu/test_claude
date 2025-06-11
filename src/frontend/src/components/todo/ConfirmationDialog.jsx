import React from 'react'
import styles from './ConfirmationDialog.module.css'

const ConfirmationDialog = ({
  title,
  message,
  confirmText = 'Confirm',
  cancelText = 'Cancel',
  confirmClass = 'primary',
  onConfirm,
  onCancel,
  loading = false
}) => {
  return (
    <div className={styles.overlay}>
      <div className={styles.dialog}>
        <div className={styles.header}>
          <h3 className={styles.title}>{title}</h3>
        </div>

        <div className={styles.content}>
          <p className={styles.message}>{message}</p>
        </div>

        <div className={styles.footer}>
          <button
            className={`${styles.button} ${styles.cancelButton}`}
            onClick={onCancel}
            disabled={loading}
          >
            {cancelText}
          </button>
          
          <button
            className={`${styles.button} ${styles.confirmButton} ${styles[confirmClass]}`}
            onClick={onConfirm}
            disabled={loading}
          >
            {loading ? (
              <div className={styles.buttonContent}>
                <div className={styles.spinner}></div>
                Processing...
              </div>
            ) : (
              confirmText
            )}
          </button>
        </div>
      </div>
    </div>
  )
}

export default ConfirmationDialog