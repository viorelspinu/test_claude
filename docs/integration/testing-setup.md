# Testing Infrastructure Setup

This document provides comprehensive setup instructions for testing infrastructure across both backend and frontend components, following the contracts defined in the parallel development synchronization guide.

## Backend Testing Setup

### 1. Test Environment Configuration

#### Dependencies
Add to `requirements.txt`:
```
pytest==7.4.3
pytest-flask==1.3.0
pytest-cov==4.1.0
factory-boy==3.3.0
faker==20.1.0
```

#### Test Configuration (`/backend/tests/conftest.py`)
```python
import pytest
import tempfile
import os
from app import create_app
from app.extensions import db
from app.models import Task

@pytest.fixture
def app():
    """Create application for the tests."""
    db_fd, db_path = tempfile.mkstemp()
    
    app = create_app({
        'TESTING': True,
        'SQLALCHEMY_DATABASE_URI': f'sqlite:///{db_path}',
        'WTF_CSRF_ENABLED': False
    })
    
    with app.app_context():
        db.create_all()
        yield app
        db.drop_all()
    
    os.close(db_fd)
    os.unlink(db_path)

@pytest.fixture
def client(app):
    """A test client for the app."""
    return app.test_client()

@pytest.fixture
def runner(app):
    """A test runner for the app's Click commands."""
    return app.test_cli_runner()

@pytest.fixture
def sample_task_data():
    """Sample task data for testing."""
    return {
        'title': 'Test Task',
        'description': 'This is a test task',
        'priority': 'High'
    }

@pytest.fixture
def task_factory():
    """Factory for creating test tasks."""
    def _create_task(**kwargs):
        defaults = {
            'title': 'Test Task',
            'description': 'Test Description',
            'priority': 'Medium',
            'completed': False
        }
        defaults.update(kwargs)
        return Task(**defaults)
    return _create_task
```

### 2. API Contract Test Suite

#### Task Model Tests (`/backend/tests/test_models.py`)
```python
import pytest
from datetime import datetime
from app.models import Task

class TestTaskModel:
    def test_task_creation(self, app, task_factory):
        """Test task creation with valid data."""
        with app.app_context():
            task = task_factory(title="New Task")
            assert task.title == "New Task"
            assert task.priority == "Medium"  # Default value
            assert task.completed is False
            assert task.created_at is not None
    
    def test_task_validation_title_required(self, app):
        """Test that title is required."""
        with app.app_context():
            with pytest.raises(ValueError):
                Task(title="", description="Test")
    
    def test_task_validation_priority_enum(self, app):
        """Test priority must be valid enum value."""
        with app.app_context():
            with pytest.raises(ValueError):
                Task(title="Test", priority="Invalid")
    
    def test_task_to_dict_serialization(self, app, task_factory):
        """Test task serialization to dictionary."""
        with app.app_context():
            task = task_factory()
            task_dict = task.to_dict()
            
            required_fields = ['id', 'title', 'description', 'priority', 
                             'completed', 'created_at', 'updated_at', 'completed_at']
            
            for field in required_fields:
                assert field in task_dict
    
    def test_task_completion_timestamp(self, app, task_factory):
        """Test completed_at timestamp is set when task is completed."""
        with app.app_context():
            task = task_factory()
            assert task.completed_at is None
            
            task.completed = True
            task.save()  # Assuming save method updates completed_at
            assert task.completed_at is not None
```

