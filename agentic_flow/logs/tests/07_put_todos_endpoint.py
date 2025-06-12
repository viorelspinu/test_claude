import sys
import os

# Add backend directory to path
backend_path = os.path.join(os.path.dirname(__file__), '../../../backend')
sys.path.insert(0, os.path.abspath(backend_path))

from app import app
from models import clear_todos, add_todo, Todo, get_todo_by_id
import json

def test_put_valid_updates():
    """Test PUT /api/todos/{id} returns 200 status for valid updates"""
    clear_todos()
    
    todo = Todo("Original text")
    add_todo(todo)
    todo_id = todo.id
    
    with app.test_client() as client:
        response = client.put(f'/api/todos/{todo_id}',
                             json={'text': 'Updated text'},
                             content_type='application/json')
        
        assert response.status_code == 200
        data = response.get_json()
        assert data['text'] == 'Updated text'
        assert 'id' in data
        assert 'completed' in data

def test_update_text_only():
    """Test updating text field only"""
    clear_todos()
    
    todo = Todo("Original text", completed=True)
    add_todo(todo)
    todo_id = todo.id
    
    with app.test_client() as client:
        response = client.put(f'/api/todos/{todo_id}',
                             json={'text': 'New text only'},
                             content_type='application/json')
        
        assert response.status_code == 200
        data = response.get_json()
        assert data['text'] == 'New text only'
        assert data['completed'] == True  # Should remain unchanged

def test_update_completed_only():
    """Test updating completed field only"""
    clear_todos()
    
    todo = Todo("Keep this text")
    add_todo(todo)
    todo_id = todo.id
    
    with app.test_client() as client:
        response = client.put(f'/api/todos/{todo_id}',
                             json={'completed': True},
                             content_type='application/json')
        
        assert response.status_code == 200
        data = response.get_json()
        assert data['completed'] == True
        assert data['text'] == 'Keep this text'  # Should remain unchanged

def test_update_both_fields():
    """Test updating both fields"""
    clear_todos()
    
    todo = Todo("Original text")
    add_todo(todo)
    todo_id = todo.id
    
    with app.test_client() as client:
        response = client.put(f'/api/todos/{todo_id}',
                             json={'text': 'Both updated', 'completed': True},
                             content_type='application/json')
        
        assert response.status_code == 200
        data = response.get_json()
        assert data['text'] == 'Both updated'
        assert data['completed'] == True

def test_nonexistent_todo_404():
    """Test 404 error for non-existent todo ID"""
    with app.test_client() as client:
        response = client.put('/api/todos/nonexistent-id',
                             json={'text': 'Updated'},
                             content_type='application/json')
        
        assert response.status_code == 404
        data = response.get_json()
        assert 'error' in data
        assert 'Todo not found' in data['error']

def test_empty_text_400():
    """Test 400 error for empty text field"""
    clear_todos()
    
    todo = Todo("Original text")
    add_todo(todo)
    todo_id = todo.id
    
    with app.test_client() as client:
        # Empty string
        response = client.put(f'/api/todos/{todo_id}',
                             json={'text': ''},
                             content_type='application/json')
        
        assert response.status_code == 400
        data = response.get_json()
        assert 'error' in data
        assert 'Text field cannot be empty' in data['error']
        
        # Whitespace only
        response = client.put(f'/api/todos/{todo_id}',
                             json={'text': '   '},
                             content_type='application/json')
        
        assert response.status_code == 400

def test_updated_todo_in_response():
    """Test updated todo is returned in response"""
    clear_todos()
    
    todo = Todo("Original text")
    add_todo(todo)
    todo_id = todo.id
    
    with app.test_client() as client:
        response = client.put(f'/api/todos/{todo_id}',
                             json={'text': 'Response test', 'completed': True},
                             content_type='application/json')
        
        data = response.get_json()
        assert data['id'] == todo_id
        assert data['text'] == 'Response test'
        assert data['completed'] == True
        assert 'created_at' in data

def test_todo_actually_updated_in_storage():
    """Test todo is actually updated in storage"""
    clear_todos()
    
    todo = Todo("Storage test")
    add_todo(todo)
    todo_id = todo.id
    
    with app.test_client() as client:
        # Update todo
        response = client.put(f'/api/todos/{todo_id}',
                             json={'text': 'Storage updated', 'completed': True},
                             content_type='application/json')
        
        assert response.status_code == 200
        
        # Verify in storage directly
        stored_todo = get_todo_by_id(todo_id)
        assert stored_todo is not None
        assert stored_todo.text == 'Storage updated'
        assert stored_todo.completed == True
        
        # Verify via GET endpoint
        get_response = client.get('/api/todos')
        todos = get_response.get_json()
        found_todo = next((t for t in todos if t['id'] == todo_id), None)
        assert found_todo is not None
        assert found_todo['text'] == 'Storage updated'
        assert found_todo['completed'] == True

if __name__ == '__main__':
    test_put_valid_updates()
    test_update_text_only()
    test_update_completed_only()
    test_update_both_fields()
    test_nonexistent_todo_404()
    test_empty_text_400()
    test_updated_todo_in_response()
    test_todo_actually_updated_in_storage()
    print("All PUT todos endpoint tests passed!")