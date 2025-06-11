import React, { useState } from 'react';
import './TodoForm.css';

const TodoForm = ({ onSubmit }) => {
  const [title, setTitle] = useState('');
  const [description, setDescription] = useState('');
  const [isLoading, setIsLoading] = useState(false);

  const handleSubmit = async (e) => {
    e.preventDefault();
    
    if (!title.trim()) {
      alert('Please enter a todo title');
      return;
    }

    setIsLoading(true);
    try {
      await onSubmit({
        title: title.trim(),
        description: description.trim(),
        completed: false
      });
      
      // Reset form
      setTitle('');
      setDescription('');
    } catch (error) {
      console.error('Error submitting todo:', error);
      alert('Failed to create todo. Please try again.');
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <form className="todo-form" onSubmit={handleSubmit}>
      <h2>Add New Todo</h2>
      
      <div className="form-group">
        <label htmlFor="title">Title *</label>
        <input
          type="text"
          id="title"
          value={title}
          onChange={(e) => setTitle(e.target.value)}
          placeholder="Enter todo title..."
          disabled={isLoading}
          required
        />
      </div>

      <div className="form-group">
        <label htmlFor="description">Description</label>
        <textarea
          id="description"
          value={description}
          onChange={(e) => setDescription(e.target.value)}
          placeholder="Enter todo description..."
          rows="3"
          disabled={isLoading}
        />
      </div>

      <button 
        type="submit" 
        className="submit-btn"
        disabled={isLoading || !title.trim()}
      >
        {isLoading ? 'Adding...' : 'Add Todo'}
      </button>
    </form>
  );
};

export default TodoForm;