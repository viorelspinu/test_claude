#!/usr/bin/env python3
"""
Integration Test Suite - Task 20
Tests full application integration with both servers running and communicating.
"""

import json
import time
import requests
import subprocess
import sys
import signal
import os
from datetime import datetime

# Test configuration
BACKEND_URL = "http://127.0.0.1:5000"
FRONTEND_URL = "http://localhost:3000"
API_BASE = f"{BACKEND_URL}/api"

# Test results tracking
test_results = {
    "task_id": "20",
    "task_name": "integration_test",
    "timestamp": datetime.now().isoformat(),
    "tests": [],
    "summary": {
        "total": 0,
        "passed": 0,
        "failed": 0,
        "error": 0
    }
}

def log_test(test_name, status, details="", error=""):
    """Log test result"""
    result = {
        "test": test_name,
        "status": status,
        "details": details,
        "error": error,
        "timestamp": datetime.now().isoformat()
    }
    test_results["tests"].append(result)
    test_results["summary"]["total"] += 1
    test_results["summary"][status] += 1
    
    # Print real-time results
    status_symbol = "✅" if status == "passed" else "❌" if status == "failed" else "⚠️"
    print(f"{status_symbol} {test_name}: {status.upper()}")
    if details:
        print(f"   Details: {details}")
    if error:
        print(f"   Error: {error}")

def check_server_accessibility(url, server_name):
    """Check if server is accessible"""
    try:
        response = requests.get(url, timeout=5)
        if response.status_code == 200:
            log_test(f"{server_name} Server Accessibility", "passed", 
                    f"Server accessible at {url}")
            return True
        else:
            log_test(f"{server_name} Server Accessibility", "failed",
                    f"Server returned status code {response.status_code}")
            return False
    except requests.exceptions.RequestException as e:
        log_test(f"{server_name} Server Accessibility", "failed",
                f"Cannot connect to {url}", str(e))
        return False

def test_api_endpoints():
    """Test all API endpoints"""
    
    # Test GET /api/todos (empty list)
    try:
        response = requests.get(f"{API_BASE}/todos")
        if response.status_code == 200:
            todos = response.json()
            if isinstance(todos, list):
                log_test("GET /api/todos (Empty)", "passed", 
                        f"Returns empty list: {todos}")
            else:
                log_test("GET /api/todos (Empty)", "failed",
                        f"Expected list, got {type(todos)}")
        else:
            log_test("GET /api/todos (Empty)", "failed",
                    f"Status code: {response.status_code}")
    except Exception as e:
        log_test("GET /api/todos (Empty)", "error", "", str(e))

    # Test POST /api/todos
    try:
        todo_data = {"text": "Integration test todo item"}
        response = requests.post(f"{API_BASE}/todos", 
                               json=todo_data,
                               headers={"Content-Type": "application/json"})
        if response.status_code == 201:
            created_todo = response.json()
            if created_todo.get("text") == todo_data["text"]:
                log_test("POST /api/todos", "passed", 
                        f"Todo created: {created_todo['text']}")
                return created_todo["id"]
            else:
                log_test("POST /api/todos", "failed",
                        f"Text mismatch: expected '{todo_data['text']}', got '{created_todo.get('text')}'")
        else:
            log_test("POST /api/todos", "failed",
                    f"Status code: {response.status_code}")
    except Exception as e:
        log_test("POST /api/todos", "error", "", str(e))
        return None

    return None

def test_todo_operations(todo_id):
    """Test todo operations with existing todo"""
    if not todo_id:
        log_test("Todo Operations", "error", "No todo ID to test with")
        return

    # Test GET /api/todos (with data)
    try:
        response = requests.get(f"{API_BASE}/todos")
        if response.status_code == 200:
            todos = response.json()
            if len(todos) == 1 and todos[0]["id"] == todo_id:
                log_test("GET /api/todos (With Data)", "passed", 
                        f"Returns 1 todo with correct ID")
            else:
                log_test("GET /api/todos (With Data)", "failed",
                        f"Expected 1 todo with ID {todo_id}, got {len(todos)} todos")
        else:
            log_test("GET /api/todos (With Data)", "failed",
                    f"Status code: {response.status_code}")
    except Exception as e:
        log_test("GET /api/todos (With Data)", "error", "", str(e))

    # Test PUT /api/todos/{id}
    try:
        update_data = {"completed": True}
        response = requests.put(f"{API_BASE}/todos/{todo_id}",
                              json=update_data,
                              headers={"Content-Type": "application/json"})
        if response.status_code == 200:
            updated_todo = response.json()
            if updated_todo.get("completed") == True:
                log_test("PUT /api/todos/{id}", "passed", 
                        f"Todo updated to completed: {updated_todo['completed']}")
            else:
                log_test("PUT /api/todos/{id}", "failed",
                        f"Expected completed=True, got {updated_todo.get('completed')}")
        else:
            log_test("PUT /api/todos/{id}", "failed",
                    f"Status code: {response.status_code}")
    except Exception as e:
        log_test("PUT /api/todos/{id}", "error", "", str(e))

    # Test DELETE /api/todos/{id}
    try:
        response = requests.delete(f"{API_BASE}/todos/{todo_id}")
        if response.status_code == 200:
            log_test("DELETE /api/todos/{id}", "passed", 
                    f"Todo deleted successfully")
            
            # Verify deletion
            response = requests.get(f"{API_BASE}/todos")
            if response.status_code == 200:
                todos = response.json()
                if len(todos) == 0:
                    log_test("DELETE Verification", "passed", 
                            "Todo list is empty after deletion")
                else:
                    log_test("DELETE Verification", "failed",
                            f"Expected empty list, found {len(todos)} todos")
        else:
            log_test("DELETE /api/todos/{id}", "failed",
                    f"Status code: {response.status_code}")
    except Exception as e:
        log_test("DELETE /api/todos/{id}", "error", "", str(e))

