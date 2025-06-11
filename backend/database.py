import sqlite3
import os
from datetime import datetime
from typing import List, Dict, Optional

DATABASE_PATH = 'todos.db'

def init_database():
    """Initialize the database and create tables if they don't exist."""
    conn = sqlite3.connect(DATABASE_PATH)
    cursor = conn.cursor()
    
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS todos (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            text TEXT NOT NULL,
            completed BOOLEAN DEFAULT 0,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    
    conn.commit()
    conn.close()

def get_all_todos() -> List[Dict]:
    """Retrieve all todos from the database."""
    conn = sqlite3.connect(DATABASE_PATH)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    
    cursor.execute('SELECT * FROM todos ORDER BY created_at DESC')
    todos = [dict(row) for row in cursor.fetchall()]
    
    conn.close()
    return todos

def create_todo(text: str) -> Dict:
    """Create a new todo and return it."""
    conn = sqlite3.connect(DATABASE_PATH)
    cursor = conn.cursor()
    
    cursor.execute(
        'INSERT INTO todos (text, completed) VALUES (?, ?)',
        (text, False)
    )
    todo_id = cursor.lastrowid
    
    conn.commit()
    conn.close()
    
    return get_todo_by_id(todo_id)

def get_todo_by_id(todo_id: int) -> Optional[Dict]:
    """Get a specific todo by its ID."""
    conn = sqlite3.connect(DATABASE_PATH)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    
    cursor.execute('SELECT * FROM todos WHERE id = ?', (todo_id,))
    row = cursor.fetchone()
    
    conn.close()
    
    if row:
        return dict(row)
    return None

def update_todo(todo_id: int, completed: bool) -> Optional[Dict]:
    """Update a todo's completed status."""
    conn = sqlite3.connect(DATABASE_PATH)
    cursor = conn.cursor()
    
    cursor.execute(
        'UPDATE todos SET completed = ? WHERE id = ?',
        (completed, todo_id)
    )
    
    if cursor.rowcount == 0:
        conn.close()
        return None
    
    conn.commit()
    conn.close()
    
    return get_todo_by_id(todo_id)

def delete_todo(todo_id: int) -> bool:
    """Delete a todo by its ID. Returns True if deleted, False if not found."""
    conn = sqlite3.connect(DATABASE_PATH)
    cursor = conn.cursor()
    
    cursor.execute('DELETE FROM todos WHERE id = ?', (todo_id,))
    deleted = cursor.rowcount > 0
    
    conn.commit()
    conn.close()
    
    return deleted