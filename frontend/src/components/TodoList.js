import React, { useState, useEffect } from 'react';
import axios from 'axios';

function TodoList() {
  const [todos, setTodos] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  const fetchTodos = async () => {
    try {
      setLoading(true);
      const response = await axios.get('http://localhost:5000/api/todos');
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

      await axios.put(`http://localhost:5000/api/todos/${todoId}`, {
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

      await axios.delete(`http://localhost:5000/api/todos/${todoId}`);
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

  if (loading) return <div>Loading todos...</div>;
  if (error) return <div>Error: {error}</div>;

  return (
    <div className="todo-list">
      <h2>Todo List ({todos.length})</h2>
      {todos.length === 0 ? (
        <p>No todos yet. Add one to get started!</p>
      ) : (
        <ul>
          {todos.map(todo => (
            <li 
              key={todo.id} 
              className={todo.completed ? 'completed' : ''}
              style={{ 
                display: 'flex', 
                alignItems: 'center', 
                justifyContent: 'space-between',
                padding: '8px',
                borderBottom: '1px solid #eee'
              }}
            >
              <div 
                onClick={() => toggleTodo(todo.id, todo.completed)}
                style={{ cursor: 'pointer', flex: 1, display: 'flex', alignItems: 'center' }}
              >
                <span className="status" style={{ marginRight: '8px' }}>
                  {todo.completed ? '✓' : '○'}
                </span>
                <span style={{ 
                  textDecoration: todo.completed ? 'line-through' : 'none',
                  opacity: todo.completed ? 0.6 : 1,
                  marginRight: '10px'
                }}>
                  {todo.text}
                </span>
                <small style={{ opacity: 0.7 }}>
                  {new Date(todo.created_at).toLocaleDateString()}
                </small>
              </div>
              <button 
                onClick={(e) => {
                  e.stopPropagation();
                  deleteTodo(todo.id);
                }}
                style={{
                  background: '#ff4444',
                  color: 'white',
                  border: 'none',
                  borderRadius: '4px',
                  padding: '4px 8px',
                  cursor: 'pointer',
                  fontSize: '12px'
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