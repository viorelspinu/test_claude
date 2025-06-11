# Task 003: Implement GET todos API endpoint

## Objective
Create a REST API endpoint to retrieve all todos from the database.

## Requirements
- Endpoint: `GET /api/todos`
- Return all todos as JSON array
- Include all todo fields (id, text, completed, created_at)
- Handle empty database gracefully
- Return appropriate HTTP status codes
- Follow REST API conventions

## Acceptance Criteria
1. ✅ Endpoint responds at `/api/todos`
2. ✅ Returns JSON array of todos
3. ✅ Empty array when no todos exist
4. ✅ All todo fields included in response
5. ✅ HTTP 200 status for successful requests
6. ✅ Proper error handling

## Implementation Plan
1. Add route handler for `GET /api/todos`
2. Query all todos from database using Todo.query.all()
3. Convert todos to dict format using to_dict() method
4. Return JSON response

## Expected Files Modified
- `/backend/app.py` - Add GET todos route

## Testing Strategy
- Start Flask app
- Make GET request to `/api/todos`
- Verify JSON response structure
- Test with empty and populated database

## Definition of Done
- Endpoint returns proper JSON response
- Manual testing shows expected behavior
- Ready for frontend integration