# Task: Create TodoForm Component for Adding New Todos

## Task Information
- **Task ID**: task-016-todo-form-component
- **Title**: Create TodoForm component for adding new todos
- **Type**: frontend
- **Estimated Hours**: 2
- **Priority**: high

## Dependencies
- **Previous Task**: task-015-todo-item-component (TodoItem component with toggle and actions)
- **Required Components**: TodoItem component must be completed and functional

## Description
Build form component for creating new todos with validation and submission. This component will serve as the primary interface for users to add new todo items to their list.

## Acceptance Criteria

1. **Form Fields**
   - Form with all required fields: title, description, due_date, priority
   - All fields properly labeled and accessible
   - Form layout is clean and user-friendly

2. **Client-side Validation**
   - Client-side validation before submission
   - Required field validation (title is mandatory)
   - Date validation (due_date cannot be in the past)
   - Character limits enforced (title max 100 chars, description max 500 chars)
   - Real-time validation feedback

3. **Form Submission**
   - Form submission handling with API integration
   - Proper HTTP request to create new todo
   - Integration with global Todo context state

4. **User Feedback**
   - Success and error feedback
   - Loading state during submission
   - Clear error messages for failed submissions

5. **Form Management**
   - Form reset after successful submission
   - Cancel functionality to clear form
   - Proper input focus management

## Deliverables

### Primary Files
- `/frontend/src/components/todo/TodoForm.jsx` - Main form component
- Form validation logic integrated within component
- CSS styling for form layout and states

### Component Structure
```jsx
// Expected component interface
<TodoForm onSubmit={handleSubmit} onCancel={handleCancel} />
```

## Technical Requirements

### Form Fields Specification
- **title**: Text input, required, max 100 characters
- **description**: Textarea, optional, max 500 characters  
- **due_date**: Date input, optional, cannot be past date
- **priority**: Select dropdown with options: low, medium, high (default: medium)

### Validation Rules
- Title is required and must be non-empty after trimming
- Due date, if provided, must be today or future date
- Character limits enforced with visual feedback
- Form cannot be submitted with validation errors

### API Integration
- Use existing todoService for API calls
- Handle network errors gracefully
- Update global context state after successful creation
- Proper error handling for duplicate titles or server errors

## Test Requirements

### Functional Testing
- Form validation works correctly for all fields
- Form submission creates new todo successfully
- Error handling works for invalid input
- Form resets after successful submission
- Cancel functionality clears all fields

### User Experience Testing
- Form is accessible via keyboard navigation
- Visual feedback for validation states
- Loading states provide clear user feedback
- Error messages are helpful and specific

## Implementation Notes

### State Management
- Use React hooks for local form state
- Integrate with global TodoContext for todo creation
- Manage validation state separately from form data

### Error Handling
- Display validation errors inline with form fields
- Show server errors in a prominent but non-intrusive way
- Provide clear recovery paths for all error scenarios

### Performance Considerations
- Debounce validation for better user experience
- Optimize re-renders during typing
- Efficient form reset implementation

## Constraints

- Component must work with existing TodoContext state management
- Must follow established component structure and naming conventions
- Form styling should be consistent with existing application design
- No external form libraries (use native React form handling)

## Success Metrics
- Users can successfully create new todos through the form
- Form validation prevents invalid data submission
- Error states are clear and actionable
- Form provides immediate feedback for user actions
- Component integrates seamlessly with existing todo list display