# Todo App Requirements Specification

## Overview
A basic todo application with Flask backend and React frontend.

## Functional Requirements

### Backend (Flask)
- **Todo Model**: id, text, completed, created_at
- **API Endpoints**:
  - GET /api/todos - List all todos
  - POST /api/todos - Create new todo
  - PUT /api/todos/{id} - Update todo
  - DELETE /api/todos/{id} - Delete todo
- **Data Storage**: SQLite database
- **CORS**: Enable cross-origin requests from React

### Frontend (React)
- **Components**:
  - TodoList - Display todos
  - TodoItem - Individual todo with toggle/delete
  - AddTodo - Form to create new todos
- **Features**:
  - View all todos
  - Add new todo
  - Toggle todo completion
  - Delete todo
  - Basic error handling

## Technical Stack
- Backend: Flask, SQLAlchemy, Flask-CORS
- Frontend: React (hooks), Axios for API calls
- Database: SQLite
- Development: Separate dev servers for Flask and React

## Success Criteria
- User can manage todos through web interface
- Data persists between sessions
- Clean separation between backend and frontend