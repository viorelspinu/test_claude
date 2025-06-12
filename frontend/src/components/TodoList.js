import React, { useState, useEffect } from 'react';
import { getTodos } from '../services/api';

/**
 * TodoList Component
 * Container component for displaying and managing the list of todos
 */
function TodoList() {
  const [todos, setTodos] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  /**
   * Fetch todos from API on component mount
   */
  useEffect(() => {
    const fetchTodos = async () => {
      try {
        setLoading(true);
        setError(null);
        const todosData = await getTodos();
        setTodos(todosData || []);
      } catch (err) {
        console.error('Failed to fetch todos:', err);
        setError(err.message || 'Failed to load todos');
      } finally {
        setLoading(false);
      }
    };

    fetchTodos();
  }, []);

  /**
   * Retry loading todos after error
   */
  const handleRetry = () => {
    setError(null);
    setLoading(true);
    // Re-trigger useEffect by forcing re-render
    setTodos([]);
  };

  // Loading state
  if (loading) {
    return (
      <div className="todo-list">
        <div className="loading">Loading todos...</div>
      </div>
    );
  }

  // Error state
  if (error) {
    return (
      <div className="todo-list">
        <div className="error">
          <p>Error: {error}</p>
          <button onClick={handleRetry} className="retry-button">
            Retry
          </button>
        </div>
      </div>
    );
  }

  // Empty state
  if (todos.length === 0) {
    return (
      <div className="todo-list">
        <div className="empty-state">
          <p>No todos yet. Add your first todo!</p>
        </div>
      </div>
    );
  }

  // Todo list display
  return (
    <div className="todo-list">
      <h2>Todo List ({todos.length})</h2>
      <div className="todos-container">
        {todos.map((todo) => (
          <div key={todo.id} className="todo-item-placeholder">
            <span className={`todo-text ${todo.completed ? 'completed' : ''}`}>
              {todo.text}
            </span>
            <span className="todo-status">
              {todo.completed ? '✅' : '⏳'}
            </span>
          </div>
        ))}
      </div>
    </div>
  );
}

export default TodoList;