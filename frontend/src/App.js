import React, { useState } from 'react';
import TodoList from './components/TodoList';
import AddTodo from './components/AddTodo';

function App() {
  const [refreshTrigger, setRefreshTrigger] = useState(0);

  const handleTodoAdded = () => {
    setRefreshTrigger(prev => prev + 1);
  };

  return (
    <div className="App">
      <h1>Todo App</h1>
      <AddTodo onTodoAdded={handleTodoAdded} />
      <TodoList key={refreshTrigger} />
    </div>
  );
}

export default App;