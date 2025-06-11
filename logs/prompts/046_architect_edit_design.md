# 046 - Architect: Edit Task Names Design

## Architecture Decision
The backend already supports text updates via PUT /api/todos/<id> endpoint. Focus on frontend implementation.

## Implementation Plan
1. Add edit state and UI to TodoItem component
2. Add updateTodoText function to todoApi.js
3. Add onEdit prop handling in parent components
4. Implement inline editing with input field
5. Add save/cancel buttons and keyboard shortcuts

## Task Breakdown
### Task 011: Add Edit Text API Function
- Add updateTodoText function to frontend/src/api/todoApi.js
- Handle text-only updates to existing PUT endpoint

### Task 012: Implement Edit UI in TodoItem
- Add edit state management
- Add inline input field for editing
- Add save/cancel controls
- Handle keyboard shortcuts (Enter to save, Escape to cancel)

### Task 013: Wire Edit Functionality
- Add onEdit prop to TodoItem
- Update TodoList to pass edit handler
- Update App.js to handle text updates

## Next Task Selection
Starting with Task 011 - Add Edit Text API Function as it's the foundation for the feature.