#### API Endpoint Tests (`/backend/tests/test_api.py`)
```python
import pytest
import json
from app.models import Task

class TestTaskAPI:
    
    def test_get_tasks_empty_list(self, client):
        """Test GET /api/tasks returns empty list initially."""
        response = client.get('/api/tasks')
        
        assert response.status_code == 200
        assert response.content_type == 'application/json'
        
        data = json.loads(response.data)
        assert 'data' in data
        assert 'tasks' in data['data']
        assert data['data']['tasks'] == []
        assert data['data']['total'] == 0
    
    def test_create_task_valid_data(self, client, sample_task_data):
        """Test POST /api/tasks with valid data."""
        response = client.post('/api/tasks', 
                             json=sample_task_data,
                             content_type='application/json')
        
        assert response.status_code == 201
        
        data = json.loads(response.data)
        assert 'data' in data
        task = data['data']
        
        assert task['title'] == sample_task_data['title']
        assert task['description'] == sample_task_data['description']
        assert task['priority'] == sample_task_data['priority']
        assert task['completed'] is False
        assert 'id' in task
        assert 'created_at' in task
    
    def test_create_task_invalid_data(self, client):
        """Test POST /api/tasks with invalid data returns 400."""
        invalid_data = {'title': '', 'priority': 'Invalid'}
        
        response = client.post('/api/tasks',
                             json=invalid_data,
                             content_type='application/json')
        
        assert response.status_code == 400
        
        data = json.loads(response.data)
        assert 'error' in data
        assert data['error']['code'] == 'VALIDATION_ERROR'
        assert 'details' in data['error']
    
    def test_update_task_partial(self, client, app):
        """Test PUT /api/tasks/{id} with partial update."""
        # First create a task
        with app.app_context():
            task = Task(title="Original Title", priority="Low")
            task.save()
            task_id = task.id
        
        update_data = {'title': 'Updated Title'}
        response = client.put(f'/api/tasks/{task_id}',
                            json=update_data,
                            content_type='application/json')
        
        assert response.status_code == 200
        
        data = json.loads(response.data)
        updated_task = data['data']
        
        assert updated_task['title'] == 'Updated Title'
        assert updated_task['priority'] == 'Low'  # Unchanged
    
    def test_delete_task(self, client, app):
        """Test DELETE /api/tasks/{id}."""
        # First create a task
        with app.app_context():
            task = Task(title="To Delete", priority="Medium")
            task.save()
            task_id = task.id
        
        response = client.delete(f'/api/tasks/{task_id}')
        assert response.status_code == 204
        
        # Verify task is deleted
        get_response = client.get(f'/api/tasks/{task_id}')
        assert get_response.status_code == 404
    
    def test_cors_headers(self, client):
        """Test CORS headers are present."""
        response = client.get('/api/tasks')
        
        assert 'Access-Control-Allow-Origin' in response.headers
        assert response.headers['Access-Control-Allow-Origin'] == 'http://localhost:3000'
        
    def test_error_response_format(self, client):
        """Test error responses follow the standard format."""
        response = client.get('/api/tasks/99999')  # Non-existent task
        
        assert response.status_code == 404
        
        data = json.loads(response.data)
        assert 'error' in data
        assert 'code' in data['error']
        assert 'message' in data['error']
```

## Frontend Testing Setup

### 1. Test Environment Configuration

#### Dependencies
Add to `package.json`:
```json
{
  "devDependencies": {
    "@testing-library/react": "^13.4.0",
    "@testing-library/jest-dom": "^5.16.5",
    "@testing-library/user-event": "^14.4.3",
    "axios-mock-adapter": "^1.21.2",
    "jest-environment-jsdom": "^29.3.1"
  }
}
```

#### Test Configuration (`/frontend/src/setupTests.js`)
```javascript
import '@testing-library/jest-dom';
import { server } from './mocks/server';

// Establish API mocking before all tests
beforeAll(() => server.listen());

// Reset any request handlers that we may add during the tests
afterEach(() => server.resetHandlers());

// Clean up after the tests are finished
afterAll(() => server.close());
```

### 2. Mock API Setup

