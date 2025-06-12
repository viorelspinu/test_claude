# Task 13: API Service Layer
**Task ID**: 13  
**Name**: api_service  
**Assigned**: Developer  
**Status**: In Progress  

## Objective
Create API service layer for backend communication

## Description  
Create a complete API service layer in the frontend that provides methods to communicate with the Flask backend. This service will abstract HTTP requests and provide a clean interface for components to interact with todo data.

## Deliverable
`frontend/src/services/api.js` with HTTP methods for all CRUD operations

## Dependencies
- Task 12 ✅ (React app initialized)

## Technical Requirements
1. **Base Configuration**
   - Configure base URL for backend API (http://localhost:5000)
   - Set up proper HTTP headers (Content-Type: application/json)
   - Handle CORS properly

2. **CRUD Operations**
   - `getTodos()` - GET /api/todos
   - `createTodo(text)` - POST /api/todos  
   - `updateTodo(id, completed)` - PUT /api/todos/{id}
   - `deleteTodo(id)` - DELETE /api/todos/{id}

3. **Error Handling**
   - Catch and handle HTTP errors
   - Return proper error responses
   - Handle network failures gracefully

4. **Data Format**
   - Parse JSON responses properly
   - Format request data correctly
   - Handle empty responses

## Test Criteria
- API service exports HTTP functions
- All CRUD functions defined and callable
- Proper error handling implemented
- Correct request/response format

## Implementation Notes
- Use native fetch() API (no additional dependencies)
- Follow existing React project structure
- Ensure functions are async/await compatible
- Include JSDoc documentation for functions

## Success Metrics
- ✅ api.js file created with all required functions
- ✅ Functions properly formatted for backend API
- ✅ Error handling implemented
- ✅ Ready for component integration