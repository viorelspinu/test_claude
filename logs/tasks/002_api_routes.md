# 002 · Create Todo API Routes

## Task Details
- **ID:** 002
- **Title:** Create Todo API Routes
- **Priority:** High
- **Effort:** Small
- **Dependencies:** 001 (completed)

## Description
Implement basic API endpoints for todo CRUD operations with hardcoded responses. This validates the API structure before database integration.

## Acceptance Criteria
- GET /api/todos - Returns list of sample todos
- POST /api/todos - Accepts todo data, returns success response
- PUT /api/todos/{id} - Accepts todo updates, returns success response  
- DELETE /api/todos/{id} - Returns success response
- All endpoints return proper JSON responses
- Endpoints testable via curl/Postman
- Proper HTTP status codes (200, 201, 404, etc.)

## File Structure to Modify
```
/backend/
├── app.py (add routes)
├── routes.py (create - route handlers)
└── requirements.txt (existing)
```

## Sample Data for Testing
```json
[
  {"id": 1, "title": "Learn Flask", "description": "Build todo API", "completed": false},
  {"id": 2, "title": "Setup React", "description": "Create frontend", "completed": false}
]
```

## Visible Effect
- API endpoints respond with JSON data
- CRUD operations return appropriate responses
- API structure ready for database integration
- Frontend can consume API endpoints