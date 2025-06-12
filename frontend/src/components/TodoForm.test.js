import React from 'react';
import { screen, fireEvent, waitFor } from '@testing-library/react';
import TodoForm from './TodoForm';
import { renderWithProviders, mockCallbacks, resetMocks } from '../test-utils/test-utils';

// Reset mocks before each test
beforeEach(() => {
  resetMocks();
});

describe('TodoForm', () => {
  test('renders form with input and button', () => {
    renderWithProviders(<TodoForm onAddTodo={mockCallbacks.onAddTodo} />);
    
    expect(screen.getByPlaceholderText('What needs to be done?')).toBeInTheDocument();
    expect(screen.getByRole('button')).toBeInTheDocument();
  });

  test('shows character counter', () => {
    renderWithProviders(<TodoForm onAddTodo={mockCallbacks.onAddTodo} />);
    
    expect(screen.getByText(/0\/500 characters/)).toBeInTheDocument();
  });

  test('updates character counter when typing', () => {
    renderWithProviders(<TodoForm onAddTodo={mockCallbacks.onAddTodo} />);
    
    const input = screen.getByPlaceholderText('What needs to be done?');
    fireEvent.change(input, { target: { value: 'Test todo' } });
    
    expect(screen.getByText(/9\/500 characters/)).toBeInTheDocument();
  });

  test('submits form when form submitted', () => {
    const { container } = renderWithProviders(<TodoForm onAddTodo={mockCallbacks.onAddTodo} />);
    
    const input = screen.getByPlaceholderText('What needs to be done?');
    const form = container.querySelector('form');
    
    fireEvent.change(input, { target: { value: 'New todo' } });
    fireEvent.submit(form);
    
    expect(mockCallbacks.onAddTodo).toHaveBeenCalledWith('New todo');
  });

  test('shows validation error for empty input', () => {
    const { container } = renderWithProviders(<TodoForm onAddTodo={mockCallbacks.onAddTodo} />);
    
    const form = container.querySelector('form');
    fireEvent.submit(form);
    
    expect(screen.getByText('Please enter a todo text')).toBeInTheDocument();
    expect(mockCallbacks.onAddTodo).not.toHaveBeenCalled();
  });

  test('disables submit button when input is empty', () => {
    renderWithProviders(<TodoForm onAddTodo={mockCallbacks.onAddTodo} />);
    
    const button = screen.getByRole('button');
    expect(button).toBeDisabled();
  });

  test('enables submit button when input has text', () => {
    renderWithProviders(<TodoForm onAddTodo={mockCallbacks.onAddTodo} />);
    
    const input = screen.getByPlaceholderText('What needs to be done?');
    const button = screen.getByRole('button');
    
    fireEvent.change(input, { target: { value: 'Test' } });
    
    expect(button).not.toBeDisabled();
  });

  test('clears input after successful submission', async () => {
    mockCallbacks.onAddTodo.mockResolvedValueOnce({ id: '1', text: 'New todo' });
    
    const { container } = renderWithProviders(<TodoForm onAddTodo={mockCallbacks.onAddTodo} />);
    
    const input = screen.getByPlaceholderText('What needs to be done?');
    const form = container.querySelector('form');
    
    fireEvent.change(input, { target: { value: 'New todo' } });
    fireEvent.submit(form);
    
    await waitFor(() => {
      expect(input.value).toBe('');
    });
  });
});