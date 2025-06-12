# Task 05: GET Todos Endpoint

## Objective
Implement GET /api/todos endpoint only

## Deliverable
GET route in `backend/routes.py`

## Dependencies
Task 04 (storage_functions) - COMPLETED

## Success Criteria
GET /api/todos returns JSON list

## Implementation Details
- Create `backend/routes.py` file
- Import Flask Blueprint for route organization
- Import storage functions from models
- Implement GET /api/todos route that:
  - Calls get_all_todos() from storage
  - Converts todos to JSON format using to_dict()
  - Returns JSON response with todos list
- Register blueprint with Flask app

## Testing Requirements
- Verify GET /api/todos returns 200 status
- Confirm response is valid JSON
- Test with empty storage (returns empty list)
- Test with multiple todos (returns all todos)
- Verify JSON structure matches Todo.to_dict()