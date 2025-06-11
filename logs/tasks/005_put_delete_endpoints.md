# Task 005: Implement PUT/DELETE todos API endpoints

## Objective
Create REST API endpoints to update and delete todos, completing backend CRUD operations.

## Requirements
- Endpoint: `PUT /api/todos/<id>` - Update todo
- Endpoint: `DELETE /api/todos/<id>` - Delete todo
- Update supports toggling completed status
- Update supports editing todo text
- Handle non-existent todo IDs
- Appropriate HTTP status codes
- Maintain data integrity

## Acceptance Criteria
1. ✅ PUT endpoint updates todo fields
2. ✅ DELETE endpoint removes todo from database
3. ✅ HTTP 404 for non-existent IDs
4. ✅ HTTP 200 for successful operations
5. ✅ Validation for PUT request data
6. ✅ Database changes persist

## PUT Endpoint Specification
- URL: `/api/todos/<id>`
- Method: `PUT`
- Body: JSON with optional fields:
  - `text`: Updated todo text (max 200 chars)
  - `completed`: Boolean completion status
- Returns: Updated todo object
- Status codes:
  - 200: Success
  - 400: Invalid data
  - 404: Todo not found

## DELETE Endpoint Specification  
- URL: `/api/todos/<id>`
- Method: `DELETE`
- Body: None
- Returns: Success message
- Status codes:
  - 200: Success
  - 404: Todo not found

## Implementation Plan
1. Add PUT route handler with ID parameter
2. Validate and parse request data
3. Find todo by ID, return 404 if missing
4. Update specified fields only
5. Add DELETE route handler
6. Find and remove todo, handle missing IDs
7. Test both endpoints thoroughly

## Testing Strategy
- Update todo text
- Toggle completed status
- Update both fields
- Try updating non-existent ID
- Delete existing todo
- Try deleting non-existent ID
- Verify database state changes

## Definition of Done
- Both endpoints functional
- Proper error handling
- Database operations successful
- Ready for frontend integration
- All status codes correct