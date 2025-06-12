from datetime import datetime
import uuid
import threading

class Todo:
    def __init__(self, text, completed=False):
        if not text or not text.strip():
            raise ValueError("Todo text cannot be empty")
        
        self.id = str(uuid.uuid4())
        self.text = text.strip()
        self.completed = completed
        self.created_at = datetime.now()
    
    def __str__(self):
        status = "✓" if self.completed else "○"
        return f"{status} {self.text}"
    
    def to_dict(self):
        return {
            'id': self.id,
            'text': self.text,
            'completed': self.completed,
            'created_at': self.created_at.isoformat()
        }


# In-memory storage
_todos = []
_lock = threading.Lock()

def add_todo(todo):
    """Add a todo to storage"""
    with _lock:
        _todos.append(todo)
    return todo

def get_all_todos():
    """Get all todos from storage"""
    with _lock:
        return _todos.copy()

def get_todo_by_id(todo_id):
    """Get a todo by ID"""
    with _lock:
        for todo in _todos:
            if todo.id == todo_id:
                return todo
    return None

def update_todo(todo_id, text=None, completed=None):
    """Update a todo in storage"""
    with _lock:
        for todo in _todos:
            if todo.id == todo_id:
                if text is not None:
                    todo.text = text.strip()
                if completed is not None:
                    todo.completed = completed
                return todo
    return None

def delete_todo(todo_id):
    """Delete a todo from storage"""
    with _lock:
        for i, todo in enumerate(_todos):
            if todo.id == todo_id:
                return _todos.pop(i)
    return None

def clear_todos():
    """Clear all todos (for testing)"""
    with _lock:
        _todos.clear()