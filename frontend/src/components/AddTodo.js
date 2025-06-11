import React, { useState } from 'react';

function AddTodo({ onAdd, disabled = false }) {
  const [text, setText] = useState('');
  const [isLoading, setIsLoading] = useState(false);

  const handleSubmit = async (e) => {
    e.preventDefault();
    
    const trimmedText = text.trim();
    if (!trimmedText) return;

    setIsLoading(true);
    try {
      await onAdd(trimmedText);
      setText('');
    } catch (error) {
      console.error('Error adding todo:', error);
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div className={`add-todo ${disabled ? 'disabled' : ''}`}>
      <h2>Add New Todo</h2>
      {disabled && (
        <div className="offline-warning">
          📱 Cannot create todos while offline
        </div>
      )}
      <form onSubmit={handleSubmit} className="add-todo-form">
        <div className="input-group">
          <input
            type="text"
            value={text}
            onChange={(e) => setText(e.target.value)}
            placeholder={disabled ? "Offline - cannot create todos" : "Enter your todo..."}
            maxLength={200}
            disabled={isLoading || disabled}
            className="todo-input"
          />
          <button 
            type="submit" 
            disabled={!text.trim() || isLoading || disabled}
            className="add-button"
          >
            {isLoading ? 'Adding...' : disabled ? 'Offline' : 'Add Todo'}
          </button>
        </div>
        <small className="char-count">
          {text.length}/200 characters
        </small>
      </form>
    </div>
  );
}

export default AddTodo;