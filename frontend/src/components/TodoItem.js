import React from 'react';
import './TodoItem.css';

const TodoItem = ({ todo, onToggle, onDelete, onEdit }) => {
  const handleToggle = () => {
    onToggle(todo.id, { ...todo, completed: !todo.completed });
  };

  const handleDelete = () => {
    onDelete(todo.id);
  };

  const handleEdit = () => {
    const newTitle = prompt('Edit todo title:', todo.title);
    const newDescription = prompt('Edit todo description:', todo.description);
    
    if (newTitle !== null) {
      onEdit(todo.id, {
        ...todo,
        title: newTitle,
        description: newDescription || todo.description
      });
    }
  };

  return (
    <div className={`todo-item ${todo.completed ? 'completed' : ''}`}>
      <div className="todo-content">
        <h3 className="todo-title">{todo.title}</h3>
        {todo.description && (
          <p className="todo-description">{todo.description}</p>
        )}
        <span className="todo-date">
          Created: {new Date(todo.created_at).toLocaleDateString()}
        </span>
      </div>
      <div className="todo-actions">
        <button 
          className={`toggle-btn ${todo.completed ? 'completed' : 'active'}`}
          onClick={handleToggle}
        >
          {todo.completed ? '✓' : '○'}
        </button>
        <button className="edit-btn" onClick={handleEdit}>
          ✏️
        </button>
        <button className="delete-btn" onClick={handleDelete}>
          🗑️
        </button>
      </div>
    </div>
  );
};

export default TodoItem;