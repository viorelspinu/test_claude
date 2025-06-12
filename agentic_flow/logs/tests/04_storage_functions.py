import sys
import os

# Add backend directory to path
backend_path = os.path.join(os.path.dirname(__file__), '../../../backend')
sys.path.insert(0, os.path.abspath(backend_path))

from models import Todo, add_todo, get_all_todos, get_todo_by_id, update_todo, delete_todo, clear_todos
import threading
import time

def test_storage_with_todos():
    """Test storage functions work with Todo instances"""
    clear_todos()
    
    todo1 = Todo("Test task 1")
    todo2 = Todo("Test task 2", completed=True)
    
    # Add todos
    result1 = add_todo(todo1)
    result2 = add_todo(todo2)
    
    assert result1 == todo1
    assert result2 == todo2
    
    # Get all todos
    all_todos = get_all_todos()
    assert len(all_todos) == 2
    assert todo1 in all_todos
    assert todo2 in all_todos

def test_crud_operations():
    """Test CRUD operations work correctly"""
    clear_todos()
    
    # Create
    todo = Todo("CRUD test")
    add_todo(todo)
    
    # Read
    found = get_todo_by_id(todo.id)
    assert found is not None
    assert found.text == "CRUD test"
    assert found.completed == False
    
    # Update
    updated = update_todo(todo.id, text="Updated CRUD", completed=True)
    assert updated is not None
    assert updated.text == "Updated CRUD"
    assert updated.completed == True
    
    # Delete
    deleted = delete_todo(todo.id)
    assert deleted is not None
    assert deleted.id == todo.id
    
    # Verify deletion
    not_found = get_todo_by_id(todo.id)
    assert not_found is None

def test_storage_persistence():
    """Test storage persistence within session"""
    clear_todos()
    
    # Add todos
    todo1 = Todo("Persistent 1")
    todo2 = Todo("Persistent 2")
    add_todo(todo1)
    add_todo(todo2)
    
    # Verify persistence across function calls
    first_call = get_all_todos()
    second_call = get_all_todos()
    
    assert len(first_call) == 2
    assert len(second_call) == 2
    assert first_call[0].id == second_call[0].id

def test_error_handling():
    """Test error handling for missing todos"""
    clear_todos()
    
    # Test get by non-existent ID
    result = get_todo_by_id("nonexistent-id")
    assert result is None
    
    # Test update non-existent todo
    result = update_todo("nonexistent-id", text="New text")
    assert result is None
    
    # Test delete non-existent todo
    result = delete_todo("nonexistent-id")
    assert result is None

def test_thread_safety():
    """Test thread safety of storage operations"""
    clear_todos()
    
    def add_todos_threaded(start_num):
        for i in range(start_num, start_num + 10):
            todo = Todo(f"Thread todo {i}")
            add_todo(todo)
    
    # Create multiple threads
    threads = []
    for i in range(0, 30, 10):
        thread = threading.Thread(target=add_todos_threaded, args=(i,))
        threads.append(thread)
        thread.start()
    
    # Wait for all threads
    for thread in threads:
        thread.join()
    
    # Verify all todos were added
    all_todos = get_all_todos()
    assert len(all_todos) == 30

if __name__ == '__main__':
    test_storage_with_todos()
    test_crud_operations()
    test_storage_persistence()
    test_error_handling()
    test_thread_safety()
    print("All storage function tests passed!")