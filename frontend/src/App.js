import React, { useState, useEffect } from 'react';
import './App.css';
import TodoList from './components/TodoList';
import AddTodo from './components/AddTodo';

function App() {
  const [todos, setTodos] = useState([]);

  // Placeholder for API integration - for now using local state
  useEffect(() => {
    // This will be replaced with API call in next task
    console.log('App component mounted - ready for API integration');
  }, []);

  const addTodo = (text) => {
    // Placeholder for API call - creating local todo for now
    const newTodo = {
      id: Date.now(), // Temporary ID generation
      text: text,
      completed: false,
      created_at: new Date().toISOString()
    };
    setTodos([newTodo, ...todos]);
  };

  const toggleTodo = (id) => {
    // Placeholder for API call - updating local state for now
    setTodos(todos.map(todo => 
      todo.id === id 
        ? { ...todo, completed: !todo.completed }
        : todo
    ));
  };

  const deleteTodo = (id) => {
    // Placeholder for API call - updating local state for now
    setTodos(todos.filter(todo => todo.id !== id));
  };

  return (
    <div className="app">
      <header className="app-header">
        <h1>Todo App</h1>
      </header>
      <main className="app-main">
        <AddTodo onAdd={addTodo} />
        <TodoList 
          todos={todos} 
          onToggle={toggleTodo}
          onDelete={deleteTodo}
        />
      </main>
    </div>
  );
}

export default App;