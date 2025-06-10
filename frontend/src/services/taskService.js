// Task-specific API service for Todo List Application
// Implements all CRUD operations according to API contract

import apiClient, { ApiError } from './api.js';
import { API_ENDPOINTS, DEFAULT_QUERY_PARAMS } from '../utils/constants.js';
import { sanitizeTaskData } from '../utils/formatters.js';

class TaskService {
  /**
   * Get all tasks with optional filtering and sorting
   * @param {object} params - Query parameters for filtering and sorting
   * @returns {Promise<object>} API response with tasks data
   */
  async getTasks(params = {}) {
    try {
      // Merge with default query parameters
      const queryParams = { ...DEFAULT_QUERY_PARAMS, ...params };
      
      // Remove undefined/null values
      const cleanParams = Object.keys(queryParams).reduce((acc, key) => {
        if (queryParams[key] !== undefined && queryParams[key] !== null && queryParams[key] !== '') {
          acc[key] = queryParams[key];
        }
        return acc;
      }, {});
      
      const response = await apiClient.get(API_ENDPOINTS.TASKS, cleanParams);
      
      // Handle the response wrapper format
      return {
        tasks: response.data?.tasks || [],
        total: response.data?.total || 0,
        filtered: response.data?.filtered || 0
      };
    } catch (error) {
      console.error('Error fetching tasks:', error);
      throw error;
    }
  }

  /**
   * Get a single task by ID
   * @param {number} taskId - Task ID
   * @returns {Promise<object>} Task data
   */
  async getTask(taskId) {
    try {
      const response = await apiClient.get(API_ENDPOINTS.TASK_BY_ID(taskId));
      return response.data;
    } catch (error) {
      console.error(`Error fetching task ${taskId}:`, error);
      throw error;
    }
  }

  /**
   * Create a new task
   * @param {object} taskData - Task data (title, description, priority)
   * @returns {Promise<object>} Created task data
   */
  async createTask(taskData) {
    try {
      // Sanitize and validate input data
      const sanitizedData = sanitizeTaskData(taskData);
      
      // Validate required fields
      if (!sanitizedData.title || sanitizedData.title.trim().length === 0) {
        throw new ApiError('Title is required', 400, 'VALIDATION_ERROR', {
          title: 'Title cannot be empty'
        });
      }
      
      if (sanitizedData.title.length > 200) {
        throw new ApiError('Title too long', 400, 'VALIDATION_ERROR', {
          title: 'Title must be 200 characters or less'
        });
      }
      
      if (sanitizedData.description && sanitizedData.description.length > 1000) {
        throw new ApiError('Description too long', 400, 'VALIDATION_ERROR', {
          description: 'Description must be 1000 characters or less'
        });
      }
      
      // Prepare request payload
      const payload = {
        title: sanitizedData.title,
        priority: sanitizedData.priority || 'Medium'
      };
      
      // Only include description if it's not empty
      if (sanitizedData.description) {
        payload.description = sanitizedData.description;
      }
      
      const response = await apiClient.post(API_ENDPOINTS.TASKS, payload);
      return response.data;
    } catch (error) {
      console.error('Error creating task:', error);
      throw error;
    }
  }