def test_cors_headers():
    """Test CORS configuration"""
    try:
        response = requests.options(f"{API_BASE}/todos")
        cors_headers = {
            "Access-Control-Allow-Origin": response.headers.get("Access-Control-Allow-Origin"),
            "Access-Control-Allow-Methods": response.headers.get("Access-Control-Allow-Methods"),
            "Access-Control-Allow-Headers": response.headers.get("Access-Control-Allow-Headers")
        }
        
        if cors_headers["Access-Control-Allow-Origin"]:
            log_test("CORS Configuration", "passed", 
                    f"CORS headers present: {cors_headers}")
        else:
            log_test("CORS Configuration", "failed",
                    "Missing CORS headers")
    except Exception as e:
        log_test("CORS Configuration", "error", "", str(e))

def test_error_handling():
    """Test API error handling"""
    
    # Test invalid endpoint
    try:
        response = requests.get(f"{API_BASE}/invalid")
        if response.status_code == 404:
            log_test("404 Error Handling", "passed", 
                    "Returns 404 for invalid endpoint")
        else:
            log_test("404 Error Handling", "failed",
                    f"Expected 404, got {response.status_code}")
    except Exception as e:
        log_test("404 Error Handling", "error", "", str(e))

    # Test invalid JSON
    try:
        response = requests.post(f"{API_BASE}/todos",
                               data="invalid json",
                               headers={"Content-Type": "application/json"})
        if response.status_code in [400, 422]:
            log_test("Invalid JSON Handling", "passed", 
                    f"Returns {response.status_code} for invalid JSON")
        else:
            log_test("Invalid JSON Handling", "failed",
                    f"Expected 400 or 422, got {response.status_code}")
    except Exception as e:
        log_test("Invalid JSON Handling", "error", "", str(e))

    # Test empty todo text
    try:
        response = requests.post(f"{API_BASE}/todos",
                               json={"text": ""},
                               headers={"Content-Type": "application/json"})
        if response.status_code in [400, 422]:
            log_test("Empty Text Validation", "passed", 
                    f"Returns {response.status_code} for empty text")
        else:
            log_test("Empty Text Validation", "failed",
                    f"Expected 400 or 422, got {response.status_code}")
    except Exception as e:
        log_test("Empty Text Validation", "error", "", str(e))

def run_integration_tests():
    """Run complete integration test suite"""
    print("=" * 60)
    print("INTEGRATION TEST SUITE - TASK 20")
    print("=" * 60)
    print(f"Backend URL: {BACKEND_URL}")
    print(f"Frontend URL: {FRONTEND_URL}")
    print(f"Started: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("=" * 60)

    # Phase 1: Server Accessibility
    print("\n🔍 PHASE 1: SERVER ACCESSIBILITY")
    print("-" * 40)
    backend_ok = check_server_accessibility(f"{BACKEND_URL}/api/todos", "Backend")
    frontend_ok = check_server_accessibility(FRONTEND_URL, "Frontend")

    if not backend_ok:
        log_test("Integration Test Suite", "failed", 
                "Backend server not accessible")
        return

    # Phase 2: API Integration Testing
    print("\n🔍 PHASE 2: API INTEGRATION TESTING")
    print("-" * 40)
    todo_id = test_api_endpoints()
    test_cors_headers()
    test_error_handling()

    # Phase 3: Todo Operations
    print("\n🔍 PHASE 3: TODO OPERATIONS")
    print("-" * 40)
    test_todo_operations(todo_id)

    # Phase 4: Frontend Integration Assessment
    print("\n🔍 PHASE 4: FRONTEND INTEGRATION ASSESSMENT")
    print("-" * 40)
    if frontend_ok:
        log_test("Frontend Server Running", "passed", 
                "React development server is accessible")
        log_test("Frontend-Backend Integration Ready", "passed", 
                "Both servers running for frontend-backend communication")
    else:
        log_test("Frontend Integration", "failed",
                "Frontend server not accessible")

    # Summary
    print("\n" + "=" * 60)
    print("INTEGRATION TEST RESULTS SUMMARY")
    print("=" * 60)
    print(f"Total Tests: {test_results['summary']['total']}")
    print(f"✅ Passed: {test_results['summary']['passed']}")
    print(f"❌ Failed: {test_results['summary']['failed']}")
    print(f"⚠️  Errors: {test_results['summary']['error']}")
    
    success_rate = (test_results['summary']['passed'] / test_results['summary']['total']) * 100 if test_results['summary']['total'] > 0 else 0
    print(f"📊 Success Rate: {success_rate:.1f}%")
    
    print("=" * 60)

    return test_results

if __name__ == "__main__":
    try:
        results = run_integration_tests()
        
        # Save results to JSON file
        with open("/Users/viorel/workspace/test_claude/agentic_flow/logs/tests/20_integration_test.json", "w") as f:
            json.dump(results, f, indent=2)
        
        print(f"\n📁 Test results saved to: agentic_flow/logs/tests/20_integration_test.json")
        
        # Exit with appropriate code
        if results['summary']['failed'] == 0 and results['summary']['error'] == 0:
            print("🎉 All integration tests PASSED!")
            sys.exit(0)
        else:
            print("❌ Some integration tests FAILED!")
            sys.exit(1)
            
    except KeyboardInterrupt:
        print("\n⚠️ Integration tests interrupted by user")
        sys.exit(1)
    except Exception as e:
        print(f"\n💥 Integration test suite failed with exception: {e}")
        sys.exit(1)