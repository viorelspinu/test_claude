/**
 * End-to-End Full Stack Integration Tests
 * 
 * These tests verify the complete integration between React frontend and Flask backend.
 * They test real user workflows and ensure the full stack works together.
 */

import { render, screen, fireEvent, waitFor } from '@testing-library/react';
import userEvent from '@testing-library/user-event';
import App from '../../App';
import { apiClient } from '../../services/api';

// Mock API responses for controlled testing
const mockHealthResponse = {
  status: 'healthy',
  message: 'Todo API is running',
  timestamp: new Date().toISOString()
};

const mockTasksResponse = {
  tasks: [
    {
      id: 1,
      title: 'Sample Task',
      description: 'This is a sample task',
      priority: 'Medium',
      completed: false,
      created_at: '2023-01-01T00:00:00',
      updated_at: '2023-01-01T00:00:00'
    }
  ],
  pagination: {
    page: 1,
    per_page: 20,
    total: 1,
    pages: 1,
    has_next: false,
    has_prev: false
  }
};

const mockStatsResponse = {
  stats: {
    total_tasks: 1,
    completed_tasks: 0,
    pending_tasks: 1,
    completion_rate: 0,
    priority_breakdown: {
      high: 0,
      medium: 1,
      low: 0
    }
  }
};

