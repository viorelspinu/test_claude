import React from 'react';
import TodoItem from './TodoItem';

function TodoList({ todos, onToggle, onEdit, onDelete, disabled = false }) {
  if (todos.length === 0) {
    return (
      <div className="todo-list-empty">
        <p>No todos yet. Add one above!</p>
      </div>
    );
  }

  return (
    <div className={`todo-list ${disabled ? 'disabled' : ''}`}>
      <h2>Your Todos ({todos.length})</h2>
      {disabled && (
        <div className="offline-warning">
          📱 Cannot modify todos while offline
        </div>
      )}
      <ul className="todo-items">
        {todos.map(todo => (
          <TodoItem 
            key={todo.id} 
            todo={todo}
            onToggle={onToggle}
            onEdit={onEdit}
            onDelete={onDelete}
            disabled={disabled}
          />
        ))}
      </ul>
    </div>
  );
}

export default TodoList;