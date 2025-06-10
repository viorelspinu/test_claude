// Utility functions for formatting data in the Todo List App

/**
 * Format date string to human-readable format
 * @param {string} dateString - ISO 8601 date string
 * @param {object} options - Intl.DateTimeFormat options
 * @returns {string} Formatted date string
 */
export const formatDate = (dateString, options = {}) => {
  if (!dateString) return '';
  
  const date = new Date(dateString);
  
  // Default options for date formatting
  const defaultOptions = {
    year: 'numeric',
    month: 'short',
    day: 'numeric',
    hour: '2-digit',
    minute: '2-digit',
    ...options
  };
  
  return new Intl.DateTimeFormat('en-US', defaultOptions).format(date);
};

/**
 * Format date to relative time (e.g., "2 hours ago", "3 days ago")
 * @param {string} dateString - ISO 8601 date string
 * @returns {string} Relative time string
 */
export const formatRelativeTime = (dateString) => {
  if (!dateString) return '';
  
  const date = new Date(dateString);
  const now = new Date();
  const diffInSeconds = Math.floor((now - date) / 1000);
  
  // Define time intervals in seconds
  const intervals = [
    { label: 'year', seconds: 31536000 },
    { label: 'month', seconds: 2592000 },
    { label: 'week', seconds: 604800 },
    { label: 'day', seconds: 86400 },
    { label: 'hour', seconds: 3600 },
    { label: 'minute', seconds: 60 }
  ];
  
  for (const interval of intervals) {
    const count = Math.floor(diffInSeconds / interval.seconds);
    if (count > 0) {
      return `${count} ${interval.label}${count !== 1 ? 's' : ''} ago`;
    }
  }
  
  return 'just now';
};

/**
 * Format task priority with appropriate styling class
 * @param {string} priority - Priority level (High, Medium, Low)
 * @returns {object} Object with display text and CSS class
 */
export const formatPriority = (priority) => {
  const priorityMap = {
    'High': { text: 'High', className: 'priority-high', color: '#c62828' },
    'Medium': { text: 'Medium', className: 'priority-medium', color: '#ef6c00' },
    'Low': { text: 'Low', className: 'priority-low', color: '#2e7d32' }
  };
  
  return priorityMap[priority] || { 
    text: priority, 
    className: 'priority-unknown', 
    color: '#7f8c8d' 
  };
};

/**
 * Format task status for display
 * @param {boolean} completed - Task completion status
 * @param {string} completedAt - Completion timestamp
 * @returns {object} Status information with text and styling
 */
export const formatStatus = (completed, completedAt = null) => {
  if (completed) {
    return {
      text: 'Completed',
      className: 'status-completed',
      detail: completedAt ? `Completed ${formatRelativeTime(completedAt)}` : 'Completed'
    };
  }
  
  return {
    text: 'Pending',
    className: 'status-pending',
    detail: 'In progress'
  };
};

/**
 * Truncate text to specified length with ellipsis
 * @param {string} text - Text to truncate
 * @param {number} maxLength - Maximum length before truncation
 * @returns {string} Truncated text
 */
export const truncateText = (text, maxLength = 100) => {
  if (!text || text.length <= maxLength) return text || '';
  
  return text.substring(0, maxLength).trim() + '...';
};

/**
 * Validate and sanitize task data
 * @param {object} taskData - Raw task data
 * @returns {object} Sanitized task data
 */
export const sanitizeTaskData = (taskData) => {
  return {
    ...taskData,
    title: taskData.title?.trim() || '',
    description: taskData.description?.trim() || null,
    priority: taskData.priority || 'Medium',
    completed: Boolean(taskData.completed)
  };
};

/**
 * Calculate task statistics
 * @param {array} tasks - Array of task objects
 * @returns {object} Task statistics
 */
export const calculateTaskStats = (tasks) => {
  const total = tasks.length;
  const completed = tasks.filter(task => task.completed).length;
  const incomplete = total - completed;
  
  const byPriority = tasks.reduce((acc, task) => {
    acc[task.priority] = (acc[task.priority] || 0) + 1;
    return acc;
  }, {});
  
  return {
    total,
    completed,
    incomplete,
    completionRate: total > 0 ? Math.round((completed / total) * 100) : 0,
    byPriority: {
      High: byPriority.High || 0,
      Medium: byPriority.Medium || 0,
      Low: byPriority.Low || 0
    }
  };
};

/**
 * Sort tasks based on criteria
 * @param {array} tasks - Array of tasks
 * @param {string} sortBy - Sort criteria (created_at, updated_at, title, priority)
 * @param {string} order - Sort order (asc, desc)
 * @returns {array} Sorted tasks array
 */
export const sortTasks = (tasks, sortBy = 'created_at', order = 'desc') => {
  // Filter out invalid tasks before sorting
  const validTasks = tasks.filter(task => {
    if (!task || typeof task.id === 'undefined' || task.id === null) {
      console.warn('Sorting: filtering out task without valid ID:', task);
      return false;
    }
    return true;
  });
  
  const sortedTasks = [...validTasks].sort((a, b) => {
    let valueA, valueB;
    
    switch (sortBy) {
      case 'title':
        valueA = a.title.toLowerCase();
        valueB = b.title.toLowerCase();
        return order === 'asc' 
          ? valueA.localeCompare(valueB)
          : valueB.localeCompare(valueA);
      
      case 'priority':
        const priorityOrder = { 'High': 3, 'Medium': 2, 'Low': 1 };
        valueA = priorityOrder[a.priority] || 0;
        valueB = priorityOrder[b.priority] || 0;
        return order === 'asc' ? valueA - valueB : valueB - valueA;
      
      case 'created_at':
      case 'updated_at':
        valueA = new Date(a[sortBy]);
        valueB = new Date(b[sortBy]);
        return order === 'asc' ? valueA - valueB : valueB - valueA;
      
      default:
        return 0;
    }
  });
  
  return sortedTasks;
};

/**
 * Filter tasks based on criteria
 * @param {array} tasks - Array of tasks
 * @param {object} filters - Filter criteria
 * @returns {array} Filtered tasks array
 */
export const filterTasks = (tasks, filters = {}) => {
  return tasks.filter(task => {
    // Validate task has required properties
    if (!task || typeof task.id === 'undefined' || task.id === null) {
      console.warn('Filtering out task without valid ID:', task);
      return false;
    }
    // Filter by completion status
    if (filters.completed !== undefined) {
      const isCompleted = filters.completed === 'true' || filters.completed === true;
      if (task.completed !== isCompleted) return false;
    }
    
    // Filter by priority
    if (filters.priority && task.priority !== filters.priority) {
      return false;
    }
    
    // Filter by search term
    if (filters.search) {
      const searchTerm = filters.search.toLowerCase();
      const titleMatch = task.title.toLowerCase().includes(searchTerm);
      const descriptionMatch = task.description && 
        task.description.toLowerCase().includes(searchTerm);
      
      if (!titleMatch && !descriptionMatch) return false;
    }
    
    return true;
  });
};