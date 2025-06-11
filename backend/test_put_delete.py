#!/usr/bin/env python3
"""
Test script for PUT and DELETE /api/todos endpoints
"""

import requests
import json
import sys

BASE_URL = 'http://localhost:8080/api'
HEADERS = {'Content-Type': 'application/json'}

def print_test(name, passed, details=""):
    status = "✅ PASSED" if passed else "❌ FAILED"
    print(f"{name}: {status}")
    if details:
        print(f"   {details}")
    print()

def test_put_delete_endpoints():
    print("=== Testing PUT/DELETE Endpoints ===\n")
    
    # First, create a test todo
    print("Setup: Creating test todos...")
    test_todos = []
    for i in range(2):
        response = requests.post(f'{BASE_URL}/todos', 
                                json={'text': f'Test todo {i+1} for PUT/DELETE'},
                                headers=HEADERS)
        if response.status_code == 201:
            test_todos.append(response.json())
            print(f"   Created todo ID: {response.json()['id']}")
    
    if len(test_todos) < 2:
        print("❌ Failed to create test todos")
        return
    
    todo_id = test_todos[0]['id']
    delete_id = test_todos[1]['id']
    
    print(f"\nTesting with Todo ID: {todo_id}")
    print("="*50 + "\n")
    
    # Test 1: PUT - Update text only
    print("1. Testing PUT - Update text only")
    update_data = {'text': 'Updated todo text'}
    response = requests.put(f'{BASE_URL}/todos/{todo_id}',
                          json=update_data,
                          headers=HEADERS)
    passed = response.status_code == 200
    if passed:
        updated = response.json()
        passed = updated['text'] == 'Updated todo text' and updated['completed'] == False
    print_test("Update text only", passed, 
               f"Status: {response.status_code}, Response: {response.json() if response.status_code == 200 else response.text}")
    
    # Test 2: PUT - Toggle completed status
    print("2. Testing PUT - Toggle completed status")
    update_data = {'completed': True}
    response = requests.put(f'{BASE_URL}/todos/{todo_id}',
                          json=update_data,
                          headers=HEADERS)
    passed = response.status_code == 200
    if passed:
        updated = response.json()
        passed = updated['completed'] == True and updated['text'] == 'Updated todo text'
    print_test("Toggle completed status", passed,
               f"Status: {response.status_code}, Completed: {response.json().get('completed') if response.status_code == 200 else 'N/A'}")
    
    # Test 3: PUT - Update both fields
    print("3. Testing PUT - Update both text and completed")
    update_data = {'text': 'Final updated text', 'completed': False}
    response = requests.put(f'{BASE_URL}/todos/{todo_id}',
                          json=update_data,
                          headers=HEADERS)
    passed = response.status_code == 200
    if passed:
        updated = response.json()
        passed = updated['text'] == 'Final updated text' and updated['completed'] == False
    print_test("Update both fields", passed,
               f"Status: {response.status_code}, Text: '{response.json().get('text')}', Completed: {response.json().get('completed')}" if response.status_code == 200 else response.text)
    
    # Test 4: PUT - Empty text validation
    print("4. Testing PUT - Empty text validation")
    update_data = {'text': '   '}
    response = requests.put(f'{BASE_URL}/todos/{todo_id}',
                          json=update_data,
                          headers=HEADERS)
    passed = response.status_code == 400
    print_test("Empty text validation", passed,
               f"Status: {response.status_code}, Error: {response.json().get('error') if response.status_code == 400 else 'No error'}")
    
    # Test 5: PUT - Invalid completed type
    print("5. Testing PUT - Invalid completed type")
    update_data = {'completed': 'not-a-boolean'}
    response = requests.put(f'{BASE_URL}/todos/{todo_id}',
                          json=update_data,
                          headers=HEADERS)
    passed = response.status_code == 400
    print_test("Invalid completed type", passed,
               f"Status: {response.status_code}, Error: {response.json().get('error') if response.status_code == 400 else 'No error'}")
    
    # Test 6: PUT - Non-existent ID
    print("6. Testing PUT - Non-existent todo ID")
    update_data = {'text': 'This should fail'}
    response = requests.put(f'{BASE_URL}/todos/99999',
                          json=update_data,
                          headers=HEADERS)
    passed = response.status_code == 404
    print_test("Non-existent ID (PUT)", passed,
               f"Status: {response.status_code}, Error: {response.json().get('error') if response.status_code == 404 else 'No error'}")
    
    # Test 7: DELETE - Existing todo
    print("7. Testing DELETE - Existing todo")
    response = requests.delete(f'{BASE_URL}/todos/{delete_id}')
    passed = response.status_code == 200
    print_test("Delete existing todo", passed,
               f"Status: {response.status_code}, Message: {response.json().get('message') if response.status_code == 200 else response.text}")
    
    # Verify deletion
    print("8. Verifying todo was deleted")
    response = requests.get(f'{BASE_URL}/todos')
    if response.status_code == 200:
        todos = response.json()
        deleted = not any(todo['id'] == delete_id for todo in todos)
        print_test("Deletion verification", deleted,
                   f"Todo ID {delete_id} {'not found' if deleted else 'still exists'} in database")
    
    # Test 8: DELETE - Non-existent ID
    print("9. Testing DELETE - Non-existent todo ID")
    response = requests.delete(f'{BASE_URL}/todos/99999')
    passed = response.status_code == 404
    print_test("Non-existent ID (DELETE)", passed,
               f"Status: {response.status_code}, Error: {response.json().get('error') if response.status_code == 404 else 'No error'}")
    
    # Test 9: Text length validation
    print("10. Testing PUT - Text over 200 characters")
    long_text = 'x' * 201
    update_data = {'text': long_text}
    response = requests.put(f'{BASE_URL}/todos/{todo_id}',
                          json=update_data,
                          headers=HEADERS)
    passed = response.status_code == 400
    print_test("Text length validation", passed,
               f"Status: {response.status_code}, Error: {response.json().get('error') if response.status_code == 400 else 'No error'}")
    
    print("\n=== All Tests Complete ===")

if __name__ == '__main__':
    try:
        # Test if server is running
        response = requests.get(f'{BASE_URL}/health')
        if response.status_code != 200:
            print("❌ Backend server not running on port 8080")
            sys.exit(1)
        
        test_put_delete_endpoints()
        
    except requests.exceptions.ConnectionError:
        print("❌ Cannot connect to backend server at http://localhost:8080")
        print("   Please start the backend server first: python app.py")
        sys.exit(1)
    except Exception as e:
        print(f"❌ Unexpected error: {e}")
        sys.exit(1)