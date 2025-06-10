# Development Workflow Guide

This guide provides detailed instructions for working with the Todo List full-stack application, including setup, development practices, and common tasks.

## Table of Contents

1. [Getting Started](#getting-started)
2. [Development Environment](#development-environment)
3. [Working with the Codebase](#working-with-the-codebase)
4. [Testing](#testing)
5. [Common Tasks](#common-tasks)
6. [Troubleshooting](#troubleshooting)
7. [Best Practices](#best-practices)

## Getting Started

### Prerequisites

- **Node.js** (v16 or higher)
- **Python** (3.8 or higher)
- **npm** (v8 or higher)
- **Git** (for version control)

### Initial Setup

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd todo-fullstack-app
   ```

2. **Run the setup script**
   ```bash
   npm run setup
   ```
   This will:
   - Install all dependencies (frontend and backend)
   - Create Python virtual environment
   - Initialize the database

3. **Start the development environment**
   ```bash
   npm run dev
   ```
   Or use the platform-specific scripts:
   - Unix/macOS: `./start-dev.sh`
   - Windows: `start-dev.bat`
   - Cross-platform: `node start-dev.js`

## Development Environment

### Starting Services

#### All Services (Recommended)
```bash
npm run dev
```
This starts both frontend and backend with proper logging and error handling.

#### Individual Services
```bash
# Backend only
npm run dev:backend

# Frontend only
npm run dev:frontend

# Check service status
npm run dev:check
```

### Environment Configuration

#### Frontend (.env)
Create a `.env` file in the `frontend/` directory:
```env
# Copy from .env.example
REACT_APP_USE_PROXY=true
PORT=3000
BROWSER=none
```

#### Backend (.env)
Create a `.env` file in the `backend/` directory:
```env
# Copy from .env.example
FLASK_ENV=development
FLASK_DEBUG=1
PORT=5001
```

### Service URLs

- **Frontend**: http://localhost:3000
- **Backend API**: http://localhost:5001/api
- **API Health Check**: http://localhost:5001/api/health

## Working with the Codebase

### Project Structure

```
todo-fullstack-app/
├── frontend/               # React application
│   ├── src/
│   │   ├── components/    # React components
│   │   ├── services/      # API client and services
│   │   ├── hooks/         # Custom React hooks
│   │   └── tests/         # Frontend tests
│   └── package.json       # Frontend dependencies
├── backend/               # Flask application
│   ├── app/
│   │   ├── api/          # API routes
│   │   ├── models.py     # Database models
│   │   └── extensions.py # Flask extensions
│   ├── tests/            # Backend tests
│   └── requirements.txt  # Backend dependencies
├── docs/                 # Documentation
└── package.json         # Root package for scripts
```

### Making Changes

#### Frontend Development

1. **Components**: Located in `frontend/src/components/`
   ```jsx
   // Example: Creating a new component
   // frontend/src/components/MyComponent/MyComponent.js
   import React from 'react';
   import './MyComponent.css';
   
   function MyComponent({ prop1, prop2 }) {
     return <div className="my-component">...</div>;
   }
   
   export default MyComponent;
   ```

2. **API Integration**: Use the API client in `frontend/src/services/api.js`
   ```javascript
   import { apiClient } from '../services/api';
   
   // Example usage
   const tasks = await apiClient.get('/tasks');
   const newTask = await apiClient.post('/tasks', { title: 'New Task' });
   ```

3. **State Management**: Use React hooks for state
   ```javascript
   // See frontend/src/hooks/useTasks.js for example
   ```

#### Backend Development

1. **API Routes**: Located in `backend/app/api/routes.py`
   ```python
   @api_bp.route('/tasks', methods=['POST'])
   def create_task():
       # Implementation
   ```

2. **Database Models**: Located in `backend/app/models.py`
   ```python
   class Task(db.Model):
       # Model definition
   ```

3. **Database Migrations**:
   ```bash
   cd backend
   flask db migrate -m "Description of changes"
   flask db upgrade
   ```

## Testing

### Running Tests

#### All Tests
```bash
npm run test:all
```

#### Frontend Tests
```bash
npm run test:frontend

# Specific test types
cd frontend
npm run test:integration  # Integration tests
npm run test:e2e         # End-to-end tests
```

#### Backend Tests
```bash
npm run test:backend

# With coverage
cd backend
pytest --cov=app tests/
```

### Writing Tests

#### Frontend Test Example
```javascript
// frontend/src/components/Task/__tests__/TaskItem.test.js
import { render, screen } from '@testing-library/react';
import TaskItem from '../TaskItem';

test('renders task title', () => {
  const task = { id: 1, title: 'Test Task', completed: false };
  render(<TaskItem task={task} />);
  expect(screen.getByText('Test Task')).toBeInTheDocument();
});
```

#### Backend Test Example
```python
# backend/tests/test_api.py
def test_create_task(client):
    response = client.post('/api/tasks', json={
        'title': 'Test Task',
        'priority': 'Medium'
    })
    assert response.status_code == 201
    assert response.json['task']['title'] == 'Test Task'
```

### Integration Testing

Run the full-stack integration test:
```bash
./test-fullstack.sh
```

## Common Tasks

### Database Operations

```bash
# Initialize database
npm run db:init

# Reset database (drops and recreates)
npm run db:reset

# Seed with sample data
npm run db:seed

# View database statistics
npm run db:stats
```

### Code Quality

```bash
# Frontend linting
npm run lint

# Frontend formatting
npm run format

# Backend linting
npm run lint:backend

# Backend formatting
npm run format:backend
```

### Building for Production

```bash
# Build frontend
npm run build

# Start production servers
npm run start:prod
```

### Docker Operations

```bash
# Build containers
npm run docker:build

# Start services
npm run docker:up

# Stop services
npm run docker:down
```

## Troubleshooting

### Common Issues

#### Port Already in Use
```bash
# Check what's using the port
lsof -i :5001  # Backend
lsof -i :3000  # Frontend

# Stop all services
npm run dev:check
./start-dev.sh --stop
```

#### Database Issues
```bash
# Reset database
npm run db:reset

# Check database file
ls -la backend/instance/
```

#### Dependency Issues
```bash
# Clean install
rm -rf node_modules frontend/node_modules backend/venv
npm run setup
```

#### CORS Errors
1. Check backend CORS configuration in `backend/config.py`
2. Ensure frontend proxy is configured in `frontend/package.json`
3. Verify API_BASE_URL in `frontend/src/services/api.js`

### Logs

- **Backend logs**: `backend/logs/backend.log`
- **Frontend logs**: `frontend/logs/frontend.log`
- **View logs**: `npm run logs:backend`

## Best Practices

### Git Workflow

1. **Branch naming**: `feature/description`, `bugfix/description`
2. **Commit messages**: Use conventional commits
   ```
   feat: add user authentication
   fix: resolve task deletion issue
   docs: update API documentation
   ```

3. **Pull Request Process**:
   - Create feature branch
   - Make changes with tests
   - Run all tests locally
   - Submit PR with description

### Code Style

#### JavaScript/React
- Use functional components with hooks
- Follow ESLint configuration
- Use meaningful component and variable names
- Add PropTypes or TypeScript for type checking

#### Python/Flask
- Follow PEP 8 style guide
- Use type hints where appropriate
- Write docstrings for functions and classes
- Keep routes thin, logic in services

### API Design

- Use RESTful conventions
- Return consistent response formats
- Include proper error messages
- Version APIs when making breaking changes

### Security

- Never commit `.env` files
- Use environment variables for secrets
- Validate all user inputs
- Implement proper authentication (when added)
- Keep dependencies updated

### Performance

- Implement pagination for lists
- Use database indexes appropriately
- Minimize API calls in frontend
- Cache responses when appropriate

## Additional Resources

- [Flask Documentation](https://flask.palletsprojects.com/)
- [React Documentation](https://reactjs.org/docs)
- [SQLAlchemy Documentation](https://www.sqlalchemy.org/)
- [Jest Testing Documentation](https://jestjs.io/docs/getting-started)
- [Pytest Documentation](https://docs.pytest.org/)

## Getting Help

1. Check the troubleshooting section
2. Review existing issues in the repository
3. Ask in the development chat/forum
4. Create a detailed issue with:
   - Steps to reproduce
   - Expected behavior
   - Actual behavior
   - Environment details