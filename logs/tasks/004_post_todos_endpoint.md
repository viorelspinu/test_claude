# Task 004: Implement POST todos API endpoint

## Objective
Create a REST API endpoint to add new todos to the database.

## Requirements
- Endpoint: `POST /api/todos`
- Accept JSON payload with todo text
- Create new todo in database
- Return created todo as JSON response
- Validate input data
- Handle errors appropriately
- Follow REST API conventions

## Acceptance Criteria
1. ✅ Endpoint responds at `POST /api/todos`
2. ✅ Accepts JSON: `{"text": "todo content"}`
3. ✅ Returns created todo with generated ID and timestamp
4. ✅ HTTP 201 status for successful creation
5. ✅ HTTP 400 for invalid/missing data
6. ✅ Proper error handling and validation

## Implementation Plan
1. Add route handler for `POST /api/todos`
2. Parse JSON request data
3. Validate required `text` field
4. Create new Todo instance
5. Save to database
6. Return created todo as JSON with HTTP 201

## Expected Files Modified
- `/backend/app.py` - Add POST todos route

## Validation Rules
- `text` field is required
- `text` must be non-empty string
- `text` length within model constraints (200 chars)

## Testing Strategy
- Test valid POST request with proper JSON
- Test missing `text` field
- Test empty `text` value
- Test oversized `text` value
- Verify database persistence
- Verify response format matches GET endpoint

## Definition of Done
- Endpoint creates todos successfully
- Proper validation and error responses
- Database persistence confirmed
- JSON response format consistent with GET endpoint