#### Mock Server Configuration (`/frontend/src/mocks/handlers.js`)
```javascript
import { rest } from 'msw';

const API_BASE_URL = 'http://localhost:5001/api';

export const handlers = [
  // GET /api/tasks
  rest.get(`${API_BASE_URL}/tasks`, (req, res, ctx) => {
    const completed = req.url.searchParams.get('completed');
    const priority = req.url.searchParams.get('priority');
    
    let tasks = mockTasks;
    
    if (completed !== null) {
      tasks = tasks.filter(task => 
        task.completed === (completed === 'true')
      );
    }
    
    if (priority) {
      tasks = tasks.filter(task => task.priority === priority);
    }
    
    return res(
      ctx.status(200),
      ctx.json({
        data: {
          tasks: tasks,
          total: tasks.length,
          filtered: tasks.length
        }
      })
    );
  }),

  // POST /api/tasks
  rest.post(`${API_BASE_URL}/tasks`, (req, res, ctx) => {
    const { title, description, priority = 'Medium' } = req.body;
    
    if (!title || title.trim().length === 0) {
      return res(
        ctx.status(400),
        ctx.json({
          error: {
            code: 'VALIDATION_ERROR',
            message: 'Title is required',
            details: {
              title: 'Title cannot be empty'
            }
          }
        })
      );
    }
    
    const newTask = {
      id: Date.now(),
      title: title.trim(),
      description: description || null,
      priority,
      completed: false,
      created_at: new Date().toISOString(),
      updated_at: new Date().toISOString(),
      completed_at: null
    };
    
    mockTasks.push(newTask);
    
    return res(
      ctx.status(201),
      ctx.json({ data: newTask })
    );
  }),

  // PUT /api/tasks/:id
  rest.put(`${API_BASE_URL}/tasks/:id`, (req, res, ctx) => {
    const taskId = parseInt(req.params.id);
    const updateData = req.body;
    
    const taskIndex = mockTasks.findIndex(task => task.id === taskId);
    
    if (taskIndex === -1) {
      return res(
        ctx.status(404),
        ctx.json({
          error: {
            code: 'NOT_FOUND',
            message: 'Task not found'
          }
        })
      );
    }
    
    const updatedTask = {
      ...mockTasks[taskIndex],
      ...updateData,
      updated_at: new Date().toISOString(),
      completed_at: updateData.completed && !mockTasks[taskIndex].completed 
        ? new Date().toISOString() 
        : mockTasks[taskIndex].completed_at
    };
    
    mockTasks[taskIndex] = updatedTask;
    
    return res(
      ctx.status(200),
      ctx.json({ data: updatedTask })
    );
  }),

  // DELETE /api/tasks/:id
  rest.delete(`${API_BASE_URL}/tasks/:id`, (req, res, ctx) => {
    const taskId = parseInt(req.params.id);
    const taskIndex = mockTasks.findIndex(task => task.id === taskId);
    
    if (taskIndex === -1) {
      return res(
        ctx.status(404),
        ctx.json({
          error: {
            code: 'NOT_FOUND',
            message: 'Task not found'
          }
        })
      );
    }
    
    mockTasks.splice(taskIndex, 1);
    
    return res(ctx.status(204));
  }),

  // GET /api/tasks/stats
  rest.get(`${API_BASE_URL}/tasks/stats`, (req, res, ctx) => {
    const completed = mockTasks.filter(task => task.completed).length;
    const incomplete = mockTasks.length - completed;
    
    const byPriority = mockTasks.reduce((acc, task) => {
      acc[task.priority] = (acc[task.priority] || 0) + 1;
      return acc;
    }, { High: 0, Medium: 0, Low: 0 });
    
    return res(
      ctx.status(200),
      ctx.json({
        data: {
          total: mockTasks.length,
          completed,
          incomplete,
          by_priority: byPriority
        }
      })
    );
  })
];

// Mock data
const mockTasks = [
  {
    id: 1,
    title: 'Sample Task 1',
    description: 'This is a sample task for testing',
    priority: 'High',
    completed: false,
    created_at: '2023-12-01T10:00:00Z',
    updated_at: '2023-12-01T10:00:00Z',
    completed_at: null
  },
  {
    id: 2,
    title: 'Completed Task',
    description: 'This task is already completed',
    priority: 'Medium',
    completed: true,
    created_at: '2023-12-01T09:00:00Z',
    updated_at: '2023-12-01T11:00:00Z',
    completed_at: '2023-12-01T11:00:00Z'
  }
];
```

