#!/usr/bin/env python3
"""Test script for API endpoints."""

import os
import json
import requests
import time
import subprocess
import signal
import sys
from multiprocessing import Process

def start_flask_server():
    """Start Flask server in background."""
    os.chdir('/Users/viorel/workspace/test_claude/backend')
    os.system('python app.py > /dev/null 2>&1 &')

def test_api_endpoints():
    """Test all API endpoints."""
    base_url = 'http://localhost:5000'
    
    print("Testing API endpoints...")
    
    # Wait for server to start
    print("Waiting for server to start...")
    time.sleep(3)
    
    try:
        # Test 1: Health check
        print("1. Testing health check...")
        response = requests.get(f'{base_url}/api/health')
        assert response.status_code == 200
        assert response.json()['status'] == 'healthy'
        print("✓ Health check passed")
        
        # Test 2: Get all todos (initially empty)
        print("2. Testing GET /api/todos...")
        response = requests.get(f'{base_url}/api/todos')
        assert response.status_code == 200
        todos = response.json()
        print(f"✓ GET todos: {len(todos)} todos found")
        
        # Test 3: Create new todo
        print("3. Testing POST /api/todos...")
        new_todo = {'text': 'Test API todo'}
        response = requests.post(f'{base_url}/api/todos', json=new_todo)
        assert response.status_code == 201
        created_todo = response.json()
        todo_id = created_todo['id']
        assert created_todo['text'] == 'Test API todo'
        assert created_todo['completed'] == 0
        print(f"✓ Created todo with ID: {todo_id}")
        
        # Test 4: Get todos again (should have 1)
        print("4. Testing GET /api/todos after creation...")
        response = requests.get(f'{base_url}/api/todos')
        assert response.status_code == 200
        todos = response.json()
        assert len(todos) == 1
        print(f"✓ GET todos: {len(todos)} todo found")
        
        # Test 5: Update todo
        print("5. Testing PUT /api/todos/{id}...")
        update_data = {'completed': True}
        response = requests.put(f'{base_url}/api/todos/{todo_id}', json=update_data)
        assert response.status_code == 200
        updated_todo = response.json()
        assert updated_todo['completed'] == 1
        print(f"✓ Updated todo completion status")
        
        # Test 6: Test error cases
        print("6. Testing error cases...")
        
        # Invalid POST (missing text)
        response = requests.post(f'{base_url}/api/todos', json={})
        assert response.status_code == 400
        print("✓ POST with missing text returns 400")
        
        # Invalid PUT (missing completed)
        response = requests.put(f'{base_url}/api/todos/{todo_id}', json={})
        assert response.status_code == 400
        print("✓ PUT with missing completed returns 400")
        
        # PUT non-existent todo
        response = requests.put(f'{base_url}/api/todos/999', json={'completed': True})
        assert response.status_code == 404
        print("✓ PUT non-existent todo returns 404")
        
        # DELETE non-existent todo
        response = requests.delete(f'{base_url}/api/todos/999')
        assert response.status_code == 404
        print("✓ DELETE non-existent todo returns 404")
        
        # Test 7: Delete todo
        print("7. Testing DELETE /api/todos/{id}...")
        response = requests.delete(f'{base_url}/api/todos/{todo_id}')
        assert response.status_code == 200
        assert 'message' in response.json()
        print("✓ Deleted todo successfully")
        
        # Test 8: Verify deletion
        print("8. Testing GET /api/todos after deletion...")
        response = requests.get(f'{base_url}/api/todos')
        assert response.status_code == 200
        todos = response.json()
        assert len(todos) == 0
        print(f"✓ GET todos: {len(todos)} todos found (after deletion)")
        
        print("\nAll API tests passed! ✅")
        return True
        
    except Exception as e:
        print(f"❌ API test failed: {e}")
        return False

if __name__ == "__main__":
    print("Starting Flask server...")
    start_flask_server()
    
    try:
        success = test_api_endpoints()
        if not success:
            sys.exit(1)
    finally:
        # Kill Flask server
        os.system("pkill -f 'python app.py'")
        print("Flask server stopped.")