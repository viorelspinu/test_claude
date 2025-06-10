#!/usr/bin/env python3
"""
API Testing Script

Tests all API endpoints to ensure they work correctly.
This script can be run to validate the API implementation.
"""

import requests
import json
import sys
import time
from datetime import datetime

# API base URL
BASE_URL = "http://localhost:5001/api"

def print_response(response, description):
    """Print response details for debugging"""
    print(f"\n=== {description} ===")
    print(f"Status Code: {response.status_code}")
    print(f"Headers: {dict(response.headers)}")
    if response.text:
        try:
            print(f"Response: {json.dumps(response.json(), indent=2)}")
        except:
            print(f"Response: {response.text}")
    print("-" * 50)

def test_create_task():
    """Test POST /api/tasks"""
    url = f"{BASE_URL}/tasks"
    data = {
        "title": "Test Task 1",
        "description": "This is a test task",
        "priority": "High"
    }
    
    response = requests.post(url, json=data)
    print_response(response, "CREATE TASK")
    
    if response.status_code == 201:
        return response.json()["data"]["id"]
    return None

def test_get_tasks():
    """Test GET /api/tasks"""
    url = f"{BASE_URL}/tasks"
    
    # Test basic request
    response = requests.get(url)
    print_response(response, "GET ALL TASKS")
    
    # Test with filters
    response = requests.get(url, params={
        "completed": "false",
        "priority": "High",
        "sort": "created_at",
        "order": "desc",
        "limit": 10
    })
    print_response(response, "GET FILTERED TASKS")

def test_update_task(task_id):
    """Test PUT /api/tasks/{id}"""
    if not task_id:
        print("No task ID provided for update test")
        return
    
    url = f"{BASE_URL}/tasks/{task_id}"
    data = {
        "title": "Updated Test Task",
        "description": "This task has been updated",
        "priority": "Medium",
        "completed": True
    }
    
    response = requests.put(url, json=data)
    print_response(response, f"UPDATE TASK {task_id}")

def test_get_stats():
    """Test GET /api/tasks/stats"""
    url = f"{BASE_URL}/tasks/stats"
    
    response = requests.get(url)
    print_response(response, "GET TASK STATS")

def test_delete_task(task_id):
    """Test DELETE /api/tasks/{id}"""
    if not task_id:
        print("No task ID provided for delete test")
        return
    
    url = f"{BASE_URL}/tasks/{task_id}"
    
    response = requests.delete(url)
    print_response(response, f"DELETE TASK {task_id}")

def test_error_cases():
    """Test various error scenarios"""
    print("\n=== TESTING ERROR CASES ===")
    
    # Test invalid task creation
    url = f"{BASE_URL}/tasks"
    invalid_data = {"description": "No title provided"}
    response = requests.post(url, json=invalid_data)
    print_response(response, "CREATE TASK WITHOUT TITLE (Should fail)")
    
    # Test updating non-existent task
    url = f"{BASE_URL}/tasks/99999"
    data = {"title": "Updated"}
    response = requests.put(url, json=data)
    print_response(response, "UPDATE NON-EXISTENT TASK (Should fail)")
    
    # Test deleting non-existent task
    url = f"{BASE_URL}/tasks/99999"
    response = requests.delete(url)
    print_response(response, "DELETE NON-EXISTENT TASK (Should fail)")

def main():
    """Run all tests"""
    print("Starting API Tests...")
    print("Make sure the Flask server is running on localhost:5001")
    
    try:
        # Test basic connectivity
        response = requests.get(f"{BASE_URL}/tasks/stats")
        if response.status_code != 200:
            print("Error: Cannot connect to API server. Make sure it's running on port 5001.")
            sys.exit(1)
        
        # Run tests
        print("\n🧪 Testing API Endpoints...")
        
        # Create a task
        task_id = test_create_task()
        
        # Create a few more tasks for better testing
        for i in range(2, 4):
            requests.post(f"{BASE_URL}/tasks", json={
                "title": f"Test Task {i}",
                "description": f"Description for task {i}",
                "priority": ["Low", "Medium"][i % 2]
            })
        
        # Test getting tasks
        test_get_tasks()
        
        # Test update
        test_update_task(task_id)
        
        # Test stats
        test_get_stats()
        
        # Test error cases
        test_error_cases()
        
        # Clean up - delete the task
        test_delete_task(task_id)
        
        print("\n✅ API Tests Completed!")
        
    except requests.exceptions.ConnectionError:
        print("❌ Error: Cannot connect to the API server.")
        print("Make sure the Flask server is running on localhost:5001")
        sys.exit(1)
    except Exception as e:
        print(f"❌ Error during testing: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()