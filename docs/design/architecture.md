# Todo App Architecture

## System Overview

Full-stack todo application with Flask backend and React frontend, designed for local development and testing.

## Backend Architecture (Flask)

### Structure
```
/src/backend/
├── app.py              # Flask application entry point
├── models.py           # Todo data model
├── routes.py           # API route handlers
├── database.py         # Database connection and setup
└── requirements.txt    # Python dependencies
```

### Technology Stack
- Flask: Web framework
- SQLAlchemy: Database ORM
- SQLite: Database (file-based)
- Flask-CORS: Cross-origin resource sharing

### Database Schema
```sql
todos (
    id INTEGER PRIMARY KEY,
    title TEXT NOT NULL,
    description TEXT,
    completed BOOLEAN DEFAULT FALSE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
)
```

## Frontend Architecture (React)

### Structure
```
/src/frontend/
├── public/
│   └── index.html
├── src/
│   ├── components/
│   │   ├── TodoList.js
│   │   ├── TodoItem.js
│   │   ├── TodoForm.js
│   │   └── TodoFilter.js
│   ├── services/
│   │   └── api.js
│   ├── App.js
│   └── index.js
├── package.json
└── package-lock.json
```

### Technology Stack
- React: UI library
- Axios: HTTP client for API calls
- CSS Modules: Component styling
- Create React App: Build tooling

## API Design

### Endpoints
- GET /api/todos - List todos (with optional status filter)
- POST /api/todos - Create todo
- PUT /api/todos/{id} - Update todo
- DELETE /api/todos/{id} - Delete todo

### Response Format
```json
{
    "success": true,
    "data": [...],
    "message": "Operation completed"
}
```

## Development Workflow

1. Backend first: API endpoints with hardcoded data
2. Database integration: SQLite with SQLAlchemy
3. Frontend setup: React app with basic components
4. API integration: Connect frontend to backend
5. Polish: Error handling, validation, styling

## Deployment Strategy

Local development only:
- Backend: `python app.py` (Flask dev server)
- Frontend: `npm start` (React dev server)
- Database: SQLite file in project directory