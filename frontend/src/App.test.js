import React from 'react';
import { screen, waitFor } from '@testing-library/react';
import userEvent from '@testing-library/user-event';
import App from './App';
import { renderWithProviders } from './test-utils/test-utils';
import { mockApiService, resetApiMocks, mockApiError, mockApiDelay } from './test-utils/api-mocks';

// Mock the API service
jest.mock('./services/api', () => ({
  getTodos: jest.fn(),
  createTodo: jest.fn(),
  updateTodo: jest.fn(),
  deleteTodo: jest.fn(),
}));

// Get the mocked functions
const api = require('./services/api');

beforeEach(() => {
  resetApiMocks();
  // Set up default mock implementations
  api.getTodos.mockImplementation(mockApiService.getTodos);
  api.createTodo.mockImplementation(mockApiService.createTodo);
  api.updateTodo.mockImplementation(mockApiService.updateTodo);
  api.deleteTodo.mockImplementation(mockApiService.deleteTodo);
});

describe('App', () => {
  test('renders app header and main sections', async () => {
    renderWithProviders(<App />);
    
    expect(screen.getByText('Todo Application')).toBeInTheDocument();
    expect(screen.getByText('Manage your tasks efficiently')).toBeInTheDocument();
    expect(screen.getByText('Built with React and Flask')).toBeInTheDocument();
  });

  test('shows loading state initially', () => {
    // Mock API delay
    api.getTodos.mockImplementationOnce(
      () => new Promise(resolve => setTimeout(() => resolve([]), 100))
    );
    
    renderWithProviders(<App />);
    
    expect(screen.getByText('Loading todos...')).toBeInTheDocument();
  });

  test('loads and displays todos on mount', async () => {
    renderWithProviders(<App />);
    
    await waitFor(() => {
      expect(screen.getByText('Test todo 1')).toBeInTheDocument();
      expect(screen.getByText('Test todo 2')).toBeInTheDocument();
      expect(screen.getByText('Test todo 3')).toBeInTheDocument();
    });
    
    expect(api.getTodos).toHaveBeenCalledTimes(1);
  });

  test('shows error state when loading todos fails', async () => {
    api.getTodos.mockRejectedValueOnce(new Error('API Error'));
    
    renderWithProviders(<App />);
    
    await waitFor(() => {
      expect(screen.getByText(/Failed to load todos/)).toBeInTheDocument();
      expect(screen.getByRole('button', { name: 'Retry' })).toBeInTheDocument();
    });
  });

  test('can retry loading todos after error', async () => {
    const user = userEvent.setup();
    api.getTodos.mockRejectedValueOnce(new Error('API Error'));
    
    renderWithProviders(<App />);
    
    await waitFor(() => {
      expect(screen.getByText(/Failed to load todos/)).toBeInTheDocument();
    });
    
    // Reset mock to succeed on retry
    api.getTodos.mockResolvedValueOnce([]);
    
    const retryButton = screen.getByRole('button', { name: 'Retry' });
    await user.click(retryButton);
    
    expect(api.getTodos).toHaveBeenCalledTimes(2);
  });

  test('shows empty state when no todos', async () => {
    api.getTodos.mockResolvedValueOnce([]);
    
    renderWithProviders(<App />);
    
    await waitFor(() => {
      expect(screen.getByText('No todos yet. Add your first todo!')).toBeInTheDocument();
    });
  });

  test('renders TodoForm component', async () => {
    renderWithProviders(<App />);
    
    await waitFor(() => {
      expect(screen.getByPlaceholderText('What needs to be done?')).toBeInTheDocument();
    });
  });

  test('can add new todo', async () => {
    const user = userEvent.setup();
    const newTodo = { id: '4', text: 'New todo', completed: false };
    api.createTodo.mockResolvedValueOnce(newTodo);
    
    renderWithProviders(<App />);
    
    // Wait for initial load
    await waitFor(() => {
      expect(screen.getByText('Test todo 1')).toBeInTheDocument();
    });
    
    const input = screen.getByPlaceholderText('What needs to be done?');
    await user.type(input, 'New todo');
    await user.click(screen.getByRole('button', { name: /add|submit/i }));
    
    await waitFor(() => {
      expect(screen.getByText('New todo')).toBeInTheDocument();
    });
    
    expect(api.createTodo).toHaveBeenCalledWith('New todo');
  });

  test('can toggle todo completion', async () => {
    const user = userEvent.setup();
    const updatedTodo = { id: '1', text: 'Test todo 1', completed: true };
    api.updateTodo.mockResolvedValueOnce(updatedTodo);
    
    renderWithProviders(<App />);
    
    // Wait for initial load
    await waitFor(() => {
      expect(screen.getByText('Test todo 1')).toBeInTheDocument();
    });
    
    const toggleButtons = screen.getAllByRole('button', { name: /mark as/i });
    await user.click(toggleButtons[0]);
    
    expect(api.updateTodo).toHaveBeenCalledWith('1', { completed: true });
  });

  test('can delete todo', async () => {
    const user = userEvent.setup();
    window.confirm = jest.fn(() => true);
    
    renderWithProviders(<App />);
    
    // Wait for initial load
    await waitFor(() => {
      expect(screen.getByText('Test todo 1')).toBeInTheDocument();
    });
    
    const deleteButtons = screen.getAllByRole('button', { name: /delete/i });
    await user.click(deleteButtons[0]);
    
    expect(api.deleteTodo).toHaveBeenCalledWith('1');
    
    await waitFor(() => {
      expect(screen.queryByText('Test todo 1')).not.toBeInTheDocument();
    });
  });

  test('displays todo count', async () => {
    renderWithProviders(<App />);
    
    await waitFor(() => {
      expect(screen.getByText('Todo List (3)')).toBeInTheDocument();
    });
  });

  test('handles API errors gracefully', async () => {
    const user = userEvent.setup();
    api.createTodo.mockRejectedValueOnce(new Error('Failed to create todo'));
    
    renderWithProviders(<App />);
    
    // Wait for initial load
    await waitFor(() => {
      expect(screen.getByText('Test todo 1')).toBeInTheDocument();
    });
    
    const input = screen.getByPlaceholderText('What needs to be done?');
    await user.type(input, 'New todo');
    await user.click(screen.getByRole('button', { name: /add|submit/i }));
    
    await waitFor(() => {
      expect(screen.getByText('Failed to create todo')).toBeInTheDocument();
    });
  });

  test('integrates all components correctly', async () => {
    renderWithProviders(<App />);
    
    // Wait for components to load
    await waitFor(() => {
      // TodoForm should be present
      expect(screen.getByPlaceholderText('What needs to be done?')).toBeInTheDocument();
      
      // TodoList should be present
      expect(screen.getByText('Todo List (3)')).toBeInTheDocument();
      
      // TodoItems should be present
      expect(screen.getByText('Test todo 1')).toBeInTheDocument();
      expect(screen.getByText('Test todo 2')).toBeInTheDocument();
      expect(screen.getByText('Test todo 3')).toBeInTheDocument();
    });
    
    // Should have toggle and delete buttons for each todo
    expect(screen.getAllByRole('button', { name: /mark as/i })).toHaveLength(3);
    expect(screen.getAllByRole('button', { name: /delete/i })).toHaveLength(3);
  });
});
