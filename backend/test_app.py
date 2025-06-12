import pytest
import sys
import os

# Add current directory to path for imports
sys.path.insert(0, os.path.dirname(__file__))

from app import app
from models import clear_todos, add_todo, Todo

@pytest.fixture
def client():
    """Create a test client for the Flask application."""
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client

@pytest.fixture(autouse=True)
def setup_teardown():
    """Setup and teardown for each test."""
    # Setup: clear todos before each test
    clear_todos()
    yield
    # Teardown: clear todos after each test
    clear_todos()

class TestHealthEndpoint:
    """Test the health check endpoint."""
    
    def test_health_check(self, client):
        """Test health endpoint returns correct response."""
        response = client.get('/health')
        assert response.status_code == 200
        data = response.get_json()
        assert data == {'status': 'healthy'}

class TestTodosAPI:
    """Test the todos API endpoints."""
    
    def test_get_empty_todos(self, client):
        """Test GET /api/todos returns empty list initially."""
        response = client.get('/api/todos')
        assert response.status_code == 200
        data = response.get_json()
        assert data == []
    
    def test_create_todo(self, client):
        """Test POST /api/todos creates a new todo."""
        todo_data = {'text': 'Test todo'}
        response = client.post('/api/todos', json=todo_data)
        assert response.status_code == 201
        data = response.get_json()
        assert data['text'] == 'Test todo'
        assert data['completed'] == False
        assert 'id' in data
        assert 'created_at' in data
    
    def test_create_todo_validation(self, client):
        """Test POST /api/todos validates required fields."""
        response = client.post('/api/todos', json={})
        assert response.status_code == 400
        data = response.get_json()
        assert 'error' in data
    
    def test_get_todos_after_creation(self, client):
        """Test GET /api/todos returns created todos."""
        # Create a todo
        todo_data = {'text': 'Test todo'}
        create_response = client.post('/api/todos', json=todo_data)
        assert create_response.status_code == 201
        
        # Get todos
        get_response = client.get('/api/todos')
        assert get_response.status_code == 200
        todos = get_response.get_json()
        assert len(todos) == 1
        assert todos[0]['text'] == 'Test todo'

class TestErrorHandling:
    """Test error handling functionality."""
    
    def test_404_error(self, client):
        """Test 404 error returns proper JSON."""
        response = client.get('/nonexistent')
        assert response.status_code == 404
        data = response.get_json()
        assert 'error' in data
        assert 'message' in data
        assert data['error'] == 'Not Found'
    
    def test_405_error(self, client):
        """Test 405 error returns proper JSON."""
        response = client.post('/health')
        assert response.status_code == 405
        data = response.get_json()
        assert 'error' in data
        assert 'message' in data
        assert data['error'] == 'Method Not Allowed'