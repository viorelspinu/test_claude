import React, { useState } from 'react';
import './AddTodo.css';

function AddTodo({ onAdd }) {
  const [text, setText] = useState('');

  const handleSubmit = (e) => {
    e.preventDefault();
    
    const trimmedText = text.trim();
    if (!trimmedText) {
      return;
    }

    onAdd(trimmedText);
    setText('');
  };

  return (
    <form className="add-todo" onSubmit={handleSubmit}>
      <input
        type="text"
        value={text}
        onChange={(e) => setText(e.target.value)}
        placeholder="What needs to be done?"
        className="add-todo-input"
      />
      <button type="submit" className="add-todo-button">
        Add Todo
      </button>
    </form>
  );
}

export default AddTodo;