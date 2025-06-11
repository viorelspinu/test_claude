# Todo App Architecture

## System Overview
A full-stack todo application with Flask REST API backend and React frontend.

## Architecture
- **Backend**: Flask web framework with SQLAlchemy ORM
- **Frontend**: React SPA with modern hooks
- **Database**: SQLite for data persistence
- **Communication**: RESTful API with JSON

## Project Structure
```
/
├── backend/
│   ├── app.py              # Flask application entry point
│   ├── models.py           # Todo data model
│   ├── requirements.txt    # Python dependencies
│   └── instance/
│       └── todos.db        # SQLite database
├── frontend/
│   ├── src/
│   │   ├── components/     # React components
│   │   ├── services/       # API service layer
│   │   └── App.js          # Main app component
│   ├── package.json        # Node dependencies
│   └── public/             # Static assets
└── docs/                   # Documentation
```

## API Design
- GET /api/todos - Retrieve all todos
- POST /api/todos - Create new todo
- PUT /api/todos/{id} - Update todo
- DELETE /api/todos/{id} - Delete todo

## Development Workflow
1. Flask development server on port 5000
2. React development server on port 3000
3. CORS enabled for cross-origin requests