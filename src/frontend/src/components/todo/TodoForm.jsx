import React, { useState, useCallback, useRef, useEffect } from 'react'
import { useTodo } from '../../context/TodoContext'
import { getTodayString } from '../../utils/dateUtils'
import styles from './TodoForm.module.css'

const TodoForm = ({ onSubmit, onCancel }) => {
  const { actions, state } = useTodo()
  const titleInputRef = useRef(null)

  // Form state
  const [formData, setFormData] = useState({
    title: '',
    description: '',
    due_date: '',
    priority: 'Medium'
  })

  // Validation state
  const [validationErrors, setValidationErrors] = useState({})
  const [isSubmitting, setIsSubmitting] = useState(false)
  const [submitAttempted, setSubmitAttempted] = useState(false)

  // Focus management - focus title input when component mounts
  useEffect(() => {
    if (titleInputRef.current) {
      titleInputRef.current.focus()
    }
  }, [])

  // Clear error when user starts typing
  useEffect(() => {
    if (state.error && Object.keys(formData).some(key => formData[key])) {
      actions.clearError()
    }
  }, [formData, state.error, actions])

  // Validation rules
  const validateField = useCallback((name, value) => {
    const errors = {}

    switch (name) {
      case 'title':
        const trimmedTitle = value.trim()
        if (!trimmedTitle) {
          errors.title = 'Title is required'
        } else if (trimmedTitle.length > 100) {
          errors.title = 'Title must be 100 characters or less'
        } else if (!/^[a-zA-Z0-9\s.,!?:;\-_()[\]@#$%&*]+$/.test(trimmedTitle)) {
          errors.title = 'Title contains invalid characters'
        }
        break

      case 'description':
        if (value && value.length > 500) {
          errors.description = 'Description must be 500 characters or less'
        } else if (value && !/^[a-zA-Z0-9\s.,!?:;\-_()[\]@#$%&*]*$/.test(value)) {
          errors.description = 'Description contains invalid characters'
        }
        break

      case 'due_date':
        if (value) {
          const selectedDate = new Date(value)
          const today = new Date()
          today.setHours(0, 0, 0, 0)
          selectedDate.setHours(0, 0, 0, 0)
          
          if (selectedDate < today) {
            errors.due_date = 'Due date cannot be in the past'
          }
        }
        break

      case 'priority':
        if (!['Low', 'Medium', 'High'].includes(value)) {
          errors.priority = 'Priority must be Low, Medium, or High'
        }
        break

      default:
        break
    }

    return errors
  }, [])

  // Validate all fields
  const validateForm = useCallback(() => {
    let allErrors = {}
    
    Object.keys(formData).forEach(field => {
      const fieldErrors = validateField(field, formData[field])
      allErrors = { ...allErrors, ...fieldErrors }
    })

    return allErrors
  }, [formData, validateField])

  // Debounced validation for real-time feedback
  const [validationTimeout, setValidationTimeout] = useState(null)
  
  const debouncedValidation = useCallback((name, value) => {
    if (validationTimeout) {
      clearTimeout(validationTimeout)
    }

    const timeout = setTimeout(() => {
      if (submitAttempted || validationErrors[name]) {
        const errors = validateField(name, value)
        setValidationErrors(prev => ({
          ...prev,
          [name]: errors[name] || undefined
        }))
      }
    }, 300)

    setValidationTimeout(timeout)
  }, [validateField, validationErrors, submitAttempted, validationTimeout])

  // Handle input changes
  const handleInputChange = useCallback((e) => {
    const { name, value } = e.target
    
    setFormData(prev => ({
      ...prev,
      [name]: value
    }))

    // Real-time validation
    debouncedValidation(name, value)
  }, [debouncedValidation])

  // Handle form submission
  const handleSubmit = async (e) => {
    e.preventDefault()
    setSubmitAttempted(true)

    // Validate form
    const errors = validateForm()
    setValidationErrors(errors)

    if (Object.keys(errors).length > 0) {
      // Focus first field with error
      const firstErrorField = Object.keys(errors)[0]
      const errorElement = document.querySelector(`[name="${firstErrorField}"]`)
      if (errorElement) {
        errorElement.focus()
      }
      return
    }

    setIsSubmitting(true)

    try {
      // Prepare data for submission
      const submitData = {
        title: formData.title.trim(),
        description: formData.description.trim() || undefined,
        due_date: formData.due_date || undefined,
        priority: formData.priority
      }

      // Remove undefined values
      Object.keys(submitData).forEach(key => {
        if (submitData[key] === undefined) {
          delete submitData[key]
        }
      })

      // Create todo via context
      const newTodo = await actions.createTodo(submitData)

      // Reset form on success
      handleReset()

      // Call onSubmit callback if provided
      if (onSubmit) {
        onSubmit(newTodo)
      }

    } catch (error) {
      console.error('Form submission error:', error)
      // Error is handled by the context and displayed via global error state
    } finally {
      setIsSubmitting(false)
    }
  }

  // Handle form reset
  const handleReset = useCallback(() => {
    setFormData({
      title: '',
      description: '',
      due_date: '',
      priority: 'Medium'
    })
    setValidationErrors({})
    setSubmitAttempted(false)
    actions.clearError()
    
    if (titleInputRef.current) {
      titleInputRef.current.focus()
    }
  }, [actions])

  // Handle cancel
  const handleCancel = useCallback(() => {
    handleReset()
    if (onCancel) {
      onCancel()
    }
  }, [handleReset, onCancel])

  // Character count helpers
  const titleCharCount = formData.title.length
  const descCharCount = formData.description.length

  return (
    <div className={styles.todoForm}>
      <h2 className={styles.formTitle}>Add New Todo</h2>
      
      {state.error && (
        <div className={styles.errorBanner} role="alert">
          <span className={styles.errorIcon}>⚠️</span>
          {state.error}
        </div>
      )}

      <form onSubmit={handleSubmit} className={styles.form} noValidate>
        {/* Title Field */}
        <div className={styles.formGroup}>
          <label htmlFor="title" className={styles.label}>
            Title *
          </label>
          <input
            ref={titleInputRef}
            type="text"
            id="title"
            name="title"
            value={formData.title}
            onChange={handleInputChange}
            className={`${styles.input} ${validationErrors.title ? styles.inputError : ''}`}
            placeholder="Enter todo title..."
            maxLength={100}
            aria-describedby={validationErrors.title ? 'title-error' : 'title-help'}
            aria-invalid={!!validationErrors.title}
            required
          />
          <div className={styles.fieldHelp}>
            <span className={styles.charCount}>
              {titleCharCount}/100
            </span>
            {validationErrors.title && (
              <span id="title-error" className={styles.errorText} role="alert">
                {validationErrors.title}
              </span>
            )}
          </div>
        </div>

        {/* Description Field */}
        <div className={styles.formGroup}>
          <label htmlFor="description" className={styles.label}>
            Description
          </label>
          <textarea
            id="description"
            name="description"
            value={formData.description}
            onChange={handleInputChange}
            className={`${styles.textarea} ${validationErrors.description ? styles.inputError : ''}`}
            placeholder="Enter optional description..."
            maxLength={500}
            rows={3}
            aria-describedby={validationErrors.description ? 'description-error' : 'description-help'}
            aria-invalid={!!validationErrors.description}
          />
          <div className={styles.fieldHelp}>
            <span className={styles.charCount}>
              {descCharCount}/500
            </span>
            {validationErrors.description && (
              <span id="description-error" className={styles.errorText} role="alert">
                {validationErrors.description}
              </span>
            )}
          </div>
        </div>

        {/* Due Date Field */}
        <div className={styles.formGroup}>
          <label htmlFor="due_date" className={styles.label}>
            Due Date
          </label>
          <input
            type="date"
            id="due_date"
            name="due_date"
            value={formData.due_date}
            onChange={handleInputChange}
            className={`${styles.input} ${validationErrors.due_date ? styles.inputError : ''}`}
            min={getTodayString()}
            aria-describedby={validationErrors.due_date ? 'due-date-error' : 'due-date-help'}
            aria-invalid={!!validationErrors.due_date}
          />
          <div className={styles.fieldHelp}>
            <span id="due-date-help" className={styles.helpText}>
              Optional - leave blank for no due date
            </span>
            {validationErrors.due_date && (
              <span id="due-date-error" className={styles.errorText} role="alert">
                {validationErrors.due_date}
              </span>
            )}
          </div>
        </div>

        {/* Priority Field */}
        <div className={styles.formGroup}>
          <label htmlFor="priority" className={styles.label}>
            Priority
          </label>
          <select
            id="priority"
            name="priority"
            value={formData.priority}
            onChange={handleInputChange}
            className={`${styles.select} ${validationErrors.priority ? styles.inputError : ''}`}
            aria-describedby={validationErrors.priority ? 'priority-error' : undefined}
            aria-invalid={!!validationErrors.priority}
          >
            <option value="Low">Low</option>
            <option value="Medium">Medium</option>
            <option value="High">High</option>
          </select>
          {validationErrors.priority && (
            <span id="priority-error" className={styles.errorText} role="alert">
              {validationErrors.priority}
            </span>
          )}
        </div>

        {/* Form Actions */}
        <div className={styles.formActions}>
          <button
            type="button"
            onClick={handleCancel}
            className={styles.cancelButton}
            disabled={isSubmitting}
          >
            Cancel
          </button>
          <button
            type="submit"
            className={styles.submitButton}
            disabled={isSubmitting || state.loading}
          >
            {isSubmitting || state.loading ? (
              <>
                <span className={styles.spinner} aria-hidden="true"></span>
                Creating...
              </>
            ) : (
              'Create Todo'
            )}
          </button>
        </div>
      </form>
    </div>
  )
}

export default TodoForm