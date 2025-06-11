import React, { useState, useEffect } from 'react';
import TodoList from './components/TodoList';
import AddTodo from './components/AddTodo';
import { ToastContainer } from './components/Toast';
import { fetchTodos, createTodo, updateTodo, updateTodoText, deleteTodo } from './api/todoApi';
import useToast from './hooks/useToast';
import useNetworkStatus from './hooks/useNetworkStatus';
import './App.css';

function App() {
  const [todos, setTodos] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [retryCount, setRetryCount] = useState(0);
  
  const { toasts, removeToast, showError, showSuccess, showWarning, showInfo } = useToast();
  const { isOnline, wasOffline } = useNetworkStatus();

  useEffect(() => {
    loadTodos();
  }, []);

  useEffect(() => {
    if (isOnline && wasOffline) {
      showInfo('Connection restored! Refreshing data...');
      loadTodos();
    }
  }, [isOnline, wasOffline]);

  useEffect(() => {
    if (!isOnline) {
      showWarning('You are offline. Some features may not work.');
    }
  }, [isOnline]);

  const loadTodos = async (showSuccessMessage = false) => {
    try {
      setLoading(true);
      const todosData = await fetchTodos();
      setTodos(todosData);
      setError(null);
      setRetryCount(0);
      
      if (showSuccessMessage) {
        showSuccess('Todos loaded successfully!');
      }
    } catch (err) {
      const errorMessage = err.message || 'Failed to load todos';
      setError(errorMessage);
      
      if (!isOnline) {
        showError('Cannot load todos while offline. Please check your connection.');
      } else {
        showError(`Failed to load todos: ${errorMessage}`);
      }
      
      console.error('Error loading todos:', err);
    } finally {
      setLoading(false);
    }
  };

  const handleAddTodo = async (text) => {
    if (!isOnline) {
      showError('Cannot create todos while offline. Please check your connection.');
      throw new Error('Offline');
    }

    try {
      const newTodo = await createTodo(text);
      setTodos(prevTodos => [...prevTodos, newTodo]);
      setError(null);
      showSuccess('Todo created successfully!');
    } catch (err) {
      const errorMessage = err.message || 'Failed to create todo';
      setError(errorMessage);
      showError(`Failed to create todo: ${errorMessage}`);
      console.error('Error creating todo:', err);
      throw err;
    }
  };

  const handleToggleTodo = async (todoId, completed) => {
    if (!isOnline) {
      showError('Cannot update todos while offline. Please check your connection.');
      throw new Error('Offline');
    }

    try {
      const updatedTodo = await updateTodo(todoId, { completed });
      setTodos(prevTodos => 
        prevTodos.map(todo => 
          todo.id === todoId ? updatedTodo : todo
        )
      );
      setError(null);
      showSuccess(`Todo marked as ${completed ? 'complete' : 'incomplete'}!`);
    } catch (err) {
      const errorMessage = err.message || 'Failed to update todo';
      setError(errorMessage);
      showError(`Failed to update todo: ${errorMessage}`);
      console.error('Error updating todo:', err);
      throw err;
    }
  };

  const handleEditTodo = async (todoId, newText) => {
    if (!isOnline) {
      showError('Cannot edit todos while offline. Please check your connection.');
      throw new Error('Offline');
    }

    try {
      const updatedTodo = await updateTodoText(todoId, newText);
      setTodos(prevTodos => 
        prevTodos.map(todo => 
          todo.id === todoId ? updatedTodo : todo
        )
      );
      setError(null);
      showSuccess('Todo updated successfully!');
    } catch (err) {
      const errorMessage = err.message || 'Failed to edit todo';
      setError(errorMessage);
      showError(`Failed to edit todo: ${errorMessage}`);
      console.error('Error editing todo:', err);
      throw err;
    }
  };

  const handleDeleteTodo = async (todoId) => {
    if (!isOnline) {
      showError('Cannot delete todos while offline. Please check your connection.');
      throw new Error('Offline');
    }

    try {
      await deleteTodo(todoId);
      setTodos(prevTodos => prevTodos.filter(todo => todo.id !== todoId));
      setError(null);
      showSuccess('Todo deleted successfully!');
    } catch (err) {
      const errorMessage = err.message || 'Failed to delete todo';
      setError(errorMessage);
      showError(`Failed to delete todo: ${errorMessage}`);
      console.error('Error deleting todo:', err);
      throw err;
    }
  };

  const handleRetry = () => {
    setRetryCount(prev => prev + 1);
    loadTodos(true);
  };

  return (
    <div className="App">
      <header className="App-header">
        <h1>Todo App</h1>
        {!isOnline && (
          <div className="offline-indicator">
            📱 Offline Mode
          </div>
        )}
      </header>
      <main className="App-main">
        <AddTodo onAdd={handleAddTodo} disabled={!isOnline} />
        
        {error && (
          <div className="error-container">
            <div className="error-message">{error}</div>
            <button className="retry-button" onClick={handleRetry}>
              🔄 Retry
            </button>
          </div>
        )}
        
        {loading ? (
          <div className="loading-container">
            <div className="loading-spinner"></div>
            <div className="loading-text">Loading todos...</div>
          </div>
        ) : (
          <TodoList 
            todos={todos} 
            onToggle={handleToggleTodo}
            onEdit={handleEditTodo}
            onDelete={handleDeleteTodo}
            disabled={!isOnline}
          />
        )}
      </main>
      
      <ToastContainer toasts={toasts} removeToast={removeToast} />
    </div>
  );
}

export default App;
