import React, { useState, useMemo } from 'react';
import TaskItem from './TaskItem.js';
import TaskForm from './TaskForm.js';
import { 
  SORT_OPTIONS, 
  SORT_ORDER, 
  FILTER_OPTIONS, 
  PRIORITY_OPTIONS, 
  MESSAGES 
} from '../../utils/constants.js';
import { sortTasks, filterTasks, calculateTaskStats } from '../../utils/formatters.js';
import './TaskList.css';

const TaskList = ({ 
  tasks = [], 
  loading = false,
  error = null,
  onTaskCreate,
  onTaskUpdate,
  onTaskDelete,
  onRefresh 
}) => {
  // Local state for filtering and sorting
  const [filters, setFilters] = useState({
    status: FILTER_OPTIONS.ALL,
    priority: '',
    search: ''
  });
  
  const [sorting, setSorting] = useState({
    sortBy: SORT_OPTIONS.CREATED_AT,
    order: SORT_ORDER.DESC
  });
  
  const [viewMode, setViewMode] = useState('list'); // 'list' or 'grid'
  const [editingTask, setEditingTask] = useState(null);
  const [showCreateForm, setShowCreateForm] = useState(false);

  // Memoized filtered and sorted tasks
  const processedTasks = useMemo(() => {
    let result = [...tasks];
    
    // Apply filters
    const filterCriteria = {};
    
    if (filters.status !== FILTER_OPTIONS.ALL) {
      filterCriteria.completed = filters.status === FILTER_OPTIONS.COMPLETED;
    }
    
    if (filters.priority) {
      filterCriteria.priority = filters.priority;
    }
    
    if (filters.search) {
      filterCriteria.search = filters.search;
    }
    
    result = filterTasks(result, filterCriteria);
    
    // Apply sorting
    result = sortTasks(result, sorting.sortBy, sorting.order);
    
    return result;
  }, [tasks, filters, sorting]);

  // Calculate statistics
  const stats = useMemo(() => calculateTaskStats(tasks), [tasks]);
  const filteredStats = useMemo(() => calculateTaskStats(processedTasks), [processedTasks]);

  // Handle filter changes
  const handleFilterChange = (filterType, value) => {
    setFilters(prev => ({
      ...prev,
      [filterType]: value
    }));
  };

  // Handle sort changes
  const handleSortChange = (sortBy) => {
    setSorting(prev => ({
      sortBy,
      order: prev.sortBy === sortBy && prev.order === SORT_ORDER.ASC 
        ? SORT_ORDER.DESC 
        : SORT_ORDER.ASC
    }));
  };

  // Handle task creation
  const handleTaskCreate = async (taskData) => {
    try {
      await onTaskCreate(taskData);
      setShowCreateForm(false);
    } catch (error) {
      console.error('Error creating task:', error);
      throw error; // Re-throw to let form handle it
    }
  };

  // Handle task update
  const handleTaskUpdate = async (taskId, updates) => {
    try {
      await onTaskUpdate(taskId, updates);
      
      // Close edit form if this was the task being edited
      if (editingTask && editingTask.id === taskId) {
        setEditingTask(null);
      }
    } catch (error) {
      console.error('Error updating task:', error);
      throw error;
    }
  };

  // Handle task deletion
  const handleTaskDelete = async (taskId) => {
    try {
      await onTaskDelete(taskId);
      
      // Close edit form if this was the task being edited
      if (editingTask && editingTask.id === taskId) {
        setEditingTask(null);
      }
    } catch (error) {
      console.error('Error deleting task:', error);
      throw error;
    }
  };

  // Handle edit task
  const handleEditTask = (task) => {
    setEditingTask(task);
    setShowCreateForm(false);
  };

  // Handle cancel edit
  const handleCancelEdit = () => {
    setEditingTask(null);
  };

  // Clear all filters
  const clearFilters = () => {
    setFilters({
      status: FILTER_OPTIONS.ALL,
      priority: '',
      search: ''
    });
  };

  // Check if any filters are active
  const hasActiveFilters = filters.status !== FILTER_OPTIONS.ALL || 
                          filters.priority !== '' || 
                          filters.search !== '';

  return (
    <div className="task-list-container">
      {/* Task List Header */}
      <div className="task-list-header">
        <div className="header-top">
          <div className="header-title">
            <h2>Tasks</h2>
            <div className="task-count">
              {hasActiveFilters ? (
                <span>
                  Showing {filteredStats.total} of {stats.total} tasks
                </span>
              ) : (
                <span>{stats.total} tasks</span>
              )}
            </div>
          </div>
          
          <div className="header-actions">
            <button
              className="btn btn-primary"
              onClick={() => {
                setShowCreateForm(true);
                setEditingTask(null);
              }}
            >
              + Add Task
            </button>
            
            {onRefresh && (
              <button
                className="btn btn-secondary"
                onClick={onRefresh}
                disabled={loading}
                title="Refresh tasks"
              >
                {loading ? '⟳' : '↻'}
              </button>
            )}
          </div>
        </div>

        {/* Task Statistics */}
        <div className="task-stats">
          <div className="stat-item">
            <span className="stat-label">Total:</span>
            <span className="stat-value">{stats.total}</span>
          </div>
          <div className="stat-item">
            <span className="stat-label">Completed:</span>
            <span className="stat-value">{stats.completed}</span>
          </div>
          <div className="stat-item">
            <span className="stat-label">Remaining:</span>
            <span className="stat-value">{stats.incomplete}</span>
          </div>
          <div className="stat-item">
            <span className="stat-label">Progress:</span>
            <span className="stat-value">{stats.completionRate}%</span>
          </div>
        </div>
      </div>

      {/* Filters and Controls */}
      <div className="task-controls">
        <div className="filters">
          {/* Search Filter */}
          <div className="filter-group">
            <input
              type="text"
              placeholder="Search tasks..."
              value={filters.search}
              onChange={(e) => handleFilterChange('search', e.target.value)}
              className="search-input"
            />
          </div>

          {/* Status Filter */}
          <div className="filter-group">
            <select
              value={filters.status}
              onChange={(e) => handleFilterChange('status', e.target.value)}
              className="filter-select"
            >
              <option value={FILTER_OPTIONS.ALL}>All Tasks</option>
              <option value={FILTER_OPTIONS.COMPLETED}>Completed</option>
              <option value={FILTER_OPTIONS.INCOMPLETE}>Incomplete</option>
            </select>
          </div>

          {/* Priority Filter */}
          <div className="filter-group">
            <select
              value={filters.priority}
              onChange={(e) => handleFilterChange('priority', e.target.value)}
              className="filter-select"
            >
              <option value="">All Priorities</option>
              {PRIORITY_OPTIONS.map(option => (
                <option key={option.value} value={option.value}>
                  {option.label}
                </option>
              ))}
            </select>
          </div>

          {/* Clear Filters */}
          {hasActiveFilters && (
            <button
              className="btn btn-outline"
              onClick={clearFilters}
            >
              Clear Filters
            </button>
          )}
        </div>

        <div className="sort-controls">
          {/* Sort Options */}
          <div className="sort-group">
            <span className="sort-label">Sort by:</span>
            <div className="sort-buttons">
              {Object.entries(SORT_OPTIONS).map(([key, value]) => (
                <button
                  key={key}
                  className={`sort-btn ${sorting.sortBy === value ? 'active' : ''}`}
                  onClick={() => handleSortChange(value)}
                >
                  {key.replace('_', ' ')}
                  {sorting.sortBy === value && (
                    <span className="sort-order">
                      {sorting.order === SORT_ORDER.ASC ? '↑' : '↓'}
                    </span>
                  )}
                </button>
              ))}
            </div>
          </div>

          {/* View Mode Toggle */}
          <div className="view-toggle">
            <button
              className={`view-btn ${viewMode === 'list' ? 'active' : ''}`}
              onClick={() => setViewMode('list')}
              title="List view"
            >
              ☰
            </button>
            <button
              className={`view-btn ${viewMode === 'grid' ? 'active' : ''}`}
              onClick={() => setViewMode('grid')}
              title="Grid view"
            >
              ⊞
            </button>
          </div>
        </div>
      </div>

      {/* Create Task Form */}
      {showCreateForm && (
        <div className="task-form-section">
          <TaskForm
            onSubmit={handleTaskCreate}
            onCancel={() => setShowCreateForm(false)}
            isEditing={false}
          />
        </div>
      )}

      {/* Edit Task Form */}
      {editingTask && (
        <div className="task-form-section">
          <TaskForm
            onSubmit={(updates) => handleTaskUpdate(editingTask.id, updates)}
            onCancel={handleCancelEdit}
            initialTask={editingTask}
            isEditing={true}
          />
        </div>
      )}

      {/* Task List Content */}
      <div className="task-list-content">
        {/* Loading State */}
        {loading && (
          <div className="loading-state">
            <div className="spinner large"></div>
            <p>{MESSAGES.LOADING}</p>
          </div>
        )}

        {/* Error State */}
        {error && (
          <div className="error-state">
            <div className="error-icon">⚠️</div>
            <p>Error loading tasks: {error}</p>
            {onRefresh && (
              <button className="btn btn-primary" onClick={onRefresh}>
                Try Again
              </button>
            )}
          </div>
        )}

        {/* Empty State */}
        {!loading && !error && tasks.length === 0 && (
          <div className="empty-state">
            <div className="empty-icon">📝</div>
            <h3>No tasks yet</h3>
            <p>{MESSAGES.EMPTY_LIST}</p>
            <button
              className="btn btn-primary"
              onClick={() => setShowCreateForm(true)}
            >
              Create Your First Task
            </button>
          </div>
        )}

        {/* Filtered Empty State */}
        {!loading && !error && tasks.length > 0 && processedTasks.length === 0 && (
          <div className="empty-state">
            <div className="empty-icon">🔍</div>
            <h3>No tasks match your filters</h3>
            <p>Try adjusting your search criteria or clearing filters.</p>
            <button className="btn btn-outline" onClick={clearFilters}>
              Clear All Filters
            </button>
          </div>
        )}

        {/* Task Items */}
        {!loading && !error && processedTasks.length > 0 && (
          <div className={`task-items ${viewMode}`}>
            {processedTasks.map(task => (
              <TaskItem
                key={task.id}
                task={task}
                onUpdate={handleTaskUpdate}
                onDelete={handleTaskDelete}
                onEdit={handleEditTask}
                isEditing={editingTask && editingTask.id === task.id}
              />
            ))}
          </div>
        )}
      </div>
    </div>
  );
};

export default TaskList;