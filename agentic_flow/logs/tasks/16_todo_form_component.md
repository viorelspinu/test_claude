# Task 16: TodoForm Component
**Task ID**: 16  
**Name**: todo_form_component  
**Assigned**: Developer  
**Status**: In Progress  

## Objective
Create TodoForm component only

## Description  
Create the TodoForm component that provides an interface for creating new todos. This component will handle form input, validation, and submission with proper error handling and user feedback.

## Deliverable
`frontend/src/components/TodoForm.js`

## Dependencies
- Task 15 ✅ (TodoItem component complete)

## Technical Requirements
1. **Component Structure**
   - Functional React component with form handling
   - Controlled form input with useState
   - Form submission with validation

2. **Props Interface**
   - `onAddTodo` - Callback function for todo creation
   - `loading` - Optional loading state from parent (optional)
   - Clean, minimal props interface

3. **Form Features**
   - Text input for todo content
   - Submit button for form submission
   - Enter key submission support
   - Input validation (non-empty, trimmed)
   - Clear input after successful submission

4. **State Management**
   - `inputValue` - Current form input value
   - `isSubmitting` - Local loading state for submission
   - `error` - Error message for failed submissions

5. **User Experience**
   - Placeholder text for guidance
   - Disabled state during submission
   - Clear error feedback
   - Focus management after submission

## Implementation Scope
- **In Scope**: Form component, input handling, validation, submission
- **Out of Scope**: Direct API calls (handled by parent via props)

## Component Behavior
1. **Input**: User types todo text
2. **Validation**: Check for non-empty, trimmed text
3. **Submit**: Trigger onAddTodo callback with text
4. **Success**: Clear input, reset form state
5. **Error**: Display error message, keep input value

## Integration with Parent
- Parent (likely App or TodoList) passes onAddTodo callback
- Parent handles API calls and state management
- TodoForm handles form state and user interaction
- Clean separation of concerns

## Test Criteria
- TodoForm component handles input
- Form validation works properly
- Submit functionality triggers callbacks
- Loading and error states work
- Enter key submission works

## Success Metrics
- ✅ TodoForm.js created in components directory
- ✅ Form input and validation implemented
- ✅ Submit handling with callbacks
- ✅ Loading and error states
- ✅ Ready for parent component integration