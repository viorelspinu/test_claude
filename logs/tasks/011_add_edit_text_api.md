# Task 011: Add Edit Text API Function

## Objective
Add updateTodoText function to todoApi.js for updating todo text via existing PUT endpoint.

## Implementation Details
- Add function that calls PUT /api/todos/<id> with text field
- Return updated todo object
- Handle errors appropriately
- Follow existing API patterns in the file

## Acceptance Criteria
- Function accepts todoId and newText parameters
- Makes PUT request to correct endpoint
- Returns promise with updated todo data
- Handles network errors consistently with other API functions

## Files to Modify
- frontend/src/api/todoApi.js