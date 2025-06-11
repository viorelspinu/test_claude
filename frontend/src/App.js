import React, { useState, useEffect, useMemo } from 'react';
import TodoForm from './components/TodoForm';
import TodoList from './components/TodoList';
import TodoFilter from './components/TodoFilter';
import todoAPI from './services/api';
import './App.css';

function App() {
  const [todos, setTodos] = useState([]);
  const [filter, setFilter] = useState('all');
  const [isLoading, setIsLoading] = useState(true);
  const [error, setError] = useState(null);

  // Calculate todo counts
  const todoCounts = useMemo(() => {
    const total = todos.length;
    const completed = todos.filter(todo => todo.completed).length;
    const active = total - completed;
    return { total, active, completed };
  }, [todos]);

  // Load todos on component mount
  useEffect(() => {
    loadTodos();
  }, []);

  const loadTodos = async () => {
    try {
      setIsLoading(true);
      setError(null);
      const response = await todoAPI.getTodos();
      if (response.success) {
        setTodos(response.data);
      } else {
        setError('Failed to load todos');
      }
    } catch (error) {
      console.error('Error loading todos:', error);
      setError('Failed to connect to server. Please ensure the backend is running on port 8080.');
    } finally {
      setIsLoading(false);
    }
  };

  const handleCreateTodo = async (todoData) => {
    try {
      const response = await todoAPI.createTodo(todoData);
      if (response.success) {
        setTodos(prev => [...prev, response.data]);
      }
    } catch (error) {
      console.error('Error creating todo:', error);
      throw error;
    }
  };

  const handleToggleTodo = async (id, updatedTodo) => {
    try {
      const response = await todoAPI.updateTodo(id, updatedTodo);
      if (response.success) {
        setTodos(prev => prev.map(todo => 
          todo.id === id ? response.data : todo
        ));
      }
    } catch (error) {
      console.error('Error updating todo:', error);
    }
  };

  const handleEditTodo = async (id, updatedTodo) => {
    try {
      const response = await todoAPI.updateTodo(id, updatedTodo);
      if (response.success) {
        setTodos(prev => prev.map(todo => 
          todo.id === id ? response.data : todo
        ));
      }
    } catch (error) {
      console.error('Error updating todo:', error);
    }
  };

  const handleDeleteTodo = async (id) => {
    if (window.confirm('Are you sure you want to delete this todo?')) {
      try {
        const response = await todoAPI.deleteTodo(id);
        if (response.success) {
          setTodos(prev => prev.filter(todo => todo.id !== id));
        }
      } catch (error) {
        console.error('Error deleting todo:', error);
      }
    }
  };

  return (
    <div className="App">
      <header className="App-header">
        <h1>Todo App</h1>
        <p>Manage your tasks efficiently</p>
      </header>

      <main className="App-main">
        {error && (
          <div className="error-message">
            <p>{error}</p>
            <button onClick={loadTodos}>Retry</button>
          </div>
        )}

        {isLoading ? (
          <div className="loading">
            <p>Loading todos...</p>
          </div>
        ) : (
          <>
            <TodoForm onSubmit={handleCreateTodo} />
            
            <TodoFilter
              currentFilter={filter}
              onFilterChange={setFilter}
              todoCounts={todoCounts}
            />

            <TodoList
              todos={todos}
              filter={filter}
              onToggle={handleToggleTodo}
              onDelete={handleDeleteTodo}
              onEdit={handleEditTodo}
            />
          </>
        )}
      </main>
    </div>
  );
}

export default App;
