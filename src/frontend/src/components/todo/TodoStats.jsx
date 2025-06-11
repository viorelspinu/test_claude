import React, { useEffect } from 'react'
import { useTodo } from '../../context/TodoContext'
import styles from './TodoStats.module.css'

const TodoStats = () => {
  const { state, actions } = useTodo()
  const { stats, loading } = state

  // Fetch stats on mount and when todos change
  useEffect(() => {
    actions.fetchStats()
  }, [state.todos])

  // Calculate completion percentage safely
  const completionPercentage = stats.total_count > 0 
    ? Math.round((stats.completed_count / stats.total_count) * 100) 
    : 0

  // Format the last updated time
  const formatLastUpdated = () => {
    const now = new Date()
    return now.toLocaleTimeString('en-US', { 
      hour: '2-digit', 
      minute: '2-digit',
      hour12: true 
    })
  }

  // Stat card component
  const StatCard = ({ title, value, color, icon }) => (
    <div className={`${styles.statCard} ${styles[color]}`}>
      <div className={styles.statIcon}>{icon}</div>
      <div className={styles.statContent}>
        <h4 className={styles.statTitle}>{title}</h4>
        <p className={styles.statValue}>{value}</p>
      </div>
    </div>
  )

  if (loading && !stats.total_count) {
    return (
      <div className={styles.statsContainer}>
        <div className={styles.loadingState}>
          <div className={styles.spinner}></div>
          <p>Loading statistics...</p>
        </div>
      </div>
    )
  }

  return (
    <div className={styles.statsContainer}>
      <div className={styles.statsHeader}>
        <h3 className={styles.title}>Todo Statistics</h3>
        <span className={styles.lastUpdated}>
          Last updated: {formatLastUpdated()}
        </span>
      </div>

      <div className={styles.statsGrid}>
        <StatCard
          title="Total Tasks"
          value={stats.total_count}
          color="gray"
          icon="📋"
        />
        <StatCard
          title="Completed"
          value={stats.completed_count}
          color="green"
          icon="✅"
        />
        <StatCard
          title="Pending"
          value={stats.pending_count}
          color="blue"
          icon="⏳"
        />
        <StatCard
          title="Overdue"
          value={stats.overdue_count}
          color="red"
          icon="⚠️"
        />
      </div>

      <div className={styles.completionSection}>
        <div className={styles.completionHeader}>
          <h4 className={styles.completionTitle}>Completion Rate</h4>
          <span className={styles.completionPercentage}>{completionPercentage}%</span>
        </div>
        <div className={styles.progressBarContainer}>
          <div 
            className={styles.progressBar} 
            style={{ width: `${completionPercentage}%` }}
            aria-valuenow={completionPercentage}
            aria-valuemin="0"
            aria-valuemax="100"
            role="progressbar"
          >
            <span className={styles.progressBarText}>
              {completionPercentage > 10 && `${completionPercentage}%`}
            </span>
          </div>
        </div>
        <p className={styles.completionSummary}>
          {stats.completed_count} of {stats.total_count} tasks completed
        </p>
      </div>

      {stats.overdue_count > 0 && (
        <div className={styles.alert}>
          <span className={styles.alertIcon}>⚠️</span>
          <p className={styles.alertText}>
            You have {stats.overdue_count} overdue {stats.overdue_count === 1 ? 'task' : 'tasks'} that need attention
          </p>
        </div>
      )}
    </div>
  )
}

export default TodoStats