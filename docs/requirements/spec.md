# Todo App Requirements Specification

## Overview
A simple todo application with Flask REST API backend and React frontend.

## Core Features
1. **Todo Management**
   - Create new todos with text description
   - Mark todos as complete/incomplete
   - Delete todos
   - View all todos

2. **User Interface**
   - Clean, responsive web interface
   - Add new todo input field
   - Todo list with checkboxes
   - Delete buttons for each todo

## Technical Requirements
- **Backend**: Flask with REST API endpoints
- **Frontend**: React with modern hooks
- **Data Storage**: Simple JSON file or SQLite for persistence
- **Communication**: HTTP REST API between frontend and backend

## API Endpoints
- `GET /api/todos` - List all todos
- `POST /api/todos` - Create new todo
- `PUT /api/todos/{id}` - Update todo (toggle completion)
- `DELETE /api/todos/{id}` - Delete todo

## Data Model
```
Todo {
  id: integer (auto-increment)
  text: string (required)
  completed: boolean (default: false)
  created_at: timestamp
}
```

## Success Criteria
- User can add, complete, and delete todos
- Changes persist between sessions
- Frontend communicates successfully with backend
- Application runs locally for development