# Todo Application Architecture

## System Overview
A todo application with separated backend and frontend components communicating via REST API.

## Directory Structure

```
backend/
├── app.py              # Flask application entry point
├── routes.py           # API route definitions
├── models.py           # Data models and storage
└── requirements.txt    # Python dependencies

frontend/
├── public/             # Static assets
├── src/
│   ├── components/     # React components
│   │   ├── TodoList.js
│   │   ├── TodoItem.js
│   │   └── TodoForm.js
│   ├── services/       # API communication
│   │   └── api.js
│   ├── App.js          # Main application component
│   └── index.js        # Application entry point
├── package.json        # Node dependencies
└── README.md           # Frontend documentation
```

## Backend Architecture (Flask)

### Core Components
- **app.py**: Flask application initialization, CORS setup
- **routes.py**: REST API endpoints for todo operations
- **models.py**: Todo data model and in-memory storage

### API Design
- RESTful endpoints following standard conventions
- JSON request/response format
- CORS enabled for frontend communication

## Frontend Architecture (React)

### Component Structure
- **TodoList**: Main container displaying all todos
- **TodoItem**: Individual todo display and actions
- **TodoForm**: New todo creation form

### State Management
- React hooks for local state
- API service layer for backend communication

## Data Flow
1. Frontend components make API calls via services layer
2. Backend processes requests and updates in-memory storage
3. Backend returns JSON responses
4. Frontend updates UI based on responses

## Error Handling Strategy

### Backend Error Handling
- JSON error responses with consistent format
- HTTP status codes following REST conventions
- Input validation for all API endpoints
- Error logging for debugging

### Frontend Error Handling
- API error response handling in service layer
- User-friendly error messages
- Loading states for async operations

## Testing Strategy

### Backend Testing
- pytest for unit and integration tests
- Test API endpoints individually
- Mock data storage for testing

### Frontend Testing
- Jest and React Testing Library
- Component unit tests
- API integration tests

## Environment Configuration

### Development Environment
- Flask development server (port 5000)
- React development server (port 3000)
- CORS enabled for cross-origin requests
- Debug mode enabled

### Configuration Management
- Environment variables for sensitive data
- Separate configs for development/production

## Development Workflow
- Backend runs on port 5000
- Frontend runs on port 3000
- CORS configured for cross-origin requests
- Testing before each commit