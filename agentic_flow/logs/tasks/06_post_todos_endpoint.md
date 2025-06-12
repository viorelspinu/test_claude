# Task 06: POST Todos Endpoint

## Objective
Implement POST /api/todos endpoint only

## Deliverable
POST route in `backend/routes.py`

## Dependencies
Task 05 (get_todos_endpoint) - COMPLETED

## Success Criteria
POST /api/todos creates new todo

## Implementation Details
- Add POST route to existing `backend/routes.py`
- Import request from Flask for JSON data
- Implement POST /api/todos route that:
  - Accepts JSON payload with 'text' field
  - Validates required 'text' field exists
  - Creates new Todo instance
  - Adds todo to storage using add_todo()
  - Returns created todo as JSON with 201 status
- Handle validation errors with 400 status

## Testing Requirements
- Verify POST /api/todos returns 201 status for valid data
- Confirm created todo is returned in response
- Test validation for missing 'text' field (400 error)
- Test validation for empty 'text' field (400 error)
- Verify todo is actually stored (can be retrieved via GET)