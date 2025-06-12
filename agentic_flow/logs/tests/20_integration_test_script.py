#!/usr/bin/env python3
"""
Integration Test Script - Task 20: Final Integration Testing
Complete end-to-end testing of Flask + React todo application
"""

import requests
import json
import time
import sys
import os
from typing import Dict, List, Optional, Tuple
from datetime import datetime

class TodoIntegrationTester:
    """Comprehensive integration tester for todo application"""
    
    def __init__(self, backend_url: str = "http://localhost:5000", frontend_url: str = "http://localhost:3000"):
        self.backend_url = backend_url.rstrip('/')
        self.frontend_url = frontend_url.rstrip('/')
        self.test_results = []
        self.todos_created = []  # Track todos for cleanup
        
    def log_test(self, test_name: str, passed: bool, details: str = "", error: str = ""):
        """Log test result"""
        result = {
            "test_name": test_name,
            "passed": passed,
            "details": details,
            "error": error,
            "timestamp": datetime.now().isoformat()
        }
        self.test_results.append(result)
        status = "✅ PASS" if passed else "❌ FAIL"
        print(f"{status}: {test_name}")
        if details:
            print(f"    Details: {details}")
        if error:
            print(f"    Error: {error}")
    
    def test_backend_connectivity(self) -> bool:
        """Test 1: Backend server connectivity"""
        try:
            response = requests.get(f"{self.backend_url}/todos", timeout=5)
            if response.status_code == 200:
                self.log_test("Backend Connectivity", True, f"Backend responding on {self.backend_url}")
                return True
            else:
                self.log_test("Backend Connectivity", False, "", f"Unexpected status code: {response.status_code}")
                return False
        except requests.exceptions.RequestException as e:
            self.log_test("Backend Connectivity", False, "", f"Connection failed: {str(e)}")
            return False
    
    def test_frontend_connectivity(self) -> bool:
        """Test 2: Frontend server connectivity"""
        try:
            response = requests.get(self.frontend_url, timeout=5)
            if response.status_code == 200:
                self.log_test("Frontend Connectivity", True, f"Frontend serving on {self.frontend_url}")
                return True
            else:
                self.log_test("Frontend Connectivity", False, "", f"Unexpected status code: {response.status_code}")
                return False
        except requests.exceptions.RequestException as e:
            self.log_test("Frontend Connectivity", False, "", f"Connection failed: {str(e)}")
            return False
    
    def test_cors_configuration(self) -> bool:
        """Test 3: CORS configuration for cross-origin requests"""
        try:
            headers = {
                'Origin': self.frontend_url,
                'Access-Control-Request-Method': 'POST',
                'Access-Control-Request-Headers': 'Content-Type'
            }
            response = requests.options(f"{self.backend_url}/todos", headers=headers, timeout=5)
            
            cors_headers = response.headers
            has_cors = (
                'Access-Control-Allow-Origin' in cors_headers and
                'Access-Control-Allow-Methods' in cors_headers
            )
            
            if has_cors:
                self.log_test("CORS Configuration", True, "CORS headers present for cross-origin requests")
                return True
            else:
                self.log_test("CORS Configuration", False, "", "Missing required CORS headers")
                return False
        except requests.exceptions.RequestException as e:
            self.log_test("CORS Configuration", False, "", f"CORS test failed: {str(e)}")
            return False
    
    def test_empty_todos_list(self) -> bool:
        """Test 4: Initial empty todos list"""
        try:
            response = requests.get(f"{self.backend_url}/todos", timeout=5)
            if response.status_code == 200:
                todos = response.json()
                if isinstance(todos, list):
                    self.log_test("Empty Todos List", True, f"Retrieved {len(todos)} todos (empty state working)")
                    return True
                else:
                    self.log_test("Empty Todos List", False, "", "Response is not a list")
                    return False
            else:
                self.log_test("Empty Todos List", False, "", f"Failed to get todos: {response.status_code}")
                return False
        except Exception as e:
            self.log_test("Empty Todos List", False, "", f"Error: {str(e)}")
            return False
    
    def test_create_todo(self, text: str) -> Optional[Dict]:
        """Test 5: Create todo functionality"""
        try:
            payload = {"text": text}
            headers = {"Content-Type": "application/json"}
            
            response = requests.post(
                f"{self.backend_url}/todos",
                json=payload,
                headers=headers,
                timeout=5
            )
            
            if response.status_code == 201:
                todo = response.json()
                if todo.get('text') == text and 'id' in todo:
                    self.todos_created.append(todo['id'])
                    self.log_test("Create Todo", True, f"Created todo: '{text}' with ID: {todo['id']}")
                    return todo
                else:
                    self.log_test("Create Todo", False, "", "Invalid todo response format")
                    return None
            else:
                self.log_test("Create Todo", False, "", f"Create failed: {response.status_code}")
                return None
        except Exception as e:
            self.log_test("Create Todo", False, "", f"Error: {str(e)}")
            return None
    
    def test_read_todos(self, expected_count: int = None) -> List[Dict]:
        """Test 6: Read todos functionality"""
        try:
            response = requests.get(f"{self.backend_url}/todos", timeout=5)
            if response.status_code == 200:
                todos = response.json()
                if isinstance(todos, list):
                    count_msg = f"Retrieved {len(todos)} todos"
                    if expected_count is not None:
                        if len(todos) == expected_count:
                            count_msg += f" (expected {expected_count})"
                        else:
                            self.log_test("Read Todos", False, "", f"Expected {expected_count} todos, got {len(todos)}")
                            return []
                    
                    self.log_test("Read Todos", True, count_msg)
                    return todos
                else:
                    self.log_test("Read Todos", False, "", "Response is not a list")
                    return []
            else:
                self.log_test("Read Todos", False, "", f"Read failed: {response.status_code}")
                return []
        except Exception as e:
            self.log_test("Read Todos", False, "", f"Error: {str(e)}")
            return []
    
    def test_update_todo(self, todo_id: str, completed: bool) -> bool:
        """Test 7: Update todo completion status"""
        try:
            payload = {"completed": completed}
            headers = {"Content-Type": "application/json"}
            
            response = requests.put(
                f"{self.backend_url}/todos/{todo_id}",
                json=payload,
                headers=headers,
                timeout=5
            )
            
            if response.status_code == 200:
                todo = response.json()
                if todo.get('completed') == completed:
                    status = "completed" if completed else "incomplete"
                    self.log_test("Update Todo", True, f"Todo {todo_id} marked as {status}")
                    return True
                else:
                    self.log_test("Update Todo", False, "", "Todo completion status not updated correctly")
                    return False
            else:
                self.log_test("Update Todo", False, "", f"Update failed: {response.status_code}")
                return False
        except Exception as e:
            self.log_test("Update Todo", False, "", f"Error: {str(e)}")
            return False
    
    def test_delete_todo(self, todo_id: str) -> bool:
        """Test 8: Delete todo functionality"""
        try:
            response = requests.delete(f"{self.backend_url}/todos/{todo_id}", timeout=5)
            
            if response.status_code == 200:
                self.log_test("Delete Todo", True, f"Successfully deleted todo {todo_id}")
                if todo_id in self.todos_created:
                    self.todos_created.remove(todo_id)
                return True
            elif response.status_code == 404:
                self.log_test("Delete Todo", False, "", f"Todo {todo_id} not found for deletion")
                return False
            else:
                self.log_test("Delete Todo", False, "", f"Delete failed: {response.status_code}")
                return False
        except Exception as e:
            self.log_test("Delete Todo", False, "", f"Error: {str(e)}")
            return False
    
    def test_error_handling(self) -> bool:
        """Test 9: Error handling for invalid requests"""
        error_tests_passed = 0
        total_error_tests = 4
        
        # Test 9a: Create todo with empty text
        try:
            response = requests.post(
                f"{self.backend_url}/todos",
                json={"text": ""},
                headers={"Content-Type": "application/json"},
                timeout=5
            )
            if response.status_code == 400:
                error_tests_passed += 1
        except:
            pass
        
        # Test 9b: Get non-existent todo
        try:
            response = requests.get(f"{self.backend_url}/todos/nonexistent-id", timeout=5)
            if response.status_code == 404:
                error_tests_passed += 1
        except:
            pass
        
        # Test 9c: Update non-existent todo
        try:
            response = requests.put(
                f"{self.backend_url}/todos/nonexistent-id",
                json={"completed": True},
                headers={"Content-Type": "application/json"},
                timeout=5
            )
            if response.status_code == 404:
                error_tests_passed += 1
        except:
            pass
        
        # Test 9d: Delete non-existent todo
        try:
            response = requests.delete(f"{self.backend_url}/todos/nonexistent-id", timeout=5)
            if response.status_code == 404:
                error_tests_passed += 1
        except:
            pass
        
        success = error_tests_passed == total_error_tests
        self.log_test(
            "Error Handling", 
            success, 
            f"Passed {error_tests_passed}/{total_error_tests} error handling tests"
        )
        return success
    
    def test_data_persistence(self) -> bool:
        """Test 10: Data persistence across requests"""
        try:
            # Create a todo
            todo = self.test_create_todo("Persistence test todo")
            if not todo:
                self.log_test("Data Persistence", False, "", "Failed to create test todo")
                return False
            
            todo_id = todo['id']
            
            # Wait a moment
            time.sleep(0.1)
            
            # Retrieve todos and verify it exists
            todos = self.test_read_todos()
            found_todo = next((t for t in todos if t['id'] == todo_id), None)
            
            if found_todo:
                # Update the todo
                if self.test_update_todo(todo_id, True):
                    # Retrieve again and verify update persisted
                    todos = self.test_read_todos()
                    updated_todo = next((t for t in todos if t['id'] == todo_id), None)
                    
                    if updated_todo and updated_todo.get('completed') is True:
                        # Clean up
                        self.test_delete_todo(todo_id)
                        self.log_test("Data Persistence", True, "Data persists correctly across CRUD operations")
                        return True
                    else:
                        self.log_test("Data Persistence", False, "", "Update did not persist")
                        return False
                else:
                    self.log_test("Data Persistence", False, "", "Failed to update todo")
                    return False
            else:
                self.log_test("Data Persistence", False, "", "Created todo not found in subsequent read")
                return False
                
        except Exception as e:
            self.log_test("Data Persistence", False, "", f"Error: {str(e)}")
            return False
    
    def test_concurrent_operations(self) -> bool:
        """Test 11: Multiple concurrent operations"""
        try:
            # Create multiple todos quickly
            todo_texts = ["Concurrent test 1", "Concurrent test 2", "Concurrent test 3"]
            created_todos = []
            
            for text in todo_texts:
                todo = self.test_create_todo(text)
                if todo:
                    created_todos.append(todo)
                else:
                    self.log_test("Concurrent Operations", False, "", f"Failed to create todo: {text}")
                    return False
            
            if len(created_todos) == len(todo_texts):
                # Verify all todos exist
                todos = self.test_read_todos()
                found_count = sum(1 for t in todos if t['id'] in [ct['id'] for ct in created_todos])
                
                if found_count == len(created_todos):
                    # Clean up
                    for todo in created_todos:
                        self.test_delete_todo(todo['id'])
                    
                    self.log_test("Concurrent Operations", True, f"Successfully handled {len(created_todos)} concurrent operations")
                    return True
                else:
                    self.log_test("Concurrent Operations", False, "", f"Only found {found_count}/{len(created_todos)} todos")
                    return False
            else:
                self.log_test("Concurrent Operations", False, "", "Failed to create all concurrent todos")
                return False
                
        except Exception as e:
            self.log_test("Concurrent Operations", False, "", f"Error: {str(e)}")
            return False
    
    def test_complete_user_workflow(self) -> bool:
        """Test 12: Complete user workflow simulation"""
        try:
            # Simulate complete user workflow
            workflow_steps = []
            
            # Step 1: Start with empty list
            initial_todos = self.test_read_todos(0)
            workflow_steps.append("Retrieved initial empty list")
            
            # Step 2: Create first todo
            todo1 = self.test_create_todo("Buy groceries")
            if not todo1:
                self.log_test("User Workflow", False, "", "Failed at step 2: Create first todo")
                return False
            workflow_steps.append("Created first todo")
            
            # Step 3: Create second todo
            todo2 = self.test_create_todo("Walk the dog")
            if not todo2:
                self.log_test("User Workflow", False, "", "Failed at step 3: Create second todo")
                return False
            workflow_steps.append("Created second todo")
            
            # Step 4: List todos (should have 2)
            todos = self.test_read_todos(2)
            if len(todos) != 2:
                self.log_test("User Workflow", False, "", f"Expected 2 todos, found {len(todos)}")
                return False
            workflow_steps.append("Listed todos (2 found)")
            
            # Step 5: Complete first todo
            if not self.test_update_todo(todo1['id'], True):
                self.log_test("User Workflow", False, "", "Failed at step 5: Complete first todo")
                return False
            workflow_steps.append("Completed first todo")
            
            # Step 6: Verify completion
            todos = self.test_read_todos(2)
            completed_todo = next((t for t in todos if t['id'] == todo1['id']), None)
            if not completed_todo or not completed_todo.get('completed'):
                self.log_test("User Workflow", False, "", "First todo not marked as completed")
                return False
            workflow_steps.append("Verified todo completion")
            
            # Step 7: Delete completed todo
            if not self.test_delete_todo(todo1['id']):
                self.log_test("User Workflow", False, "", "Failed at step 7: Delete completed todo")
                return False
            workflow_steps.append("Deleted completed todo")
            
            # Step 8: Verify only one todo remains
            final_todos = self.test_read_todos(1)
            if len(final_todos) != 1 or final_todos[0]['id'] != todo2['id']:
                self.log_test("User Workflow", False, "", "Incorrect final state")
                return False
            workflow_steps.append("Verified final state")
            
            # Clean up remaining todo
            self.test_delete_todo(todo2['id'])
            
            self.log_test("User Workflow", True, f"Completed workflow: {' → '.join(workflow_steps)}")
            return True
            
        except Exception as e:
            self.log_test("User Workflow", False, "", f"Error: {str(e)}")
            return False
    
    def cleanup_remaining_todos(self):
        """Clean up any remaining test todos"""
        for todo_id in self.todos_created[:]:
            try:
                self.test_delete_todo(todo_id)
            except:
                pass  # Ignore cleanup errors
    
    def run_all_tests(self) -> Tuple[int, int]:
        """Run complete integration test suite"""
        print("=" * 60)
        print("TODO APPLICATION - INTEGRATION TEST SUITE")
        print("=" * 60)
        print(f"Backend URL: {self.backend_url}")
        print(f"Frontend URL: {self.frontend_url}")
        print(f"Test started: {datetime.now().isoformat()}")
        print("=" * 60)
        
        # Core connectivity tests
        if not self.test_backend_connectivity():
            print("\n❌ Backend not available - stopping tests")
            return 0, 1
        
        if not self.test_frontend_connectivity():
            print("\n⚠️  Frontend not available - continuing with backend tests only")
        
        # Run all integration tests
        self.test_cors_configuration()
        self.test_empty_todos_list()
        
        # CRUD operation tests
        self.test_create_todo("Test todo 1")
        self.test_read_todos()
        
        if self.todos_created:
            self.test_update_todo(self.todos_created[0], True)
            self.test_delete_todo(self.todos_created[0])
        
        # Advanced integration tests
        self.test_error_handling()
        self.test_data_persistence()
        self.test_concurrent_operations()
        self.test_complete_user_workflow()
        
        # Cleanup
        self.cleanup_remaining_todos()
        
        # Generate summary
        passed = sum(1 for result in self.test_results if result['passed'])
        total = len(self.test_results)
        
        print("\n" + "=" * 60)
        print("TEST SUMMARY")
        print("=" * 60)
        print(f"Total tests: {total}")
        print(f"Passed: {passed}")
        print(f"Failed: {total - passed}")
        print(f"Success rate: {(passed/total)*100:.1f}%")
        
        if passed == total:
            print("🎉 ALL TESTS PASSED - Application ready for production!")
        else:
            print("⚠️  Some tests failed - review results above")
        
        return passed, total
    
    def generate_json_report(self, output_file: str):
        """Generate JSON test report"""
        report = {
            "test_suite": "Todo Application Integration Tests",
            "backend_url": self.backend_url,
            "frontend_url": self.frontend_url,
            "test_timestamp": datetime.now().isoformat(),
            "total_tests": len(self.test_results),
            "passed_tests": sum(1 for r in self.test_results if r['passed']),
            "failed_tests": sum(1 for r in self.test_results if not r['passed']),
            "success_rate": (sum(1 for r in self.test_results if r['passed']) / len(self.test_results)) * 100 if self.test_results else 0,
            "test_results": self.test_results
        }
        
        with open(output_file, 'w') as f:
            json.dump(report, f, indent=2)
        
        print(f"\nDetailed test report saved to: {output_file}")

def main():
    """Main test runner"""
    # Parse command line arguments for custom URLs if needed
    backend_url = os.getenv('BACKEND_URL', 'http://localhost:5000')
    frontend_url = os.getenv('FRONTEND_URL', 'http://localhost:3000')
    
    if len(sys.argv) > 1:
        backend_url = sys.argv[1]
    if len(sys.argv) > 2:
        frontend_url = sys.argv[2]
    
    # Run integration tests
    tester = TodoIntegrationTester(backend_url, frontend_url)
    passed, total = tester.run_all_tests()
    
    # Generate JSON report
    report_file = "/Users/viorel/workspace/test_claude/agentic_flow/logs/tests/20_integration_test_results.json"
    tester.generate_json_report(report_file)
    
    # Exit with appropriate code
    sys.exit(0 if passed == total else 1)

if __name__ == "__main__":
    main()