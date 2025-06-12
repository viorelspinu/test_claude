# Prompt 13: Developer - API Service Implementation  
**Timestamp**: 2025-01-23 (estimated)  
**Role**: Developer  
**Action**: Implement Task 13 - API service layer  

## Task Context
- **Objective**: Create API service layer for backend communication
- **Deliverable**: frontend/src/services/api.js with HTTP methods
- **Dependencies**: Task 12 ✅ (React app initialized)

## Implementation Plan
1. Create services directory structure
2. Implement base API configuration
3. Create CRUD operation functions
4. Add comprehensive error handling
5. Include JSDoc documentation

## Technical Specifications
- Use native fetch() API (no additional dependencies)  
- Base URL: http://localhost:5000
- Content-Type: application/json headers
- Async/await pattern for all functions
- Proper error handling and response parsing

## Backend API Reference
From completed backend tasks:
- GET /api/todos - Returns array of todos
- POST /api/todos - Creates new todo (requires {text})
- PUT /api/todos/{id} - Updates todo (requires {text, completed})  
- DELETE /api/todos/{id} - Deletes todo

## Expected Functions
- getTodos()
- createTodo(text)
- updateTodo(id, updates)
- deleteTodo(id)

## Implementation Approach
Frontend-first development with backend integration in mind.