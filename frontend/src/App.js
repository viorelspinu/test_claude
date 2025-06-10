import React, { useState, useEffect } from 'react';
import TaskList from './components/Task/TaskList.js';
import useTasks from './hooks/useTasks.js';
import { MESSAGES } from './utils/constants.js';
import './App.css';

const App = () => {
  // Use the custom hook for task management
  const {
    tasks,
    stats,
    isLoading,
    error,
    createTask,
    updateTask,
    deleteTask,
    refresh,
    clearError
  } = useTasks();

  // Local state for notifications
  const [notification, setNotification] = useState(null);

  // Handle task creation
  const handleTaskCreate = async (taskData) => {
    try {
      await createTask(taskData);
      showNotification(MESSAGES.SUCCESS_CREATE, 'success');
    } catch (error) {
      console.error('Error creating task:', error);
      showNotification(error.message || MESSAGES.ERROR_GENERIC, 'error');
      throw error; // Re-throw to let form handle validation errors
    }
  };

  // Handle task update
  const handleTaskUpdate = async (taskId, updates) => {
    try {
      await updateTask(taskId, updates);
      showNotification(MESSAGES.SUCCESS_UPDATE, 'success');
    } catch (error) {
      console.error('Error updating task:', error);
      showNotification(error.message || MESSAGES.ERROR_GENERIC, 'error');
      throw error;
    }
  };

  // Handle task deletion
  const handleTaskDelete = async (taskId) => {
    try {
      await deleteTask(taskId);
      showNotification(MESSAGES.SUCCESS_DELETE, 'success');
    } catch (error) {
      console.error('Error deleting task:', error);
      showNotification(error.message || MESSAGES.ERROR_GENERIC, 'error');
      throw error;
    }
  };

  // Handle refresh
  const handleRefresh = async () => {
    try {
      await refresh();
      clearError();
    } catch (error) {
      console.error('Error refreshing tasks:', error);
    }
  };

  // Show notification
  const showNotification = (message, type = 'info') => {
    setNotification({ message, type });
    
    // Auto-dismiss notification after 5 seconds
    setTimeout(() => {
      setNotification(null);
    }, 5000);
  };

  // Dismiss notification
  const dismissNotification = () => {
    setNotification(null);
  };

  // Clear error when component mounts
  useEffect(() => {
    clearError();
  }, [clearError]);

  return (
    <div className="app">
      {/* Notification System */}
      {notification && (
        <div className={`notification ${notification.type}`}>
          <span className="notification-message">{notification.message}</span>
          <button 
            className="notification-close"
            onClick={dismissNotification}
            aria-label="Dismiss notification"
          >
            ×
          </button>
        </div>
      )}

      {/* Application Header */}
      <header className="app-header">
        <div className="header-content">
          <div className="header-title">
            <h1>Todo List Application</h1>
            <p className="app-subtitle">Organize your tasks efficiently</p>
          </div>
          
          <div className="header-stats">
            <div className="stat-card">
              <span className="stat-number">{stats.total}</span>
              <span className="stat-label">Total</span>
            </div>
            <div className="stat-card">
              <span className="stat-number">{stats.completed}</span>
              <span className="stat-label">Completed</span>
            </div>
            <div className="stat-card">
              <span className="stat-number">{stats.incomplete}</span>
              <span className="stat-label">Remaining</span>
            </div>
            <div className="stat-card">
              <span className="stat-number">{stats.completionRate || 0}%</span>
              <span className="stat-label">Progress</span>
            </div>
          </div>
        </div>

        {/* Progress Bar */}
        {stats.total > 0 && (
          <div className="progress-container">
            <div className="progress-bar">
              <div 
                className="progress-fill"
                style={{ width: `${stats.completionRate || 0}%` }}
              ></div>
            </div>
            <span className="progress-text">
              {stats.completed} of {stats.total} tasks completed
            </span>
          </div>
        )}
      </header>

      {/* Main Content */}
      <main className="app-main">
        <div className="app-container">
          {/* Error Display */}
          {error && (
            <div className="error-banner">
              <div className="error-content">
                <span className="error-icon">⚠️</span>
                <span className="error-message">
                  {error}
                </span>
                <button 
                  className="error-retry"
                  onClick={handleRefresh}
                  disabled={isLoading}
                >
                  {isLoading ? 'Retrying...' : 'Retry'}
                </button>
                <button 
                  className="error-dismiss"
                  onClick={clearError}
                >
                  ×
                </button>
              </div>
            </div>
          )}

          {/* Task List Component */}
          <TaskList
            tasks={tasks}
            loading={isLoading}
            error={null} // We handle errors at the app level
            onTaskCreate={handleTaskCreate}
            onTaskUpdate={handleTaskUpdate}
            onTaskDelete={handleTaskDelete}
            onRefresh={handleRefresh}
          />
        </div>
      </main>

      {/* Application Footer */}
      <footer className="app-footer">
        <div className="footer-content">
          <p>Todo List App - React + Flask Backend</p>
          <div className="footer-info">
            <span>Version 1.0.0</span>
            <span>•</span>
            <span>Built with React & Flask</span>
          </div>
        </div>
      </footer>
    </div>
  );
};

export default App;