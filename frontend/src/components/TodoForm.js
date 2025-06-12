import React, { useState } from 'react';
import './TodoForm.css';

/**
 * TodoForm Component
 * Provides interface for creating new todos
 * 
 * @param {Object} props - Component props
 * @param {Function} props.onAddTodo - Callback for todo creation
 */
function TodoForm({ onAddTodo }) {
  const [inputValue, setInputValue] = useState('');
  const [isSubmitting, setIsSubmitting] = useState(false);
  const [error, setError] = useState(null);

  /**
   * Handle form submission
   */
  const handleSubmit = async (e) => {
    e.preventDefault();
    
    const trimmedValue = inputValue.trim();
    
    // Validation
    if (!trimmedValue) {
      setError('Please enter a todo text');
      return;
    }

    if (trimmedValue.length > 500) {
      setError('Todo text must be less than 500 characters');
      return;
    }

    try {
      setIsSubmitting(true);
      setError(null);
      
      await onAddTodo(trimmedValue);
      
      // Clear form on success
      setInputValue('');
    } catch (err) {
      console.error('Failed to add todo:', err);
      setError(err.message || 'Failed to add todo');
    } finally {
      setIsSubmitting(false);
    }
  };

  /**
   * Handle input change
   */
  const handleInputChange = (e) => {
    setInputValue(e.target.value);
    // Clear error when user starts typing
    if (error) {
      setError(null);
    }
  };

  /**
   * Handle key press for Enter submission
   */
  const handleKeyPress = (e) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault();
      handleSubmit(e);
    }
  };

  /**
   * Clear error message
   */
  const clearError = () => {
    setError(null);
  };

  return (
    <div className="todo-form">
      <form onSubmit={handleSubmit} className="todo-form-container">
        <div className="input-container">
          <input
            type="text"
            value={inputValue}
            onChange={handleInputChange}
            onKeyPress={handleKeyPress}
            placeholder="What needs to be done?"
            className={`todo-input ${error ? 'error' : ''}`}
            disabled={isSubmitting}
            maxLength={500}
            autoFocus
          />
          <button
            type="submit"
            className="add-button"
            disabled={isSubmitting || !inputValue.trim()}
          >
            {isSubmitting ? '⏳' : '➕'}
          </button>
        </div>
        
        {error && (
          <div className="form-error">
            <span className="error-message">{error}</span>
            <button 
              type="button"
              className="clear-error-button"
              onClick={clearError}
            >
              ✕
            </button>
          </div>
        )}
        
        <div className="form-hint">
          <span className="hint-text">
            Press Enter to add • {inputValue.length}/500 characters
          </span>
        </div>
      </form>
    </div>
  );
}

export default TodoForm;