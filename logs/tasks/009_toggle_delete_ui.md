# Task 009: Add todo toggle and delete functionality

## Objective
Implement UI controls to toggle todo completion status and delete todos, integrating with PUT/DELETE endpoints.

## Requirements
- Add checkbox/button to toggle completed status
- Add delete button for each todo item
- Visual indication of completed todos
- Confirmation for delete action (optional)
- Update local state after operations
- Handle loading states during API calls
- Show errors if operations fail

## Acceptance Criteria
1. ✅ Click to toggle todo between completed/incomplete
2. ✅ Visual difference for completed todos
3. ✅ Delete button removes todo from list
4. ✅ API calls to PUT /api/todos/<id>
5. ✅ API calls to DELETE /api/todos/<id>
6. ✅ Optimistic UI updates or loading states
7. ✅ Error handling for failed operations

## UI Design
- Checkbox or toggle button for completion
- Delete button (trash icon or "Delete" text)
- Completed todos: strikethrough text, muted colors
- Hover states for interactive elements
- Loading feedback during operations

## Implementation Plan
1. Update TodoItem component with action buttons
2. Add click handlers for toggle and delete
3. Implement API calls using existing todoApi functions
4. Update parent state after successful operations
5. Add visual styling for completed state
6. Implement error handling
7. Test all interactions

## Component Updates
- `TodoItem.js` - Add buttons and handlers
- `App.js` - Add update/delete state handlers
- `todoApi.js` - Ensure PUT/DELETE functions work
- `App.css` - Styling for interactive elements

## API Integration
- PUT /api/todos/<id> with {completed: !current}
- DELETE /api/todos/<id>
- Update local state on success
- Show error on failure

## Testing Strategy
- Toggle todo completion status
- Delete todo and verify removal
- Test error scenarios (network failure)
- Verify visual feedback
- Check multiple rapid clicks

## Definition of Done
- Users can mark todos as complete/incomplete
- Users can delete unwanted todos
- Visual feedback for all states
- Smooth user experience
- Error handling implemented