import sys
import os

# Add backend directory to path
backend_path = os.path.join(os.path.dirname(__file__), '../../../backend')
sys.path.insert(0, os.path.abspath(backend_path))

from app import app
from models import clear_todos, add_todo, Todo, get_todo_by_id
import json

def test_delete_valid_todo():
    """Test DELETE /api/todos/{id} returns 200 status for valid deletion"""
    clear_todos()
    
    todo = Todo("Todo to delete")
    add_todo(todo)
    todo_id = todo.id
    
    with app.test_client() as client:
        response = client.delete(f'/api/todos/{todo_id}')
        
        assert response.status_code == 200
        data = response.get_json()
        assert data is not None
        assert data['id'] == todo_id
        assert data['text'] == 'Todo to delete'

def test_nonexistent_todo_404():
    """Test 404 error for non-existent todo ID"""
    with app.test_client() as client:
        response = client.delete('/api/todos/nonexistent-id')
        
        assert response.status_code == 404
        data = response.get_json()
        assert 'error' in data
        assert 'Todo not found' in data['error']

def test_deleted_todo_in_response():
    """Test deleted todo is returned in response"""
    clear_todos()
    
    todo = Todo("Response test todo", completed=True)
    add_todo(todo)
    todo_id = todo.id
    
    with app.test_client() as client:
        response = client.delete(f'/api/todos/{todo_id}')
        
        data = response.get_json()
        assert data['id'] == todo_id
        assert data['text'] == 'Response test todo'
        assert data['completed'] == True
        assert 'created_at' in data

def test_todo_removed_from_storage():
    """Test todo is actually removed from storage"""
    clear_todos()
    
    # Create multiple todos
    todo1 = Todo("Keep this one")
    todo2 = Todo("Delete this one") 
    todo3 = Todo("Keep this too")
    
    add_todo(todo1)
    add_todo(todo2)
    add_todo(todo3)
    
    todo_to_delete_id = todo2.id
    
    with app.test_client() as client:
        # Verify initial count
        get_response = client.get('/api/todos')
        todos = get_response.get_json()
        assert len(todos) == 3
        
        # Delete todo
        delete_response = client.delete(f'/api/todos/{todo_to_delete_id}')
        assert delete_response.status_code == 200
        
        # Verify count after deletion
        get_response = client.get('/api/todos')
        todos = get_response.get_json()
        assert len(todos) == 2
        
        # Verify specific todo is gone
        todo_ids = [todo['id'] for todo in todos]
        assert todo_to_delete_id not in todo_ids
        assert todo1.id in todo_ids
        assert todo3.id in todo_ids

def test_deleted_todo_not_retrievable():
    """Test that deleted todo cannot be retrieved afterward"""
    clear_todos()
    
    todo = Todo("Will be deleted")
    add_todo(todo)
    todo_id = todo.id
    
    with app.test_client() as client:
        # Delete todo
        delete_response = client.delete(f'/api/todos/{todo_id}')
        assert delete_response.status_code == 200
        
        # Verify it's not in storage directly
        stored_todo = get_todo_by_id(todo_id)
        assert stored_todo is None

def test_multiple_deletions():
    """Test multiple deletion operations"""
    clear_todos()
    
    # Create multiple todos
    todos = []
    for i in range(3):
        todo = Todo(f"Todo {i}")
        add_todo(todo)
        todos.append(todo)
    
    with app.test_client() as client:
        # Delete each todo
        for todo in todos:
            response = client.delete(f'/api/todos/{todo.id}')
            assert response.status_code == 200
            
            # Verify response contains correct data
            data = response.get_json()
            assert data['id'] == todo.id
            assert data['text'] == todo.text
        
        # Verify all todos are gone
        get_response = client.get('/api/todos')
        remaining_todos = get_response.get_json()
        assert len(remaining_todos) == 0

if __name__ == '__main__':
    test_delete_valid_todo()
    test_nonexistent_todo_404()
    test_deleted_todo_in_response()
    test_todo_removed_from_storage()
    test_deleted_todo_not_retrievable()
    test_multiple_deletions()
    print("All DELETE todos endpoint tests passed!")