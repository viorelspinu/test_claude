import React from 'react';
import { render } from '@testing-library/react';

/**
 * Test utilities for todo application
 */

/**
 * Custom render function for components with common providers
 * Can be extended with context providers if needed
 */
export function renderWithProviders(ui, options = {}) {
  const { ...renderOptions } = options;

  function Wrapper({ children }) {
    // Add providers here if needed (e.g., Context, Router)
    return children;
  }

  return render(ui, { wrapper: Wrapper, ...renderOptions });
}

/**
 * Sample todo data for testing
 */
export const mockTodos = [
  {
    id: '1',
    text: 'Test todo 1',
    completed: false,
    created_at: new Date().toISOString(),
  },
  {
    id: '2',
    text: 'Test todo 2',
    completed: true,
    created_at: new Date().toISOString(),
  },
  {
    id: '3',
    text: 'Test todo 3',
    completed: false,
    created_at: new Date().toISOString(),
  },
];

/**
 * Mock functions for testing
 */
export const mockCallbacks = {
  onAddTodo: jest.fn(),
  onToggle: jest.fn(),
  onDelete: jest.fn(),
};

/**
 * Reset all mock functions
 */
export function resetMocks() {
  Object.values(mockCallbacks).forEach(mock => mock.mockReset());
}

/**
 * Wait for async operations to complete
 */
export const waitForAsync = () => new Promise(resolve => setTimeout(resolve, 0));

// Re-export everything from @testing-library/react
export * from '@testing-library/react';
export { default as userEvent } from '@testing-library/user-event';