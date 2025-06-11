import React, { useState, useEffect } from 'react';
import axios from 'axios';

function TodoList() {
  const [todos, setTodos] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  const fetchTodos = async () => {
    try {
      setLoading(true);
      const response = await axios.get('http://localhost:5001/api/todos');
      setTodos(response.data);
      setError(null);
    } catch (err) {
      setError('Failed to fetch todos');
      console.error('Error fetching todos:', err);
    } finally {
      setLoading(false);
    }
  };

  const toggleTodo = async (todoId, currentCompleted) => {
    try {
      // Optimistic update
      setTodos(todos.map(todo => 
        todo.id === todoId 
          ? { ...todo, completed: !currentCompleted }
          : todo
      ));

      await axios.put(`http://localhost:5001/api/todos/${todoId}`, {
        completed: !currentCompleted
      });
    } catch (err) {
      // Revert on error
      setTodos(todos.map(todo => 
        todo.id === todoId 
          ? { ...todo, completed: currentCompleted }
          : todo
      ));
      setError('Failed to update todo');
      console.error('Error updating todo:', err);
    }
  };

  const deleteTodo = async (todoId) => {
    if (!window.confirm('Are you sure you want to delete this todo?')) {
      return;
    }

    try {
      // Optimistic update
      const originalTodos = [...todos];
      setTodos(todos.filter(todo => todo.id !== todoId));

      await axios.delete(`http://localhost:5001/api/todos/${todoId}`);
    } catch (err) {
      // Revert on error
      setTodos(originalTodos);
      setError('Failed to delete todo');
      console.error('Error deleting todo:', err);
    }
  };

  useEffect(() => {
    fetchTodos();
  }, []);

  if (loading) return <div className="loading">Loading todos...</div>;
  if (error) return <div className="error">Error: {error}</div>;

  return (
    <div className="todo-list">
      <h2>Todo List ({todos.length})</h2>
      {todos.length === 0 ? (
        <p className="empty-state">No todos yet. Add one to get started!</p>
      ) : (
        <ul>
          {todos.map(todo => (
            <li key={todo.id}>
              <div 
                className="todo-item-content"
                onClick={() => toggleTodo(todo.id, todo.completed)}
              >
                <span className="todo-status">
                  {todo.completed ? '✓' : '○'}
                </span>
                <span className={`todo-text ${todo.completed ? 'completed' : ''}`}>
                  {todo.text}
                </span>
                <small className="todo-date">
                  {new Date(todo.created_at).toLocaleDateString()}
                </small>
              </div>
              <button 
                className="delete-btn"
                onClick={(e) => {
                  e.stopPropagation();
                  deleteTodo(todo.id);
                }}
              >
                Delete
              </button>
            </li>
          ))}
        </ul>
      )}
    </div>
  );
}

export default TodoList;