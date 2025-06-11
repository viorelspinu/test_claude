#!/usr/bin/env python3
"""Test script for database operations."""

import os
import sys
from database import init_database, create_todo, get_all_todos, update_todo, delete_todo, get_todo_by_id

def test_database_operations():
    """Test all database operations."""
    print("Testing database operations...")
    
    # Clean up any existing test database
    if os.path.exists('todos.db'):
        os.remove('todos.db')
    
    # Test 1: Initialize database
    print("1. Testing database initialization...")
    init_database()
    print("✓ Database initialized")
    
    # Test 2: Create todos
    print("2. Testing todo creation...")
    todo1 = create_todo("Test todo 1")
    todo2 = create_todo("Test todo 2")
    print(f"✓ Created todo 1: {todo1}")
    print(f"✓ Created todo 2: {todo2}")
    
    # Test 3: Get all todos
    print("3. Testing get all todos...")
    all_todos = get_all_todos()
    print(f"✓ Retrieved {len(all_todos)} todos")
    
    # Test 4: Get specific todo
    print("4. Testing get specific todo...")
    specific_todo = get_todo_by_id(todo1['id'])
    print(f"✓ Retrieved specific todo: {specific_todo}")
    
    # Test 5: Update todo
    print("5. Testing todo update...")
    updated_todo = update_todo(todo1['id'], True)
    print(f"✓ Updated todo: {updated_todo}")
    
    # Test 6: Delete todo
    print("6. Testing todo deletion...")
    deleted = delete_todo(todo2['id'])
    print(f"✓ Deleted todo: {deleted}")
    
    # Test 7: Verify final state
    print("7. Testing final state...")
    final_todos = get_all_todos()
    print(f"✓ Final todos count: {len(final_todos)}")
    
    print("\nAll tests passed! ✅")
    return True

if __name__ == "__main__":
    try:
        test_database_operations()
    except Exception as e:
        print(f"❌ Test failed: {e}")
        sys.exit(1)