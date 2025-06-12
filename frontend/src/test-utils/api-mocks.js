/**
 * API service mocks for testing
 */

import { mockTodos } from './test-utils';

/**
 * Mock API responses
 */
export const mockApiResponses = {
  getTodos: jest.fn(() => Promise.resolve([...mockTodos])),
  createTodo: jest.fn((text) =>
    Promise.resolve({
      id: '4',
      text,
      completed: false,
      created_at: new Date().toISOString(),
    })
  ),
  updateTodo: jest.fn((id, updates) => {
    const todo = mockTodos.find(t => t.id === id);
    return Promise.resolve({ ...todo, ...updates });
  }),
  deleteTodo: jest.fn(() => Promise.resolve()),
  toggleTodo: jest.fn((id, completed) => {
    const todo = mockTodos.find(t => t.id === id);
    return Promise.resolve({ ...todo, completed });
  }),
};

/**
 * Mock API service module
 */
export const mockApiService = {
  ...mockApiResponses,
};

/**
 * Reset all API mocks
 */
export function resetApiMocks() {
  Object.values(mockApiResponses).forEach(mock => {
    mock.mockReset();
    // Restore default implementations
    if (mock === mockApiResponses.getTodos) {
      mock.mockResolvedValue([...mockTodos]);
    } else if (mock === mockApiResponses.createTodo) {
      mock.mockImplementation((text) =>
        Promise.resolve({
          id: '4',
          text,
          completed: false,
          created_at: new Date().toISOString(),
        })
      );
    } else if (mock === mockApiResponses.updateTodo) {
      mock.mockImplementation((id, updates) => {
        const todo = mockTodos.find(t => t.id === id);
        return Promise.resolve({ ...todo, ...updates });
      });
    } else if (mock === mockApiResponses.deleteTodo) {
      mock.mockResolvedValue();
    } else if (mock === mockApiResponses.toggleTodo) {
      mock.mockImplementation((id, completed) => {
        const todo = mockTodos.find(t => t.id === id);
        return Promise.resolve({ ...todo, completed });
      });
    }
  });
}

/**
 * Mock API errors for testing error states
 */
export function mockApiError(method, error = new Error('API Error')) {
  mockApiResponses[method].mockRejectedValueOnce(error);
}

/**
 * Mock API loading delay for testing loading states
 */
export function mockApiDelay(method, delay = 100) {
  const originalImpl = mockApiResponses[method].getMockImplementation();
  mockApiResponses[method].mockImplementationOnce(
    (...args) => new Promise(resolve => 
      setTimeout(() => resolve(originalImpl(...args)), delay)
    )
  );
}