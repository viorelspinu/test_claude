# Todo App Architecture

## System Overview
Full-stack todo application with clear separation of concerns.

## Directory Structure
```
/backend/          # Flask API server
  /app/           # Main application
  /models/        # Data models
  /routes/        # API endpoints
  requirements.txt
  run.py

/frontend/         # React application
  /src/           # React source
  /public/        # Static assets
  package.json

/database/         # SQLite database file
```

## API Design
- `GET /api/todos` - List all todos
- `POST /api/todos` - Create new todo
- `PUT /api/todos/<id>` - Update todo
- `DELETE /api/todos/<id>` - Delete todo

## Data Model
```
Todo:
- id (primary key)
- text (string)
- completed (boolean)
- created_at (timestamp)
```

## Technology Choices
- Flask with Flask-SQLAlchemy for ORM
- SQLite for simplicity
- React with modern hooks
- Axios for HTTP requests
- Basic CSS for styling