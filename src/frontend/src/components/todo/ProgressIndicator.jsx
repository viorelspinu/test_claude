import React from 'react'
import styles from './ProgressIndicator.module.css'

const ProgressIndicator = ({ progress = 0, message = 'Processing...' }) => {
  return (
    <div className={styles.progressContainer}>
      <div className={styles.progressMessage}>
        {message}
      </div>
      
      <div className={styles.progressBar}>
        <div 
          className={styles.progressFill}
          style={{ width: `${Math.min(100, Math.max(0, progress))}%` }}
        />
      </div>
      
      <div className={styles.progressText}>
        {Math.round(progress)}%
      </div>
    </div>
  )
}

export default ProgressIndicator