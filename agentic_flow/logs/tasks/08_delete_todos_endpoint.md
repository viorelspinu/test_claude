# Task 08: DELETE Todos Endpoint

## Objective
Implement DELETE /api/todos/{id} endpoint only

## Deliverable
DELETE route in `backend/routes.py`

## Dependencies
Task 07 (put_todos_endpoint) - COMPLETED

## Success Criteria
DELETE /api/todos/{id} removes todo

## Implementation Details
- Add DELETE route to existing `backend/routes.py`
- Import delete_todo from models (already imported)
- Implement DELETE /api/todos/<todo_id> route that:
  - Accepts todo_id as URL parameter
  - Validates todo exists (404 if not found)
  - Deletes todo using delete_todo() function
  - Returns deleted todo as JSON with 200 status
- Handle not found errors with 404 status

## Testing Requirements
- Verify DELETE /api/todos/{id} returns 200 status for valid deletion
- Test 404 error for non-existent todo ID
- Verify deleted todo is returned in response
- Verify todo is actually removed from storage
- Test that deleted todo cannot be retrieved afterward