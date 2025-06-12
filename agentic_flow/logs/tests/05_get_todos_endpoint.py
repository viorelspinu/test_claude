import sys
import os

# Add backend directory to path
backend_path = os.path.join(os.path.dirname(__file__), '../../../backend')
sys.path.insert(0, os.path.abspath(backend_path))

from app import app
from models import clear_todos, add_todo, Todo
import json

def test_get_todos_status():
    """Test GET /api/todos returns 200 status"""
    with app.test_client() as client:
        response = client.get('/api/todos')
        assert response.status_code == 200

def test_response_is_json():
    """Test response is valid JSON"""
    with app.test_client() as client:
        response = client.get('/api/todos')
        assert response.content_type == 'application/json'
        data = response.get_json()
        assert isinstance(data, list)

def test_empty_storage():
    """Test empty storage returns empty list"""
    clear_todos()
    with app.test_client() as client:
        response = client.get('/api/todos')
        data = response.get_json()
        assert data == []
        assert len(data) == 0

def test_multiple_todos():
    """Test multiple todos returns all todos"""
    clear_todos()
    
    # Add test todos
    todo1 = Todo("First todo")
    todo2 = Todo("Second todo", completed=True)
    todo3 = Todo("Third todo")
    
    add_todo(todo1)
    add_todo(todo2)
    add_todo(todo3)
    
    with app.test_client() as client:
        response = client.get('/api/todos')
        data = response.get_json()
        
        assert len(data) == 3
        assert response.status_code == 200
        
        # Check all todos are returned
        todo_texts = [todo['text'] for todo in data]
        assert "First todo" in todo_texts
        assert "Second todo" in todo_texts
        assert "Third todo" in todo_texts

def test_json_structure():
    """Test JSON structure matches Todo.to_dict()"""
    clear_todos()
    
    todo = Todo("Structure test", completed=True)
    add_todo(todo)
    
    with app.test_client() as client:
        response = client.get('/api/todos')
        data = response.get_json()
        
        assert len(data) == 1
        todo_json = data[0]
        
        # Check required fields
        assert 'id' in todo_json
        assert 'text' in todo_json
        assert 'completed' in todo_json
        assert 'created_at' in todo_json
        
        # Check values
        assert todo_json['text'] == "Structure test"
        assert todo_json['completed'] == True
        assert isinstance(todo_json['id'], str)
        assert isinstance(todo_json['created_at'], str)

def test_cors_headers():
    """Test CORS headers are present"""
    with app.test_client() as client:
        response = client.get('/api/todos')
        headers = dict(response.headers)
        assert 'Access-Control-Allow-Origin' in headers

if __name__ == '__main__':
    test_get_todos_status()
    test_response_is_json()
    test_empty_storage()
    test_multiple_todos()
    test_json_structure()
    test_cors_headers()
    print("All GET todos endpoint tests passed!")