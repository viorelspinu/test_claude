import sys
import os

# Add backend directory to path
backend_path = os.path.join(os.path.dirname(__file__), '../../../backend')
sys.path.insert(0, os.path.abspath(backend_path))

from app import app
from models import clear_todos
import json

def test_post_todos_valid_data():
    """Test POST /api/todos returns 201 status for valid data"""
    clear_todos()
    
    with app.test_client() as client:
        response = client.post('/api/todos',
                             json={'text': 'Valid test todo'},
                             content_type='application/json')
        
        assert response.status_code == 201
        data = response.get_json()
        assert data is not None
        assert 'id' in data
        assert data['text'] == 'Valid test todo'
        assert data['completed'] == False

def test_created_todo_in_response():
    """Test created todo is returned in response"""
    clear_todos()
    
    with app.test_client() as client:
        response = client.post('/api/todos',
                             json={'text': 'Response test todo'},
                             content_type='application/json')
        
        data = response.get_json()
        assert data['text'] == 'Response test todo'
        assert data['completed'] == False
        assert 'id' in data
        assert 'created_at' in data
        assert len(data['id']) == 36  # UUID length

def test_missing_text_field():
    """Test validation for missing 'text' field (400 error)"""
    with app.test_client() as client:
        # Test with no JSON data
        response = client.post('/api/todos',
                             json={},
                             content_type='application/json')
        
        assert response.status_code == 400
        data = response.get_json()
        assert 'error' in data
        assert 'Missing required field: text' in data['error']
        
        # Test with no JSON at all
        response = client.post('/api/todos',
                             content_type='application/json')
        assert response.status_code == 400

def test_empty_text_field():
    """Test validation for empty 'text' field (400 error)"""
    with app.test_client() as client:
        # Empty string
        response = client.post('/api/todos',
                             json={'text': ''},
                             content_type='application/json')
        
        assert response.status_code == 400
        data = response.get_json()
        assert 'error' in data
        assert 'Text field cannot be empty' in data['error']
        
        # Whitespace only
        response = client.post('/api/todos',
                             json={'text': '   '},
                             content_type='application/json')
        
        assert response.status_code == 400
        data = response.get_json()
        assert 'error' in data

def test_todo_actually_stored():
    """Test todo is actually stored (can be retrieved via GET)"""
    clear_todos()
    
    with app.test_client() as client:
        # Create todo
        post_response = client.post('/api/todos',
                                  json={'text': 'Storage test todo'},
                                  content_type='application/json')
        
        assert post_response.status_code == 201
        created_todo = post_response.get_json()
        
        # Retrieve todos
        get_response = client.get('/api/todos')
        assert get_response.status_code == 200
        
        todos = get_response.get_json()
        assert len(todos) == 1
        assert todos[0]['id'] == created_todo['id']
        assert todos[0]['text'] == 'Storage test todo'

def test_multiple_todos_creation():
    """Test creating multiple todos"""
    clear_todos()
    
    with app.test_client() as client:
        # Create first todo
        response1 = client.post('/api/todos',
                              json={'text': 'First todo'},
                              content_type='application/json')
        assert response1.status_code == 201
        
        # Create second todo
        response2 = client.post('/api/todos',
                              json={'text': 'Second todo'},
                              content_type='application/json')
        assert response2.status_code == 201
        
        # Verify both stored
        get_response = client.get('/api/todos')
        todos = get_response.get_json()
        assert len(todos) == 2

if __name__ == '__main__':
    test_post_todos_valid_data()
    test_created_todo_in_response()
    test_missing_text_field()
    test_empty_text_field()
    test_todo_actually_stored()
    test_multiple_todos_creation()
    print("All POST todos endpoint tests passed!")