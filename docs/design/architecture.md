# Todo App Architecture

## System Overview
A full-stack todo application with clear separation between backend API and frontend UI.

## Architecture Components

### Backend (Flask)
- **Location**: `/backend/`
- **Framework**: Flask with Flask-CORS for cross-origin requests
- **Database**: SQLite with simple file-based storage
- **Structure**:
  - `app.py` - Main Flask application
  - `models.py` - Todo data model
  - `database.py` - Database initialization and operations
  - `todos.db` - SQLite database file

### Frontend (React)
- **Location**: `/frontend/` (already exists)
- **Framework**: React with hooks (useState, useEffect)
- **HTTP Client**: Fetch API for backend communication
- **Structure**:
  - `src/App.js` - Main application component
  - `src/components/TodoList.js` - Todo list display
  - `src/components/TodoItem.js` - Individual todo item
  - `src/components/AddTodo.js` - Add new todo form

## API Design
- Base URL: `http://localhost:5000/api`
- Content-Type: `application/json`
- CORS enabled for frontend communication

## Development Setup
- Backend runs on port 5000
- Frontend runs on port 3000 (default React dev server)
- Both can run simultaneously for development

## Data Flow
1. User interacts with React frontend
2. Frontend makes HTTP requests to Flask API
3. Flask processes requests, updates SQLite database
4. Flask returns JSON responses
5. Frontend updates UI based on responses