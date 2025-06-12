import React from 'react';
import { screen, waitFor } from '@testing-library/react';
import userEvent from '@testing-library/user-event';
import TodoItem from './TodoItem';
import { renderWithProviders, mockCallbacks, resetMocks } from '../test-utils/test-utils';

// Reset mocks before each test
beforeEach(() => {
  resetMocks();
});

describe('TodoItem', () => {
  const mockTodo = {
    id: '1',
    text: 'Test todo',
    completed: false,
    created_at: '2025-01-23T10:00:00Z'
  };

  const completedTodo = {
    id: '2',
    text: 'Completed todo',
    completed: true,
    created_at: '2025-01-23T09:00:00Z'
  };

  test('renders todo text and status', () => {
    renderWithProviders(
      <TodoItem 
        todo={mockTodo} 
        onToggle={mockCallbacks.onToggle} 
        onDelete={mockCallbacks.onDelete} 
      />
    );
    
    expect(screen.getByText('Test todo')).toBeInTheDocument();
    expect(screen.getByText('⭕')).toBeInTheDocument(); // pending status
  });

  test('renders completed todo with different styling', () => {
    renderWithProviders(
      <TodoItem 
        todo={completedTodo} 
        onToggle={mockCallbacks.onToggle} 
        onDelete={mockCallbacks.onDelete} 
      />
    );
    
    expect(screen.getByText('Completed todo')).toBeInTheDocument();
    expect(screen.getByText('✅')).toBeInTheDocument(); // completed status
  });

  test('displays formatted creation date', () => {
    renderWithProviders(
      <TodoItem 
        todo={mockTodo} 
        onToggle={mockCallbacks.onToggle} 
        onDelete={mockCallbacks.onDelete} 
      />
    );
    
    // Should display some formatted date
    expect(screen.getByText(/1\/23\/2025|23\/1\/2025/)).toBeInTheDocument();
  });

  test('calls onToggle when toggle button clicked', async () => {
    const user = userEvent.setup();
    renderWithProviders(
      <TodoItem 
        todo={mockTodo} 
        onToggle={mockCallbacks.onToggle} 
        onDelete={mockCallbacks.onDelete} 
      />
    );
    
    const toggleButton = screen.getByRole('button', { name: /mark as/i });
    await user.click(toggleButton);
    
    expect(mockCallbacks.onToggle).toHaveBeenCalledWith('1');
  });

  test('calls onDelete when delete button clicked after confirmation', async () => {
    const user = userEvent.setup();
    // Mock window.confirm to return true
    window.confirm = jest.fn(() => true);
    
    renderWithProviders(
      <TodoItem 
        todo={mockTodo} 
        onToggle={mockCallbacks.onToggle} 
        onDelete={mockCallbacks.onDelete} 
      />
    );
    
    const deleteButton = screen.getByRole('button', { name: /delete/i });
    await user.click(deleteButton);
    
    expect(window.confirm).toHaveBeenCalledWith('Are you sure you want to delete this todo?');
    expect(mockCallbacks.onDelete).toHaveBeenCalledWith('1');
  });

  test('does not call onDelete when confirmation canceled', async () => {
    const user = userEvent.setup();
    // Mock window.confirm to return false
    window.confirm = jest.fn(() => false);
    
    renderWithProviders(
      <TodoItem 
        todo={mockTodo} 
        onToggle={mockCallbacks.onToggle} 
        onDelete={mockCallbacks.onDelete} 
      />
    );
    
    const deleteButton = screen.getByRole('button', { name: /delete/i });
    await user.click(deleteButton);
    
    expect(window.confirm).toHaveBeenCalled();
    expect(mockCallbacks.onDelete).not.toHaveBeenCalled();
  });

  test('shows loading state during toggle operation', async () => {
    const user = userEvent.setup();
    mockCallbacks.onToggle.mockImplementationOnce(
      () => new Promise(resolve => setTimeout(resolve, 100))
    );
    
    renderWithProviders(
      <TodoItem 
        todo={mockTodo} 
        onToggle={mockCallbacks.onToggle} 
        onDelete={mockCallbacks.onDelete} 
      />
    );
    
    const toggleButton = screen.getByRole('button', { name: /mark as/i });
    await user.click(toggleButton);
    
    expect(screen.getByText('⏳')).toBeInTheDocument();
    expect(toggleButton).toBeDisabled();
  });

  test('shows loading state during delete operation', async () => {
    const user = userEvent.setup();
    window.confirm = jest.fn(() => true);
    mockCallbacks.onDelete.mockImplementationOnce(
      () => new Promise(resolve => setTimeout(resolve, 100))
    );
    
    renderWithProviders(
      <TodoItem 
        todo={mockTodo} 
        onToggle={mockCallbacks.onToggle} 
        onDelete={mockCallbacks.onDelete} 
      />
    );
    
    const deleteButton = screen.getByRole('button', { name: /delete/i });
    await user.click(deleteButton);
    
    expect(screen.getAllByText('⏳')).toHaveLength(1);
    expect(deleteButton).toBeDisabled();
  });

  test('shows error message on toggle failure', async () => {
    const user = userEvent.setup();
    mockCallbacks.onToggle.mockRejectedValueOnce(new Error('Toggle failed'));
    
    renderWithProviders(
      <TodoItem 
        todo={mockTodo} 
        onToggle={mockCallbacks.onToggle} 
        onDelete={mockCallbacks.onDelete} 
      />
    );
    
    const toggleButton = screen.getByRole('button', { name: /mark as/i });
    await user.click(toggleButton);
    
    await waitFor(() => {
      expect(screen.getByText('Failed to update todo')).toBeInTheDocument();
    });
  });

  test('shows error message on delete failure', async () => {
    const user = userEvent.setup();
    window.confirm = jest.fn(() => true);
    mockCallbacks.onDelete.mockRejectedValueOnce(new Error('Delete failed'));
    
    renderWithProviders(
      <TodoItem 
        todo={mockTodo} 
        onToggle={mockCallbacks.onToggle} 
        onDelete={mockCallbacks.onDelete} 
      />
    );
    
    const deleteButton = screen.getByRole('button', { name: /delete/i });
    await user.click(deleteButton);
    
    await waitFor(() => {
      expect(screen.getByText('Failed to delete todo')).toBeInTheDocument();
    });
  });

  test('can dismiss error messages', async () => {
    const user = userEvent.setup();
    mockCallbacks.onToggle.mockRejectedValueOnce(new Error('Toggle failed'));
    
    renderWithProviders(
      <TodoItem 
        todo={mockTodo} 
        onToggle={mockCallbacks.onToggle} 
        onDelete={mockCallbacks.onDelete} 
      />
    );
    
    const toggleButton = screen.getByRole('button', { name: /mark as/i });
    await user.click(toggleButton);
    
    await waitFor(() => {
      expect(screen.getByText('Failed to update todo')).toBeInTheDocument();
    });
    
    const dismissButton = screen.getByText('✕');
    await user.click(dismissButton);
    
    expect(screen.queryByText('Failed to update todo')).not.toBeInTheDocument();
  });

  test('prevents multiple simultaneous operations', async () => {
    const user = userEvent.setup();
    mockCallbacks.onToggle.mockImplementationOnce(
      () => new Promise(resolve => setTimeout(resolve, 100))
    );
    
    renderWithProviders(
      <TodoItem 
        todo={mockTodo} 
        onToggle={mockCallbacks.onToggle} 
        onDelete={mockCallbacks.onDelete} 
      />
    );
    
    const toggleButton = screen.getByRole('button', { name: /mark as/i });
    const deleteButton = screen.getByRole('button', { name: /delete/i });
    
    await user.click(toggleButton);
    
    expect(deleteButton).toBeDisabled();
    expect(mockCallbacks.onToggle).toHaveBeenCalledTimes(1);
  });
});