import React, { useState, useEffect } from 'react';
import { PRIORITIES, PRIORITY_OPTIONS, VALIDATION_RULES, MESSAGES } from '../../utils/constants.js';
import { ApiError } from '../../services/api.js';
import './TaskForm.css';

const TaskForm = ({ 
  onSubmit, 
  onCancel, 
  initialTask = null, 
  isEditing = false,
  isSubmitting = false 
}) => {
  const [formData, setFormData] = useState({
    title: '',
    description: '',
    priority: PRIORITIES.MEDIUM
  });
  
  const [errors, setErrors] = useState({});
  const [touched, setTouched] = useState({});

  // Initialize form with task data for editing
  useEffect(() => {
    if (initialTask && isEditing) {
      setFormData({
        title: initialTask.title || '',
        description: initialTask.description || '',
        priority: initialTask.priority || PRIORITIES.MEDIUM
      });
    } else {
      // Reset form for new task
      setFormData({
        title: '',
        description: '',
        priority: PRIORITIES.MEDIUM
      });
    }
    
    // Clear errors and touched state when switching modes
    setErrors({});
    setTouched({});
  }, [initialTask, isEditing]);

  // Validate individual field
  const validateField = (name, value) => {
    switch (name) {
      case 'title':
        if (!value || value.trim().length === 0) {
          return 'Title is required';
        }
        if (value.trim().length > VALIDATION_RULES.TITLE.maxLength) {
          return `Title must be ${VALIDATION_RULES.TITLE.maxLength} characters or less`;
        }
        return '';
        
      case 'description':
        if (value && value.length > VALIDATION_RULES.DESCRIPTION.maxLength) {
          return `Description must be ${VALIDATION_RULES.DESCRIPTION.maxLength} characters or less`;
        }
        return '';
        
      case 'priority':
        if (!Object.values(PRIORITIES).includes(value)) {
          return 'Please select a valid priority';
        }
        return '';
        
      default:
        return '';
    }
  };

  // Validate entire form
  const validateForm = () => {
    const newErrors = {};
    
    Object.keys(formData).forEach(field => {
      const error = validateField(field, formData[field]);
      if (error) {
        newErrors[field] = error;
      }
    });
    
    return newErrors;
  };

  // Handle input changes
  const handleChange = (e) => {
    const { name, value } = e.target;
    
    setFormData(prev => ({
      ...prev,
      [name]: value
    }));
    
    // Clear error for this field if it becomes valid
    if (touched[name]) {
      const fieldError = validateField(name, value);
      setErrors(prev => ({
        ...prev,
        [name]: fieldError
      }));
    }
  };

  // Handle field blur (mark as touched)
  const handleBlur = (e) => {
    const { name, value } = e.target;
    
    setTouched(prev => ({
      ...prev,
      [name]: true
    }));
    
    // Validate field on blur
    const fieldError = validateField(name, value);
    setErrors(prev => ({
      ...prev,
      [name]: fieldError
    }));
  };

  // Handle form submission
  const handleSubmit = async (e) => {
    e.preventDefault();
    
    // Mark all fields as touched
    const allTouched = Object.keys(formData).reduce((acc, key) => {
      acc[key] = true;
      return acc;
    }, {});
    setTouched(allTouched);
    
    // Validate form
    const formErrors = validateForm();
    setErrors(formErrors);
    
    // Don't submit if there are errors
    if (Object.keys(formErrors).length > 0) {
      return;
    }
    
    // Prepare data for submission
    const submitData = {
      title: formData.title.trim(),
      priority: formData.priority
    };
    
    // Only include description if it's not empty
    if (formData.description && formData.description.trim()) {
      submitData.description = formData.description.trim();
    }
    
    try {
      await onSubmit(submitData);
      
      // Reset form if creating new task
      if (!isEditing) {
        setFormData({
          title: '',
          description: '',
          priority: PRIORITIES.MEDIUM
        });
        setTouched({});
        setErrors({});
      }
    } catch (error) {
      console.error('Form submission error:', error);
      
      // Handle API validation errors
      if (error instanceof ApiError && error.isValidationError()) {
        const apiErrors = {};
        
        if (error.details) {
          Object.keys(error.details).forEach(field => {
            apiErrors[field] = error.details[field];
          });
        } else {
          apiErrors.general = error.message;
        }
        
        setErrors(prev => ({ ...prev, ...apiErrors }));
      } else {
        setErrors(prev => ({
          ...prev,
          general: error.message || MESSAGES.ERROR_GENERIC
        }));
      }
    }
  };

  // Handle cancel
  const handleCancel = () => {
    if (onCancel) {
      onCancel();
    }
    
    // Reset form
    if (!isEditing) {
      setFormData({
        title: '',
        description: '',
        priority: PRIORITIES.MEDIUM
      });
      setTouched({});
      setErrors({});
    }
  };

  // Calculate character counts
  const titleCharCount = formData.title.length;
  const descriptionCharCount = formData.description.length;

  return (
    <div className="task-form-container">
      <form onSubmit={handleSubmit} className="task-form" noValidate>
        <div className="form-header">
          <h3>{isEditing ? 'Edit Task' : 'Create New Task'}</h3>
        </div>

        {/* General Error Message */}
        {errors.general && (
          <div className="error-message general-error">
            {errors.general}
          </div>
        )}

        {/* Title Field */}
        <div className="form-group">
          <label htmlFor="title" className="form-label">
            Title <span className="required">*</span>
          </label>
          <input
            type="text"
            id="title"
            name="title"
            value={formData.title}
            onChange={handleChange}
            onBlur={handleBlur}
            className={`form-input ${errors.title ? 'error' : ''}`}
            placeholder="Enter task title..."
            maxLength={VALIDATION_RULES.TITLE.maxLength}
            disabled={isSubmitting}
            aria-describedby={errors.title ? 'title-error' : 'title-hint'}
          />
          <div className="form-hint">
            <span className="char-count">
              {titleCharCount}/{VALIDATION_RULES.TITLE.maxLength}
            </span>
          </div>
          {errors.title && (
            <div id="title-error" className="error-message">
              {errors.title}
            </div>
          )}
        </div>

        {/* Description Field */}
        <div className="form-group">
          <label htmlFor="description" className="form-label">
            Description
          </label>
          <textarea
            id="description"
            name="description"
            value={formData.description}
            onChange={handleChange}
            onBlur={handleBlur}
            className={`form-textarea ${errors.description ? 'error' : ''}`}
            placeholder="Enter task description (optional)..."
            rows={4}
            maxLength={VALIDATION_RULES.DESCRIPTION.maxLength}
            disabled={isSubmitting}
            aria-describedby={errors.description ? 'description-error' : 'description-hint'}
          />
          <div className="form-hint">
            <span className="char-count">
              {descriptionCharCount}/{VALIDATION_RULES.DESCRIPTION.maxLength}
            </span>
          </div>
          {errors.description && (
            <div id="description-error" className="error-message">
              {errors.description}
            </div>
          )}
        </div>

        {/* Priority Field */}
        <div className="form-group">
          <label htmlFor="priority" className="form-label">
            Priority
          </label>
          <select
            id="priority"
            name="priority"
            value={formData.priority}
            onChange={handleChange}
            onBlur={handleBlur}
            className={`form-select ${errors.priority ? 'error' : ''}`}
            disabled={isSubmitting}
            aria-describedby={errors.priority ? 'priority-error' : undefined}
          >
            {PRIORITY_OPTIONS.map(option => (
              <option key={option.value} value={option.value}>
                {option.label}
              </option>
            ))}
          </select>
          {errors.priority && (
            <div id="priority-error" className="error-message">
              {errors.priority}
            </div>
          )}
        </div>

        {/* Form Actions */}
        <div className="form-actions">
          {isEditing && (
            <button
              type="button"
              onClick={handleCancel}
              className="btn btn-secondary"
              disabled={isSubmitting}
            >
              Cancel
            </button>
          )}
          
          <button
            type="submit"
            className="btn btn-primary"
            disabled={isSubmitting || Object.keys(validateForm()).length > 0}
          >
            {isSubmitting ? (
              <>
                <span className="spinner"></span>
                {isEditing ? 'Updating...' : 'Creating...'}
              </>
            ) : (
              isEditing ? 'Update Task' : 'Create Task'
            )}
          </button>
        </div>
      </form>
    </div>
  );
};

export default TaskForm;