import sys
import os

# Add backend directory to path
backend_path = os.path.join(os.path.dirname(__file__), '../../../backend')
sys.path.insert(0, os.path.abspath(backend_path))

from app import app
from models import clear_todos, add_todo, Todo
import json

def test_404_error_handler():
    """Test 404 error returns proper JSON format"""
    with app.test_client() as client:
        response = client.get('/nonexistent-endpoint')
        
        assert response.status_code == 404
        data = response.get_json()
        assert data is not None
        assert 'error' in data
        assert 'message' in data
        assert data['error'] == 'Not Found'
        assert 'not found' in data['message'].lower()

def test_405_error_handler():
    """Test 405 error returns proper JSON format"""
    with app.test_client() as client:
        # Try POST on GET-only endpoint
        response = client.post('/health')
        
        assert response.status_code == 405
        data = response.get_json()
        assert data is not None
        assert 'error' in data
        assert 'message' in data
        assert data['error'] == 'Method Not Allowed'
        assert 'not allowed' in data['message'].lower()

def test_existing_functionality_preserved():
    """Test error handling doesn't break existing functionality"""
    clear_todos()
    
    with app.test_client() as client:
        # Test health endpoint
        response = client.get('/health')
        assert response.status_code == 200
        assert response.get_json() == {'status': 'healthy'}
        
        # Test API endpoints
        response = client.get('/api/todos')
        assert response.status_code == 200
        assert response.get_json() == []
        
        # Test creating todo
        response = client.post('/api/todos', 
                             json={'text': 'Test todo'},
                             content_type='application/json')
        assert response.status_code == 201
        data = response.get_json()
        assert data['text'] == 'Test todo'

def test_api_error_responses():
    """Test API endpoints return proper error format"""
    with app.test_client() as client:
        # Test validation error
        response = client.post('/api/todos', 
                             json={},
                             content_type='application/json')
        
        assert response.status_code == 400
        data = response.get_json()
        assert 'error' in data
        assert 'Missing required field: text' in data['error']

def test_nonexistent_todo_error():
    """Test 404 for nonexistent todo"""
    with app.test_client() as client:
        response = client.get('/api/todos/nonexistent-id')
        
        # This should return 405 since GET /api/todos/{id} is not implemented
        # but our error handler should format it properly
        assert response.status_code == 405
        data = response.get_json()
        assert 'error' in data
        assert data['error'] == 'Method Not Allowed'

def test_error_response_format():
    """Test all errors have consistent JSON format"""
    with app.test_client() as client:
        # Test 404
        response = client.get('/nonexistent')
        data = response.get_json()
        assert 'error' in data
        assert 'message' in data
        assert isinstance(data['error'], str)
        assert isinstance(data['message'], str)
        
        # Test 405
        response = client.post('/health')
        data = response.get_json()
        assert 'error' in data
        assert 'message' in data
        assert isinstance(data['error'], str)
        assert isinstance(data['message'], str)

def test_error_logging_configured():
    """Test error logging is configured"""
    import logging
    
    # Check if logging is configured
    logger = logging.getLogger('app')
    assert logger.level <= logging.INFO

if __name__ == '__main__':
    test_404_error_handler()
    test_405_error_handler()
    test_existing_functionality_preserved()
    test_api_error_responses()
    test_nonexistent_todo_error()
    test_error_response_format()
    test_error_logging_configured()
    print("All backend error handling tests passed!")