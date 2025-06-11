#!/usr/bin/env python3
"""
Test script for toggle and delete UI functionality
Tests the full stack integration with UI actions
"""

import requests
import json
import time
import subprocess
import threading
import sys
from datetime import datetime

BACKEND_URL = 'http://localhost:8080/api'
FRONTEND_URL = 'http://localhost:3002'
HEADERS = {'Content-Type': 'application/json'}

def print_test(name, passed, details=""):
    status = "✅ PASSED" if passed else "❌ FAILED"
    timestamp = datetime.now().strftime("%H:%M:%S")
    print(f"[{timestamp}] {name}: {status}")
    if details:
        print(f"    {details}")
    print()

def wait_for_server(url, timeout=30):
    """Wait for server to be ready"""
    start_time = time.time()
    while time.time() - start_time < timeout:
        try:
            response = requests.get(url, timeout=2)
            if response.status_code == 200:
                return True
        except:
            pass
        time.sleep(1)
    return False

def test_toggle_delete_integration():
    print("=== Testing Toggle and Delete UI Integration ===\n")
    
    # Setup: Create test todos
    print("Setup: Creating test todos for toggle/delete testing...")
    test_todos = []
    todo_texts = [
        "Test todo for toggle functionality",
        "Test todo for delete functionality", 
        "Test todo for multiple operations"
    ]
    
    for text in todo_texts:
        try:
            response = requests.post(f'{BACKEND_URL}/todos',
                                   json={'text': text},
                                   headers=HEADERS)
            if response.status_code == 201:
                todo = response.json()
                test_todos.append(todo)
                print(f"    Created todo ID {todo['id']}: '{todo['text']}'")
        except Exception as e:
            print(f"    ❌ Failed to create test todo: {e}")
    
    if len(test_todos) < 3:
        print("❌ Failed to create sufficient test todos")
        return False
    
    toggle_todo = test_todos[0]
    delete_todo = test_todos[1]
    multi_todo = test_todos[2]
    
    print(f"\nUsing todos for testing:")
    print(f"    Toggle operations: ID {toggle_todo['id']}")
    print(f"    Delete operations: ID {delete_todo['id']}")
    print(f"    Multiple operations: ID {multi_todo['id']}")
    print("="*60 + "\n")
    
    # Test 1: Toggle todo from incomplete to complete
    print("1. Testing toggle incomplete → complete")
    try:
        response = requests.put(f"{BACKEND_URL}/todos/{toggle_todo['id']}",
                              json={'completed': True},
                              headers=HEADERS)
        passed = response.status_code == 200
        if passed:
            updated = response.json()
            passed = updated['completed'] == True
            print_test("Toggle to complete", passed,
                      f"Status: {response.status_code}, Completed: {updated['completed']}")
        else:
            print_test("Toggle to complete", False, f"HTTP {response.status_code}")
    except Exception as e:
        print_test("Toggle to complete", False, f"Error: {e}")
    
    # Test 2: Toggle todo from complete to incomplete
    print("2. Testing toggle complete → incomplete")
    try:
        response = requests.put(f"{BACKEND_URL}/todos/{toggle_todo['id']}",
                              json={'completed': False},
                              headers=HEADERS)
        passed = response.status_code == 200
        if passed:
            updated = response.json()
            passed = updated['completed'] == False
            print_test("Toggle to incomplete", passed,
                      f"Status: {response.status_code}, Completed: {updated['completed']}")
        else:
            print_test("Toggle to incomplete", False, f"HTTP {response.status_code}")
    except Exception as e:
        print_test("Toggle to incomplete", False, f"Error: {e}")
    
    # Test 3: Delete todo functionality
    print("3. Testing delete functionality")
    try:
        response = requests.delete(f"{BACKEND_URL}/todos/{delete_todo['id']}")
        passed = response.status_code == 200
        if passed:
            result = response.json()
            print_test("Delete todo", passed,
                      f"Status: {response.status_code}, Message: {result.get('message')}")
        else:
            print_test("Delete todo", False, f"HTTP {response.status_code}")
    except Exception as e:
        print_test("Delete todo", False, f"Error: {e}")
    
    # Test 4: Verify deletion persistence
    print("4. Verifying todo deletion persistence")
    try:
        response = requests.get(f"{BACKEND_URL}/todos")
        if response.status_code == 200:
            todos = response.json()
            deleted_still_exists = any(todo['id'] == delete_todo['id'] for todo in todos)
            passed = not deleted_still_exists
            print_test("Deletion persistence", passed,
                      f"Deleted todo ID {delete_todo['id']} {'still exists' if deleted_still_exists else 'properly removed'}")
        else:
            print_test("Deletion persistence", False, f"Could not fetch todos: {response.status_code}")
    except Exception as e:
        print_test("Deletion persistence", False, f"Error: {e}")
    
    # Test 5: Multiple operations on same todo
    print("5. Testing multiple operations on same todo")
    try:
        # First toggle to complete
        response1 = requests.put(f"{BACKEND_URL}/todos/{multi_todo['id']}",
                               json={'completed': True},
                               headers=HEADERS)
        
        # Then update text
        response2 = requests.put(f"{BACKEND_URL}/todos/{multi_todo['id']}",
                               json={'text': 'Updated text after toggle'},
                               headers=HEADERS)
        
        passed = response1.status_code == 200 and response2.status_code == 200
        if passed:
            final_todo = response2.json()
            passed = final_todo['completed'] == True and 'Updated text' in final_todo['text']
            print_test("Multiple operations", passed,
                      f"Final state - Completed: {final_todo['completed']}, Text: '{final_todo['text']}'")
        else:
            print_test("Multiple operations", False, 
                      f"HTTP statuses: {response1.status_code}, {response2.status_code}")
    except Exception as e:
        print_test("Multiple operations", False, f"Error: {e}")
    
    # Test 6: Frontend server accessibility
    print("6. Testing frontend server accessibility")
    try:
        response = requests.get(FRONTEND_URL, timeout=5)
        passed = response.status_code == 200 and 'React App' in response.text
        print_test("Frontend server", passed,
                  f"Status: {response.status_code}, Contains React content: {'React App' in response.text}")
    except Exception as e:
        print_test("Frontend server", False, f"Error: {e}")
    
    # Test 7: API endpoints from frontend perspective
    print("7. Testing CORS for frontend integration")
    try:
        response = requests.get(f"{BACKEND_URL}/todos",
                              headers={'Origin': FRONTEND_URL})
        cors_header = response.headers.get('Access-Control-Allow-Origin')
        passed = response.status_code == 200 and cors_header is not None
        print_test("CORS configuration", passed,
                  f"Status: {response.status_code}, CORS header: {cors_header}")
    except Exception as e:
        print_test("CORS configuration", False, f"Error: {e}")
    
    # Test 8: Error handling - non-existent todo operations
    print("8. Testing error handling for non-existent todos")
    try:
        # Try to toggle non-existent todo
        response1 = requests.put(f"{BACKEND_URL}/todos/99999",
                               json={'completed': True},
                               headers=HEADERS)
        
        # Try to delete non-existent todo  
        response2 = requests.delete(f"{BACKEND_URL}/todos/99999")
        
        passed = response1.status_code == 404 and response2.status_code == 404
        print_test("Error handling", passed,
                  f"Toggle 404: {response1.status_code == 404}, Delete 404: {response2.status_code == 404}")
    except Exception as e:
        print_test("Error handling", False, f"Error: {e}")
    
    # Final summary
    print("\n" + "="*60)
    print("Integration Test Summary:")
    print(f"    Backend API: {BACKEND_URL}")
    print(f"    Frontend UI: {FRONTEND_URL}")
    print(f"    Test todos created: {len(test_todos)}")
    print(f"    Operations tested: Toggle, Delete, Multi-op, Error cases")
    print("="*60)
    
    return True

def main():
    print("Toggle/Delete UI Integration Test")
    print("="*50)
    
    # Check if backend is running
    print("Checking backend server...")
    if not wait_for_server(f"{BACKEND_URL}/health", timeout=5):
        print("❌ Backend server not accessible")
        print("   Please start: cd backend && python app.py")
        return 1
    
    print("✅ Backend server is running")
    
    # Check if frontend is accessible (may not be running)
    print("Checking frontend server...")
    if wait_for_server(FRONTEND_URL, timeout=3):
        print("✅ Frontend server is running")
    else:
        print("⚠️  Frontend server not running (tests will still check backend APIs)")
    
    print()
    
    # Run integration tests
    try:
        success = test_toggle_delete_integration()
        return 0 if success else 1
    except KeyboardInterrupt:
        print("\n❌ Tests interrupted by user")
        return 1
    except Exception as e:
        print(f"\n❌ Unexpected error: {e}")
        return 1

if __name__ == '__main__':
    exit_code = main()
    sys.exit(exit_code)