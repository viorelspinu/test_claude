import React, { useState, useEffect } from 'react';
import './App.css';
import TodoForm from './components/TodoForm';
import TodoList from './components/TodoList';
import { getTodos, createTodo, updateTodo, deleteTodo } from './services/api';

/**
 * Main App Component
 * Integrates all todo components and manages global state
 */
function App() {
  const [todos, setTodos] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  /**
   * Load todos on app initialization
   */
  useEffect(() => {
    loadTodos();
  }, []);

  /**
   * Load todos from API
   */
  const loadTodos = async () => {
    try {
      setLoading(true);
      setError(null);
      const todosData = await getTodos();
      setTodos(todosData || []);
    } catch (err) {
      console.error('Failed to load todos:', err);
      setError('Failed to load todos. Please try again.');
    } finally {
      setLoading(false);
    }
  };

  /**
   * Handle adding new todo
   */
  const handleAddTodo = async (text) => {
    try {
      const newTodo = await createTodo(text);
      setTodos(prevTodos => [...prevTodos, newTodo]);
      return newTodo;
    } catch (err) {
      console.error('Failed to add todo:', err);
      throw new Error(err.message || 'Failed to add todo');
    }
  };

  /**
   * Handle toggling todo completion
   */
  const handleToggleTodo = async (id) => {
    const todo = todos.find(t => t.id === id);
    if (!todo) return;

    try {
      const updatedTodo = await updateTodo(id, { completed: !todo.completed });
      setTodos(prevTodos =>
        prevTodos.map(t => t.id === id ? updatedTodo : t)
      );
      return updatedTodo;
    } catch (err) {
      console.error('Failed to toggle todo:', err);
      throw new Error(err.message || 'Failed to update todo');
    }
  };

  /**
   * Handle updating todo
   */
  const handleUpdateTodo = async (id, updates) => {
    try {
      const updatedTodo = await updateTodo(id, updates);
      setTodos(prevTodos =>
        prevTodos.map(t => t.id === id ? updatedTodo : t)
      );
      return updatedTodo;
    } catch (err) {
      console.error('Failed to update todo:', err);
      throw new Error(err.message || 'Failed to update todo');
    }
  };

  /**
   * Handle deleting todo
   */
  const handleDeleteTodo = async (id) => {
    try {
      await deleteTodo(id);
      setTodos(prevTodos => prevTodos.filter(t => t.id !== id));
    } catch (err) {
      console.error('Failed to delete todo:', err);
      throw new Error(err.message || 'Failed to delete todo');
    }
  };

  /**
   * Retry loading todos after error
   */
  const retryLoad = () => {
    loadTodos();
  };

  return (
    <div className="App">
      <header className="App-header">
        <h1>Todo Application</h1>
        <p>Manage your tasks efficiently</p>
      </header>

      <main className="App-main">
        {/* Add Todo Form */}
        <section className="todo-form-section">
          <TodoForm onAddTodo={handleAddTodo} />
        </section>

        {/* Todo List */}
        <section className="todo-list-section">
          {loading ? (
            <div className="app-loading">
              <p>Loading todos...</p>
            </div>
          ) : error ? (
            <div className="app-error">
              <p>Error: {error}</p>
              <button onClick={retryLoad} className="retry-button">
                Retry
              </button>
            </div>
          ) : (
            <TodoList 
              todos={todos}
              onToggle={handleToggleTodo}
              onUpdate={handleUpdateTodo}
              onDelete={handleDeleteTodo}
            />
          )}
        </section>
      </main>

      <footer className="App-footer">
        <p>Built with React and Flask</p>
      </footer>
    </div>
  );
}

export default App;