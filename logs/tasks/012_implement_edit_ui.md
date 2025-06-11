# Task 012: Implement Edit UI in TodoItem

## Objective
Add inline editing functionality to TodoItem component with input field and save/cancel controls.

## Implementation Details
- Add isEditing state to TodoItem
- Add editText state for input value
- Replace todo text span with input when editing
- Add save/cancel buttons or keyboard shortcuts
- Handle Enter to save, Escape to cancel
- Add onEdit prop for parent communication

## Acceptance Criteria
- Click on todo text enters edit mode
- Input field shows current text
- Enter key saves changes
- Escape key cancels changes
- Visual feedback during save operation
- Validation for empty text and length limits

## Files to Modify
- frontend/src/components/TodoItem.js