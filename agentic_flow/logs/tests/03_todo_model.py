import sys
import os

# Add backend directory to path
backend_path = os.path.join(os.path.dirname(__file__), '../../../backend')
sys.path.insert(0, os.path.abspath(backend_path))

from models import Todo
import datetime
import uuid

def test_todo_instantiation():
    """Test Todo class instantiates correctly"""
    todo = Todo("Test task")
    assert todo is not None
    assert isinstance(todo.id, str)
    assert todo.text == "Test task"
    assert todo.completed == False
    assert isinstance(todo.created_at, datetime.datetime)

def test_todo_attributes():
    """Test all attributes are properly set"""
    todo = Todo("Buy groceries", completed=True)
    assert todo.text == "Buy groceries"
    assert todo.completed == True
    assert len(todo.id) == 36  # UUID string length
    assert isinstance(todo.created_at, datetime.datetime)

def test_string_representation():
    """Test string representation works"""
    incomplete_todo = Todo("Incomplete task")
    completed_todo = Todo("Completed task", completed=True)
    
    assert str(incomplete_todo) == "○ Incomplete task"
    assert str(completed_todo) == "✓ Completed task"

def test_validation():
    """Test validation and default values"""
    # Test empty text validation
    try:
        Todo("")
        assert False, "Should raise ValueError for empty text"
    except ValueError:
        pass
    
    # Test None text validation
    try:
        Todo(None)
        assert False, "Should raise ValueError for None text"
    except (ValueError, TypeError):
        pass
    
    # Test text stripping
    todo = Todo("  Spaced text  ")
    assert todo.text == "Spaced text"

def test_to_dict():
    """Test to_dict method for JSON serialization"""
    todo = Todo("Test task")
    data = todo.to_dict()
    
    assert data['id'] == todo.id
    assert data['text'] == "Test task"
    assert data['completed'] == False
    assert 'created_at' in data

if __name__ == '__main__':
    test_todo_instantiation()
    test_todo_attributes()
    test_string_representation()
    test_validation()
    test_to_dict()
    print("All Todo model tests passed!")