import { useState, useEffect, useCallback, useMemo } from 'react';
import taskService from '../services/taskService.js';
import useApi from './useApi.js';
import { MESSAGES, DEFAULT_QUERY_PARAMS } from '../utils/constants.js';

/**
 * Custom hook for managing task state and operations
 * Provides comprehensive task management functionality
 */
const useTasks = (initialParams = {}) => {
  // Core state
  const [tasks, setTasks] = useState([]);
  const [stats, setStats] = useState({
    total: 0,
    completed: 0,
    incomplete: 0,
    byPriority: { High: 0, Medium: 0, Low: 0 }
  });
  
  // Query parameters for filtering and sorting
  const [queryParams, setQueryParams] = useState({
    ...DEFAULT_QUERY_PARAMS,
    ...initialParams
  });

  // API hooks for different operations
  const fetchApi = useApi();
  const createApi = useApi();
  const updateApi = useApi();
  const deleteApi = useApi();
  const statsApi = useApi();

  // Fetch tasks from API
  const fetchTasks = useCallback(async (params = {}) => {
    const mergedParams = { ...queryParams, ...params };
    
    return fetchApi.execute(
      () => taskService.getTasks(mergedParams),
      {
        successMessage: 'Tasks loaded successfully',
        errorMessage: 'Failed to load tasks'
      }
    );
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [queryParams]);

  // Create a new task
  const createTask = useCallback(async (taskData) => {
    const result = await createApi.execute(
      () => taskService.createTask(taskData),
      {
        successMessage: MESSAGES.SUCCESS_CREATE,
        errorMessage: 'Failed to create task',
        onError: (error) => {
          // Prevent infinite retries on error
          console.error('Task creation failed:', error);
        }
      }
    );

    if (result) {
      // Validate the created task has an ID before adding to state
      if (typeof result.id !== 'undefined' && result.id !== null) {
        // Add new task to local state
        setTasks(prev => [result, ...prev]);
      } else {
        console.error('Created task missing ID, not adding to local state:', result);
        // Refresh tasks from server to get the proper data
        fetchTasks();
      }
      
      // No need to refresh - we already have the new task in local state
    }

    return result;
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, []);

  // Update an existing task
  const updateTask = useCallback(async (taskId, updates) => {
    // Validate taskId
    if (typeof taskId === 'undefined' || taskId === null) {
      console.error('updateTask called with invalid taskId:', taskId);
      throw new Error('Task ID is required for update operation');
    }

    const result = await updateApi.execute(
      () => taskService.updateTask(taskId, updates),
      {
        successMessage: MESSAGES.SUCCESS_UPDATE,
        errorMessage: 'Failed to update task',
        onError: (error) => {
          // Prevent infinite retries on error
          console.error('Task update failed:', error);
        }
      }
    );

    if (result) {
      // Update task in local state
      setTasks(prev => 
        prev.map(task => 
          task.id === taskId ? result : task
        )
      );
    }

    return result;
  }, []);

  // Delete a task
  const deleteTask = useCallback(async (taskId) => {
    // Validate taskId
    if (typeof taskId === 'undefined' || taskId === null) {
      console.error('deleteTask called with invalid taskId:', taskId);
      throw new Error('Task ID is required for delete operation');
    }

    await deleteApi.execute(
      () => taskService.deleteTask(taskId),
      {
        successMessage: MESSAGES.SUCCESS_DELETE,
        errorMessage: 'Failed to delete task',
        onError: (error) => {
          // Prevent infinite retries on error
          console.error('Task deletion failed:', error);
        }
      }
    );

    // Remove task from local state
    setTasks(prev => prev.filter(task => task.id !== taskId));
  }, []);

  // Toggle task completion
  const toggleTaskCompletion = useCallback(async (taskId, completed) => {
    return updateTask(taskId, { completed });
  }, []);

  // Bulk update tasks
  const bulkUpdateTasks = useCallback(async (taskUpdates) => {
    const result = await updateApi.execute(
      () => taskService.bulkUpdateTasks(taskUpdates),
      {
        successMessage: 'Tasks updated successfully',
        errorMessage: 'Failed to update some tasks',
        onError: (error) => {
          console.error('Bulk update failed:', error);
        }
      }
    );

    if (result) {
      // No need to refresh - bulk updates should update local state individually
    }

    return result;
  }, []);

  // Mark all tasks as completed
  const completeAllTasks = useCallback(async () => {
    const incompleteTasks = tasks.filter(task => !task.completed);
    const updates = incompleteTasks.map(task => ({
      id: task.id,
      updates: { completed: true }
    }));

    if (updates.length > 0) {
      return bulkUpdateTasks(updates);
    }
  }, [tasks]);

  // Delete all completed tasks
  const deleteCompletedTasks = useCallback(async () => {
    const completedTasks = tasks.filter(task => task.completed);
    
    for (const task of completedTasks) {
      await deleteTask(task.id);
    }
  }, [tasks]);

  // Fetch task statistics
  const fetchStats = useCallback(async () => {
    return statsApi.execute(
      () => taskService.getTaskStats(),
      {
        errorMessage: 'Failed to load task statistics',
        onError: (error) => {
          console.error('Stats fetch failed:', error);
        }
      }
    );
  }, []);

  // Update query parameters
  const updateQueryParams = useCallback((newParams) => {
    setQueryParams(prev => ({ ...prev, ...newParams }));
  }, []);

  // Reset query parameters to defaults
  const resetQueryParams = useCallback(() => {
    setQueryParams(DEFAULT_QUERY_PARAMS);
  }, []);

  // Search tasks
  const searchTasks = useCallback(async (searchTerm) => {
    return fetchTasks({ search: searchTerm });
  }, []);

  // Filter tasks by status
  const filterByStatus = useCallback(async (completed) => {
    return fetchTasks({ completed: completed ? 'true' : 'false' });
  }, []);

  // Filter tasks by priority
  const filterByPriority = useCallback(async (priority) => {
    return fetchTasks({ priority });
  }, []);

  // Refresh all data
  const refresh = useCallback(async () => {
    await Promise.all([
      fetchTasks(),
      fetchStats()
    ]);
  }, []);

  // Calculate local statistics from current tasks
  const localStats = useMemo(() => {
    const total = tasks.length;
    const completed = tasks.filter(task => task.completed).length;
    const incomplete = total - completed;
    
    const byPriority = tasks.reduce((acc, task) => {
      acc[task.priority] = (acc[task.priority] || 0) + 1;
      return acc;
    }, { High: 0, Medium: 0, Low: 0 });

    return {
      total,
      completed,
      incomplete,
      completionRate: total > 0 ? Math.round((completed / total) * 100) : 0,
      byPriority
    };
  }, [tasks]);

  // Load initial data on mount or when query params change
  useEffect(() => {
    const loadTasks = async () => {
      const mergedParams = { ...queryParams };
      
      fetchApi.execute(
        () => taskService.getTasks(mergedParams),
        {
          successMessage: 'Tasks loaded successfully',
          errorMessage: 'Failed to load tasks'
        }
      );
    };
    
    loadTasks();
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [queryParams]);

  // Update tasks state when fetch succeeds
  useEffect(() => {
    if (fetchApi.data) {
      const tasksData = fetchApi.data.tasks || [];
      // Filter out any tasks without valid IDs
      const validTasks = tasksData.filter(task => 
        task && typeof task.id !== 'undefined' && task.id !== null
      );
      
      if (validTasks.length !== tasksData.length) {
        console.warn(`Filtered out ${tasksData.length - validTasks.length} tasks with invalid IDs in useTasks`);
      }
      
      setTasks(validTasks);
    }
  }, [fetchApi.data]);

  // Update stats state when stats fetch succeeds
  useEffect(() => {
    if (statsApi.data) {
      setStats(statsApi.data);
    } else {
      // Use local stats if API stats unavailable
      setStats(localStats);
    }
  }, [statsApi.data, localStats]);

  // Computed states
  const isLoading = fetchApi.loading || createApi.loading || updateApi.loading || deleteApi.loading;
  const hasError = fetchApi.error || createApi.error || updateApi.error || deleteApi.error;
  const isEmpty = !isLoading && tasks.length === 0;

  return {
    // Data
    tasks,
    stats,
    queryParams,
    localStats,

    // Loading states
    isLoading,
    isCreating: createApi.loading,
    isUpdating: updateApi.loading,
    isDeleting: deleteApi.loading,
    isFetching: fetchApi.loading,

    // Error states
    error: hasError,
    fetchError: fetchApi.error,
    createError: createApi.error,
    updateError: updateApi.error,
    deleteError: deleteApi.error,

    // Computed states
    isEmpty,
    hasData: tasks.length > 0,

    // Core operations
    fetchTasks,
    createTask,
    updateTask,
    deleteTask,
    refresh,

    // Convenience operations
    toggleTaskCompletion,
    bulkUpdateTasks,
    completeAllTasks,
    deleteCompletedTasks,

    // Query operations
    searchTasks,
    filterByStatus,
    filterByPriority,
    updateQueryParams,
    resetQueryParams,

    // Statistics
    fetchStats,

    // Error handling
    clearError: useCallback(() => {
      fetchApi.clearError();
      createApi.clearError();
      updateApi.clearError();
      deleteApi.clearError();
      statsApi.clearError();
      // eslint-disable-next-line react-hooks/exhaustive-deps
    }, [])
  };
};

/**
 * Hook for managing a single task's state
 * Useful for task detail views or forms
 */
export const useTask = (taskId = null) => {
  const [task, setTask] = useState(null);
  const api = useApi();

  const fetchTask = useCallback(async (id = taskId) => {
    if (!id) return null;
    
    const result = await api.execute(
      () => taskService.getTask(id),
      {
        errorMessage: 'Failed to load task',
        onError: (error) => {
          console.error('Task fetch failed:', error);
        }
      }
    );

    if (result) {
      setTask(result);
    }

    return result;
  }, [taskId]);

  const updateTask = useCallback(async (updates) => {
    if (!taskId) return null;

    const result = await api.execute(
      () => taskService.updateTask(taskId, updates),
      {
        successMessage: MESSAGES.SUCCESS_UPDATE,
        errorMessage: 'Failed to update task',
        onError: (error) => {
          console.error('Task update failed:', error);
        }
      }
    );

    if (result) {
      setTask(result);
    }

    return result;
  }, [taskId]);

  const deleteTask = useCallback(async () => {
    if (!taskId) return;

    await api.execute(
      () => taskService.deleteTask(taskId),
      {
        successMessage: MESSAGES.SUCCESS_DELETE,
        errorMessage: 'Failed to delete task',
        onError: (error) => {
          console.error('Task delete failed:', error);
        }
      }
    );

    setTask(null);
  }, [taskId]);

  // Load task on mount or when ID changes
  useEffect(() => {
    if (taskId) {
      fetchTask();
    }
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [taskId]);

  return {
    task,
    loading: api.loading,
    error: api.error,
    fetchTask,
    updateTask,
    deleteTask,
    clearError: useCallback(() => api.clearError(), [])
  };
};

export default useTasks;