#### Mock Server Setup (`/frontend/src/mocks/server.js`)
```javascript
import { setupServer } from 'msw/node';
import { handlers } from './handlers';

// Setup requests interception with the given handlers
export const server = setupServer(...handlers);
```

### 3. Component Integration Tests

#### API Service Tests (`/frontend/src/services/__tests__/taskService.test.js`)
```javascript
import { 
  getTasks, 
  createTask, 
  updateTask, 
  deleteTask,
  getTaskStats 
} from '../taskService';

describe('Task Service API Integration', () => {
  
  test('getTasks returns tasks with correct format', async () => {
    const result = await getTasks();
    
    expect(result.data).toHaveProperty('tasks');
    expect(result.data).toHaveProperty('total');
    expect(result.data).toHaveProperty('filtered');
    expect(Array.isArray(result.data.tasks)).toBe(true);
    
    if (result.data.tasks.length > 0) {
      const task = result.data.tasks[0];
      expect(task).toHaveProperty('id');
      expect(task).toHaveProperty('title');
      expect(task).toHaveProperty('priority');
      expect(task).toHaveProperty('completed');
      expect(task).toHaveProperty('created_at');
    }
  });
  
  test('createTask with valid data returns created task', async () => {
    const taskData = {
      title: 'New Test Task',
      description: 'Test description',
      priority: 'High'
    };
    
    const result = await createTask(taskData);
    
    expect(result.data).toHaveProperty('id');
    expect(result.data.title).toBe(taskData.title);
    expect(result.data.description).toBe(taskData.description);
    expect(result.data.priority).toBe(taskData.priority);
    expect(result.data.completed).toBe(false);
  });
  
  test('createTask with invalid data throws validation error', async () => {
    const invalidData = { title: '', priority: 'High' };
    
    await expect(createTask(invalidData)).rejects.toMatchObject({
      response: {
        status: 400,
        data: {
          error: {
            code: 'VALIDATION_ERROR'
          }
        }
      }
    });
  });
  
  test('updateTask modifies existing task', async () => {
    const updateData = { title: 'Updated Title' };
    
    const result = await updateTask(1, updateData);
    
    expect(result.data.title).toBe('Updated Title');
    expect(result.data.id).toBe(1);
  });
  
  test('deleteTask removes task successfully', async () => {
    await expect(deleteTask(1)).resolves.not.toThrow();
  });
  
  test('getTaskStats returns correct statistics format', async () => {
    const result = await getTaskStats();
    
    expect(result.data).toHaveProperty('total');
    expect(result.data).toHaveProperty('completed');
    expect(result.data).toHaveProperty('incomplete');
    expect(result.data).toHaveProperty('by_priority');
    
    expect(result.data.by_priority).toHaveProperty('High');
    expect(result.data.by_priority).toHaveProperty('Medium');
    expect(result.data.by_priority).toHaveProperty('Low');
  });
});
```

### 4. Running Tests

#### Backend Test Commands
```bash
# Install test dependencies
pip install -r requirements.txt

# Run all tests
pytest

# Run with coverage
pytest --cov=app --cov-report=html

# Run specific test file
pytest tests/test_api.py

# Run with verbose output
pytest -v
```

#### Frontend Test Commands
```bash
# Install test dependencies
npm install

# Run all tests
npm test

# Run tests in watch mode
npm test -- --watch

# Run tests with coverage
npm test -- --coverage

# Run specific test file
npm test -- TaskService.test.js
```

## Test Data Management

### Backend Test Data
- Use factories for consistent test data creation
- Isolated test database for each test run
- Automatic cleanup after each test

### Frontend Mock Data
- Consistent with backend data model
- Realistic test scenarios
- Stateful mocks that persist changes during test runs

## Continuous Integration

### Test Pipeline Requirements
1. Both backend and frontend tests must pass
2. Code coverage thresholds: 80% minimum
3. API contract validation tests are mandatory
4. Integration tests run against real API endpoints
5. Performance tests for API response times

This testing infrastructure ensures reliable integration between backend and frontend components while maintaining the contracts defined in the parallel development guide.