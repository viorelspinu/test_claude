import React from 'react';
import TodoItem from './TodoItem';
import './TodoList.css';

/**
 * TodoList Component
 * Container component for displaying and managing the list of todos
 * 
 * @param {Object} props - Component props
 * @param {Array} props.todos - Array of todo objects
 * @param {Function} props.onToggle - Callback for toggling todo completion
 * @param {Function} props.onUpdate - Callback for updating todo text
 * @param {Function} props.onDelete - Callback for deleting todo
 */
function TodoList({ todos, onToggle, onUpdate, onDelete }) {

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
          <TodoItem
            key={todo.id}
            todo={todo}
            onToggle={onToggle}
            onUpdate={onUpdate}
            onDelete={onDelete}
          />
        ))}
      </div>
    </div>
  );
}

export default TodoList;