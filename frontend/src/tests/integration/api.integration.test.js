/**
 * Integration tests for API communication
 * 
 * These tests verify that the frontend can properly communicate with the backend API.
 * They require both frontend and backend servers to be running.
 */

import { apiClient, ApiError } from '../../services/api';

// Mock server URL for testing
const TEST_BASE_URL = 'http://localhost:5000/api';

describe('API Integration Tests', () => {
  let testTaskId = null;

  beforeAll(async () => {
    // Check if API is available
    try {
      const response = await fetch(`${TEST_BASE_URL}/health`);
      if (!response.ok) {
        throw new Error('API not available');
      }
    } catch (error) {
      console.warn('API server may not be running. These tests require the backend server to be running on port 5000.');
      // You might want to skip tests or use a different approach here
    }
  });

  afterEach(async () => {
    // Clean up test task if it was created
    if (testTaskId) {
      try {
        await apiClient.delete(`/tasks/${testTaskId}`);
      } catch (error) {
        // Ignore cleanup errors
      }
      testTaskId = null;
    }
  });

  describe('Health Check', () => {
    test('should successfully check API health', async () => {
      const response = await apiClient.get('/health');
      
      expect(response).toHaveProperty('status', 'healthy');
      expect(response).toHaveProperty('message');
      expect(response).toHaveProperty('timestamp');
    });
  });

  describe('Task CRUD Operations', () => {
    test('should create a new task', async () => {
      const taskData = {
        title: 'Integration Test Task',
        description: 'This task was created by an integration test',
        priority: 'Medium'
      };

      const response = await apiClient.post('/tasks', taskData);
      
      expect(response).toHaveProperty('task');
      expect(response.task).toHaveProperty('id');
      expect(response.task.title).toBe(taskData.title);
      expect(response.task.description).toBe(taskData.description);
      expect(response.task.priority).toBe(taskData.priority);
      expect(response.task.completed).toBe(false);
      
      // Store for cleanup
      testTaskId = response.task.id;
    });

    test('should get all tasks', async () => {
      // Create a test task first
      const taskData = {
        title: 'Test Task for Get All',
        priority: 'High'
      };
      
      const createResponse = await apiClient.post('/tasks', taskData);
      testTaskId = createResponse.task.id;

      const response = await apiClient.get('/tasks');
      
      expect(response).toHaveProperty('tasks');
      expect(response).toHaveProperty('pagination');
      expect(Array.isArray(response.tasks)).toBe(true);
      expect(response.pagination.total).toBeGreaterThan(0);
      
      // Find our test task
      const testTask = response.tasks.find(task => task.id === testTaskId);
      expect(testTask).toBeDefined();
      expect(testTask.title).toBe(taskData.title);
    });

    test('should get a specific task', async () => {
      // Create a test task first
      const taskData = {
        title: 'Test Task for Get Specific',
        description: 'Specific task test',
        priority: 'Low'
      };
      
      const createResponse = await apiClient.post('/tasks', taskData);
      testTaskId = createResponse.task.id;

      const response = await apiClient.get(`/tasks/${testTaskId}`);
      
      expect(response).toHaveProperty('task');
      expect(response.task.id).toBe(testTaskId);
      expect(response.task.title).toBe(taskData.title);
      expect(response.task.description).toBe(taskData.description);
    });

    test('should update a task', async () => {
      // Create a test task first
      const taskData = {
        title: 'Task to Update',
        priority: 'Medium',
        completed: false
      };
      
      const createResponse = await apiClient.post('/tasks', taskData);
      testTaskId = createResponse.task.id;

      // Update the task
      const updateData = {
        completed: true,
        priority: 'High',
        description: 'Updated description'
      };

      const response = await apiClient.put(`/tasks/${testTaskId}`, updateData);
      
      expect(response).toHaveProperty('task');
      expect(response.task.completed).toBe(true);
      expect(response.task.priority).toBe('High');
      expect(response.task.description).toBe('Updated description');
      expect(response.task.title).toBe(taskData.title); // Should remain unchanged
    });

    test('should delete a task', async () => {
      // Create a test task first
      const taskData = {
        title: 'Task to Delete',
        priority: 'Low'
      };
      
      const createResponse = await apiClient.post('/tasks', taskData);
      const taskToDeleteId = createResponse.task.id;

      // Delete the task
      const deleteResponse = await apiClient.delete(`/tasks/${taskToDeleteId}`);
      expect(deleteResponse).toBeNull(); // DELETE returns null for 204 responses

      // Verify task is deleted by trying to get it
      await expect(apiClient.get(`/tasks/${taskToDeleteId}`))
        .rejects.toThrow(ApiError);
      
      // Don't set testTaskId since we already deleted it
    });
  });

  describe('Task Filtering and Pagination', () => {
    const testTasks = [];

    beforeAll(async () => {
      // Create multiple test tasks for filtering
      const tasksToCreate = [
        { title: 'Completed High Priority', completed: true, priority: 'High' },
        { title: 'Pending Medium Priority', completed: false, priority: 'Medium' },
        { title: 'Pending Low Priority', completed: false, priority: 'Low' },
        { title: 'Completed Low Priority', completed: true, priority: 'Low' }
      ];

      for (const taskData of tasksToCreate) {
        const response = await apiClient.post('/tasks', taskData);
        testTasks.push(response.task.id);
      }
    });

    afterAll(async () => {
      // Clean up test tasks
      for (const taskId of testTasks) {
        try {
          await apiClient.delete(`/tasks/${taskId}`);
        } catch (error) {
          // Ignore cleanup errors
        }
      }
    });

    test('should filter tasks by completion status', async () => {
      const completedResponse = await apiClient.get('/tasks', { completed: true });
      
      expect(completedResponse.tasks.length).toBeGreaterThan(0);
      completedResponse.tasks.forEach(task => {
        expect(task.completed).toBe(true);
      });

      const pendingResponse = await apiClient.get('/tasks', { completed: false });
      
      expect(pendingResponse.tasks.length).toBeGreaterThan(0);
      pendingResponse.tasks.forEach(task => {
        expect(task.completed).toBe(false);
      });
    });

    test('should filter tasks by priority', async () => {
      const highPriorityResponse = await apiClient.get('/tasks', { priority: 'High' });
      
      expect(highPriorityResponse.tasks.length).toBeGreaterThan(0);
      highPriorityResponse.tasks.forEach(task => {
        expect(task.priority).toBe('High');
      });
    });

    test('should handle pagination', async () => {
      const firstPageResponse = await apiClient.get('/tasks', { 
        page: 1, 
        per_page: 2 
      });
      
      expect(firstPageResponse.pagination.page).toBe(1);
      expect(firstPageResponse.pagination.per_page).toBe(2);
      expect(firstPageResponse.tasks.length).toBeLessThanOrEqual(2);
      
      if (firstPageResponse.pagination.has_next) {
        const secondPageResponse = await apiClient.get('/tasks', { 
          page: 2, 
          per_page: 2 
        });
        
        expect(secondPageResponse.pagination.page).toBe(2);
        expect(secondPageResponse.tasks.length).toBeLessThanOrEqual(2);
      }
    });
  });

  describe('Advanced Operations', () => {
    test('should get task statistics', async () => {
      const response = await apiClient.get('/tasks/stats');
      
      expect(response).toHaveProperty('stats');
      expect(response.stats).toHaveProperty('total_tasks');
      expect(response.stats).toHaveProperty('completed_tasks');
      expect(response.stats).toHaveProperty('pending_tasks');
      expect(response.stats).toHaveProperty('completion_rate');
      expect(response.stats).toHaveProperty('priority_breakdown');
      
      expect(typeof response.stats.total_tasks).toBe('number');
      expect(typeof response.stats.completion_rate).toBe('number');
    });

    test('should perform bulk updates', async () => {
      // Create multiple test tasks
      const taskIds = [];
      for (let i = 0; i < 3; i++) {
        const response = await apiClient.post('/tasks', {
          title: `Bulk Test Task ${i}`,
          priority: 'Medium',
          completed: false
        });
        taskIds.push(response.task.id);
      }

      // Perform bulk update
      const bulkResponse = await apiClient.put('/tasks/bulk', {
        task_ids: taskIds,
        updates: { completed: true, priority: 'High' }
      });

      expect(bulkResponse.tasks).toHaveLength(3);
      bulkResponse.tasks.forEach(task => {
        expect(task.completed).toBe(true);
        expect(task.priority).toBe('High');
      });

      // Clean up
      for (const taskId of taskIds) {
        await apiClient.delete(`/tasks/${taskId}`);
      }
    });
  });

  describe('Error Handling', () => {
    test('should handle validation errors', async () => {
      // Try to create task without title
      await expect(apiClient.post('/tasks', { description: 'No title' }))
        .rejects.toThrow(ApiError);
      
      try {
        await apiClient.post('/tasks', { description: 'No title' });
      } catch (error) {
        expect(error).toBeInstanceOf(ApiError);
        expect(error.status).toBe(400);
        expect(error.code).toBe('MISSING_TITLE');
      }
    });

    test('should handle not found errors', async () => {
      await expect(apiClient.get('/tasks/99999'))
        .rejects.toThrow(ApiError);
      
      try {
        await apiClient.get('/tasks/99999');
      } catch (error) {
        expect(error).toBeInstanceOf(ApiError);
        expect(error.status).toBe(404);
        expect(error.isNotFoundError()).toBe(true);
      }
    });

    test('should handle invalid priority', async () => {
      await expect(apiClient.post('/tasks', {
        title: 'Test Task',
        priority: 'Invalid'
      })).rejects.toThrow(ApiError);
      
      try {
        await apiClient.post('/tasks', {
          title: 'Test Task',
          priority: 'Invalid'
        });
      } catch (error) {
        expect(error).toBeInstanceOf(ApiError);
        expect(error.status).toBe(400);
        expect(error.code).toBe('INVALID_PRIORITY');
        expect(error.isValidationError()).toBe(true);
      }
    });
  });

  describe('Network Error Handling', () => {
    test('should handle network errors gracefully', async () => {
      // Create a client with invalid URL to simulate network error
      const badClient = new (apiClient.constructor)('http://localhost:9999/api');
      
      await expect(badClient.get('/health'))
        .rejects.toThrow(ApiError);
      
      try {
        await badClient.get('/health');
      } catch (error) {
        expect(error).toBeInstanceOf(ApiError);
        expect(error.isNetworkError()).toBe(true);
        expect(error.code).toBe('NETWORK_ERROR');
      }
    });
  });
});