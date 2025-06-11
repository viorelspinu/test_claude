# Database Model Implementation

## Files Created
- `/backend/database.py` - Complete database layer with SQLite operations

## Implementation Details

### Database Schema
```sql
CREATE TABLE todos (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    text TEXT NOT NULL,
    completed BOOLEAN DEFAULT 0,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
)
```

### Functions Implemented
- `init_database()` - Creates database and tables
- `get_all_todos()` - Retrieves all todos
- `create_todo(text)` - Creates new todo
- `get_todo_by_id(id)` - Gets specific todo
- `update_todo(id, completed)` - Updates completion status
- `delete_todo(id)` - Deletes todo

### Features
- Type hints for better code quality
- Error handling with return values
- SQLite row factory for dict conversion
- Proper connection management