  /**
   * Update an existing task
   * @param {number} taskId - Task ID
   * @param {object} updates - Fields to update
   * @returns {Promise<object>} Updated task data
   */
  async updateTask(taskId, updates) {
    try {
      // Sanitize update data
      const sanitizedUpdates = {};
      
      // Only include fields that are being updated
      if (updates.title !== undefined) {
        sanitizedUpdates.title = updates.title.trim();
        
        if (sanitizedUpdates.title.length === 0) {
          throw new ApiError('Title is required', 400, 'VALIDATION_ERROR', {
            title: 'Title cannot be empty'
          });
        }
        
        if (sanitizedUpdates.title.length > 200) {
          throw new ApiError('Title too long', 400, 'VALIDATION_ERROR', {
            title: 'Title must be 200 characters or less'
          });
        }
      }
      
      if (updates.description !== undefined) {
        sanitizedUpdates.description = updates.description ? updates.description.trim() : null;
        
        if (sanitizedUpdates.description && sanitizedUpdates.description.length > 1000) {
          throw new ApiError('Description too long', 400, 'VALIDATION_ERROR', {
            description: 'Description must be 1000 characters or less'
          });
        }
      }
      
      if (updates.priority !== undefined) {
        const validPriorities = ['High', 'Medium', 'Low'];
        if (!validPriorities.includes(updates.priority)) {
          throw new ApiError('Invalid priority', 400, 'VALIDATION_ERROR', {
            priority: 'Priority must be High, Medium, or Low'
          });
        }
        sanitizedUpdates.priority = updates.priority;
      }
      
      if (updates.completed !== undefined) {
        sanitizedUpdates.completed = Boolean(updates.completed);
      }
      
      const response = await apiClient.put(API_ENDPOINTS.TASK_BY_ID(taskId), sanitizedUpdates);
      return response.data;
    } catch (error) {
      console.error(`Error updating task ${taskId}:`, error);
      throw error;
    }
  }

  /**
   * Delete a task
   * @param {number} taskId - Task ID
   * @returns {Promise<void>}
   */
  async deleteTask(taskId) {
    try {
      await apiClient.delete(API_ENDPOINTS.TASK_BY_ID(taskId));
    } catch (error) {
      console.error(`Error deleting task ${taskId}:`, error);
      throw error;
    }
  }

  /**
   * Toggle task completion status
   * @param {number} taskId - Task ID
   * @param {boolean} completed - New completion status
   * @returns {Promise<object>} Updated task data
   */
  async toggleTaskCompletion(taskId, completed) {
    return this.updateTask(taskId, { completed });
  }

  /**
   * Get task statistics
   * @returns {Promise<object>} Task statistics data
   */
  async getTaskStats() {
    try {
      const response = await apiClient.get(API_ENDPOINTS.TASK_STATS);
      return response.data;
    } catch (error) {
      console.error('Error fetching task stats:', error);
      throw error;
    }
  }

  /**
   * Search tasks by title and description
   * @param {string} searchTerm - Search term
   * @param {object} additionalParams - Additional query parameters
   * @returns {Promise<object>} Search results
   */
  async searchTasks(searchTerm, additionalParams = {}) {
    return this.getTasks({
      search: searchTerm,
      ...additionalParams
    });
  }

  /**
   * Get tasks filtered by completion status
   * @param {boolean} completed - Completion status filter
   * @param {object} additionalParams - Additional query parameters
   * @returns {Promise<object>} Filtered tasks
   */
  async getTasksByStatus(completed, additionalParams = {}) {
    return this.getTasks({
      completed: completed ? 'true' : 'false',
      ...additionalParams
    });
  }

  /**
   * Get tasks filtered by priority
   * @param {string} priority - Priority level (High, Medium, Low)
   * @param {object} additionalParams - Additional query parameters
   * @returns {Promise<object>} Filtered tasks
   */
  async getTasksByPriority(priority, additionalParams = {}) {
    return this.getTasks({
      priority,
      ...additionalParams
    });
  }

  /**
   * Bulk update multiple tasks
   * @param {array} taskUpdates - Array of {id, updates} objects
   * @returns {Promise<array>} Array of updated tasks
   */
  async bulkUpdateTasks(taskUpdates) {
    try {
      const updatePromises = taskUpdates.map(({ id, updates }) => 
        this.updateTask(id, updates)
      );
      
      const results = await Promise.allSettled(updatePromises);
      
      // Return successful updates and collect errors
      const successfulUpdates = [];
      const errors = [];
      
      results.forEach((result, index) => {
        if (result.status === 'fulfilled') {
          successfulUpdates.push(result.value);
        } else {
          errors.push({
            taskId: taskUpdates[index].id,
            error: result.reason
          });
        }
      });
      
      if (errors.length > 0) {
        console.warn('Some bulk updates failed:', errors);
      }
      
      return {
        successful: successfulUpdates,
        errors: errors
      };
    } catch (error) {
      console.error('Error in bulk update:', error);
      throw error;
    }
  }
}

// Create and export singleton instance
const taskService = new TaskService();

export default taskService;