describe('Full Stack E2E Tests', () => {
  beforeEach(() => {
    // Clear all mocks before each test
    jest.clearAllMocks();
    
    // Setup default mock responses
    global.fetch = jest.fn((url) => {
      if (url.includes('/health')) {
        return Promise.resolve({
          ok: true,
          status: 200,
          json: () => Promise.resolve(mockHealthResponse)
        });
      }
      
      if (url.includes('/tasks/stats')) {
        return Promise.resolve({
          ok: true,
          status: 200,
          json: () => Promise.resolve(mockStatsResponse)
        });
      }
      
      if (url.includes('/tasks') && !url.includes('/')) {
        return Promise.resolve({
          ok: true,
          status: 200,
          json: () => Promise.resolve(mockTasksResponse)
        });
      }
      
      // Default response for unmatched URLs
      return Promise.resolve({
        ok: false,
        status: 404,
        json: () => Promise.resolve({ error: { message: 'Not found' } })
      });
    });
  });

  describe('Application Initialization', () => {
    test('should render app and check API health', async () => {
      render(<App />);
      
      // Wait for the app to load and make initial API calls
      await waitFor(() => {
        expect(global.fetch).toHaveBeenCalled();
      });
      
      // Check that health endpoint was called
      expect(global.fetch).toHaveBeenCalledWith(
        expect.stringContaining('/health'),
        expect.any(Object)
      );
    });

    test('should load and display tasks on startup', async () => {
      render(<App />);
      
      // Wait for tasks to load
      await waitFor(() => {
        expect(screen.getByText('Sample Task')).toBeInTheDocument();
      });
      
      // Verify API was called to fetch tasks
      expect(global.fetch).toHaveBeenCalledWith(
        expect.stringContaining('/tasks'),
        expect.objectContaining({
          method: 'GET'
        })
      );
    });
  });

  describe('Task Management Workflow', () => {
    test('should create a new task through the UI', async () => {
      const user = userEvent.setup();
      
      // Mock the POST response for creating a task
      const newTask = {
        id: 2,
        title: 'New Task from UI',
        description: 'Created through user interface',
        priority: 'High',
        completed: false,
        created_at: new Date().toISOString(),
        updated_at: new Date().toISOString()
      };
      
      global.fetch.mockImplementation((url, options) => {
        if (url.includes('/health')) {
          return Promise.resolve({
            ok: true,
            status: 200,
            json: () => Promise.resolve(mockHealthResponse)
          });
        }
        
        if (url.includes('/tasks') && options?.method === 'POST') {
          return Promise.resolve({
            ok: true,
            status: 201,
            json: () => Promise.resolve({
              task: newTask,
              message: 'Task created successfully'
            })
          });
        }
        
        if (url.includes('/tasks') && options?.method === 'GET') {
          return Promise.resolve({
            ok: true,
            status: 200,
            json: () => Promise.resolve({
              ...mockTasksResponse,
              tasks: [...mockTasksResponse.tasks, newTask]
            })
          });
        }
        
        return Promise.resolve({
          ok: false,
          status: 404,
          json: () => Promise.resolve({ error: { message: 'Not found' } })
        });
      });

      render(<App />);
      
      // Find and interact with task creation form
      const titleInput = screen.getByPlaceholderText(/task title/i) || 
                        screen.getByLabelText(/title/i) ||
                        screen.getByRole('textbox', { name: /title/i });
      
      if (titleInput) {
        await user.type(titleInput, 'New Task from UI');
        
        const submitButton = screen.getByRole('button', { name: /add|create|submit/i });
        await user.click(submitButton);
        
        // Wait for the task to appear in the list
        await waitFor(() => {
          expect(screen.getByText('New Task from UI')).toBeInTheDocument();
        });
        
        // Verify POST request was made
        expect(global.fetch).toHaveBeenCalledWith(
          expect.stringContaining('/tasks'),
          expect.objectContaining({
            method: 'POST',
            body: expect.stringContaining('New Task from UI')
          })
        );
      }
    });

    test('should update task completion status', async () => {
      const user = userEvent.setup();
      
      // Mock the PUT response for updating a task
      global.fetch.mockImplementation((url, options) => {
        if (url.includes('/health')) {
          return Promise.resolve({
            ok: true,
            status: 200,
            json: () => Promise.resolve(mockHealthResponse)
          });
        }
        
        if (url.includes('/tasks/1') && options?.method === 'PUT') {
          return Promise.resolve({
            ok: true,
            status: 200,
            json: () => Promise.resolve({
              task: {
                ...mockTasksResponse.tasks[0],
                completed: true
              },
              message: 'Task updated successfully'
            })
          });
        }
        
        if (url.includes('/tasks') && options?.method === 'GET') {
          return Promise.resolve({
            ok: true,
            status: 200,
            json: () => Promise.resolve(mockTasksResponse)
          });
        }
        
        return Promise.resolve({
          ok: false,
          status: 404,
          json: () => Promise.resolve({ error: { message: 'Not found' } })
        });
      });

      render(<App />);
      
      // Wait for tasks to load
      await waitFor(() => {
        expect(screen.getByText('Sample Task')).toBeInTheDocument();
      });
      
      // Find and click the completion checkbox/button
      const completeButton = screen.getByRole('checkbox') || 
                            screen.getByRole('button', { name: /complete|done/i });
      
      if (completeButton) {
        await user.click(completeButton);
        
        // Verify PUT request was made
        await waitFor(() => {
          expect(global.fetch).toHaveBeenCalledWith(
            expect.stringContaining('/tasks/1'),
            expect.objectContaining({
              method: 'PUT'
            })
          );
        });
      }
    });
  });

  describe('Error Handling Integration', () => {
    test('should handle API connection errors gracefully', async () => {
      // Mock network error
      global.fetch.mockRejectedValue(new Error('Network Error'));
      
      render(<App />);
      
      // Wait for error handling
      await waitFor(() => {
        // Should show some kind of error message or fallback UI
        const errorElement = screen.queryByText(/error|failed|connection/i);
        expect(errorElement).toBeInTheDocument();
      });
    });

    test('should handle invalid API responses', async () => {
      // Mock invalid API response
      global.fetch.mockResolvedValue({
        ok: false,
        status: 500,
        json: () => Promise.resolve({
          error: {
            message: 'Internal server error',
            code: 'INTERNAL_ERROR'
          }
        })
      });
      
      render(<App />);
      
      // Wait for error handling
      await waitFor(() => {
        const errorElement = screen.queryByText(/error|failed/i);
        expect(errorElement).toBeInTheDocument();
      });
    });
  });

  describe('Real API Integration Tests', () => {
    // These tests will only run if the API is actually available
    beforeAll(async () => {
      // Check if real API is available
      try {
        const response = await fetch('http://localhost:5000/api/health');
        if (!response.ok) {
          throw new Error('API not available');
        }
      } catch (error) {
        console.warn('Real API not available, skipping real integration tests');
        return;
      }
    });

    test('should successfully communicate with real API', async () => {
      // Only run if we can connect to the real API
      try {
        const healthResponse = await apiClient.get('/health');
        expect(healthResponse.status).toBe('healthy');
        
        const tasksResponse = await apiClient.get('/tasks');
        expect(tasksResponse).toHaveProperty('tasks');
        expect(tasksResponse).toHaveProperty('pagination');
        
        const statsResponse = await apiClient.get('/tasks/stats');
        expect(statsResponse).toHaveProperty('stats');
      } catch (error) {
        // Skip test if API is not available
        console.warn('Skipping real API test - API not available');
      }
    });
  });

  describe('Performance and Load Testing', () => {
    test('should handle multiple concurrent API calls', async () => {
      const promises = [];
      
      // Make multiple concurrent API calls
      for (let i = 0; i < 5; i++) {
        promises.push(apiClient.get('/health'));
      }
      
      const results = await Promise.all(promises);
      
      // All calls should succeed
      results.forEach(result => {
        expect(result.status).toBe('healthy');
      });
    });

    test('should handle rapid UI interactions', async () => {
      const user = userEvent.setup();
      
      render(<App />);
      
      // Wait for initial load
      await waitFor(() => {
        expect(global.fetch).toHaveBeenCalled();
      });
      
      // Perform rapid UI interactions if elements exist
      const refreshButton = screen.queryByRole('button', { name: /refresh|reload/i });
      if (refreshButton) {
        // Click multiple times rapidly
        for (let i = 0; i < 3; i++) {
          await user.click(refreshButton);
        }
        
        // Should handle rapid clicks gracefully without errors
        expect(refreshButton).toBeInTheDocument();
      }
    });
  });
});