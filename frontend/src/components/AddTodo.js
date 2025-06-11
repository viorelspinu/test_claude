import React, { useState } from 'react';
import axios from 'axios';

function AddTodo({ onTodoAdded }) {
  const [text, setText] = useState('');
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  const handleSubmit = async (e) => {
    e.preventDefault();
    
    if (!text.trim()) {
      setError('Please enter a todo text');
      return;
    }

    try {
      setLoading(true);
      setError(null);
      
      await axios.post('http://localhost:5001/api/todos', {
        text: text.trim()
      });
      
      setText('');
      if (onTodoAdded) onTodoAdded();
    } catch (err) {
      setError('Failed to add todo');
      console.error('Error adding todo:', err);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="add-todo">
      <h3>Add New Todo</h3>
      <form onSubmit={handleSubmit}>
        <input
          type="text"
          value={text}
          onChange={(e) => setText(e.target.value)}
          placeholder="Enter todo text..."
          disabled={loading}
        />
        <button type="submit" disabled={loading || !text.trim()}>
          {loading ? 'Adding...' : 'Add Todo'}
        </button>
      </form>
      {error && <div className="error">{error}</div>}
    </div>
  );
}

export default AddTodo;