#!/usr/bin/env python3
"""
Test script for error handling and validation enhancements
Tests the enhanced error handling, toast notifications, and offline features
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

def test_error_handling_enhancements():
    print("=== Testing Error Handling and Validation Enhancements ===\n")
    
    # Test 1: React component compilation
    print("1. Testing React component compilation...")
    try:
        result = subprocess.run(['npm', 'run', 'build'], 
                              capture_output=True, text=True, timeout=60)
        passed = result.returncode == 0
        if passed:
            print_test("React compilation", True, "Production build successful")
        else:
            print_test("React compilation", False, f"Build failed: {result.stderr[:200]}")
    except subprocess.TimeoutExpired:
        print_test("React compilation", False, "Build timeout after 60 seconds")
    except Exception as e:
        print_test("React compilation", False, f"Build error: {e}")
    
    # Test 2: Backend API error responses
    print("2. Testing enhanced backend error responses...")
    try:
        # Test with empty todo creation
        response = requests.post(f'{BACKEND_URL}/todos',
                               json={'text': '   '},
                               headers=HEADERS)
        passed = response.status_code == 400
        if passed:
            error_data = response.json()
            has_error_field = 'error' in error_data
            clear_message = 'empty' in error_data.get('error', '').lower()
            passed = has_error_field and clear_message
        
        print_test("Enhanced error responses", passed,
                  f"Status: {response.status_code}, Error format: {response.json() if response.status_code == 400 else 'N/A'}")
    except Exception as e:
        print_test("Enhanced error responses", False, f"Error: {e}")
    
    # Test 3: API endpoint validation improvements
    print("3. Testing API validation improvements...")
    test_cases = [
        ({'text': ''}, 400, "empty text"),
        ({'text': 'x' * 201}, 400, "text too long"),
        ({'completed': 'not-boolean'}, 400, "invalid boolean"),
        ({'text': 'Valid todo'}, 201, "valid creation")
    ]
    
    passed_validations = 0
    for i, (data, expected_status, description) in enumerate(test_cases):
        try:
            if 'completed' in data:
                # Test PUT request for boolean validation
                response = requests.put(f'{BACKEND_URL}/todos/1',
                                      json=data, headers=HEADERS)
            else:
                # Test POST request
                response = requests.post(f'{BACKEND_URL}/todos',
                                       json=data, headers=HEADERS)
            
            if response.status_code == expected_status:
                passed_validations += 1
                print(f"    ✅ {description}: HTTP {response.status_code}")
            else:
                print(f"    ❌ {description}: Expected {expected_status}, got {response.status_code}")
        except Exception as e:
            print(f"    ❌ {description}: Error {e}")
    
    print_test("API validation improvements", passed_validations == len(test_cases),
              f"Passed {passed_validations}/{len(test_cases)} validation tests")
    
    # Test 4: CORS and error handling integration
    print("4. Testing CORS with error scenarios...")
    try:
        # Test CORS with error response
        response = requests.post(f'{BACKEND_URL}/todos',
                               json={'text': ''},
                               headers={**HEADERS, 'Origin': FRONTEND_URL})
        
        cors_header = response.headers.get('Access-Control-Allow-Origin')
        error_response = response.status_code == 400
        passed = cors_header is not None and error_response
        
        print_test("CORS error handling", passed,
                  f"CORS header present: {cors_header is not None}, Error status: {error_response}")
    except Exception as e:
        print_test("CORS error handling", False, f"Error: {e}")
    
    # Test 5: Component structure validation
    print("5. Testing new component structure...")
    component_files = [
        'src/components/Toast.js',
        'src/hooks/useToast.js',
        'src/hooks/useNetworkStatus.js'
    ]
    
    existing_components = 0
    for component in component_files:
        try:
            with open(component, 'r') as f:
                content = f.read()
                if len(content) > 100:  # Basic content check
                    existing_components += 1
                    print(f"    ✅ {component}: Found ({len(content)} chars)")
                else:
                    print(f"    ❌ {component}: Too small or empty")
        except FileNotFoundError:
            print(f"    ❌ {component}: Not found")
        except Exception as e:
            print(f"    ❌ {component}: Error reading - {e}")
    
    print_test("Component structure", existing_components == len(component_files),
              f"Found {existing_components}/{len(component_files)} required components")
    
    # Test 6: CSS enhancements validation
    print("6. Testing CSS enhancements...")
    try:
        with open('src/App.css', 'r') as f:
            css_content = f.read()
            
            # Check for new CSS classes
            required_classes = [
                'toast-container',
                'loading-spinner',
                'offline-indicator',
                'retry-button',
                'offline-warning'
            ]
            
            found_classes = 0
            for css_class in required_classes:
                if css_class in css_content:
                    found_classes += 1
                    print(f"    ✅ .{css_class}: Found")
                else:
                    print(f"    ❌ .{css_class}: Missing")
            
            print_test("CSS enhancements", found_classes == len(required_classes),
                      f"Found {found_classes}/{len(required_classes)} required CSS classes")
    except Exception as e:
        print_test("CSS enhancements", False, f"Error reading CSS: {e}")
    
    # Test 7: Error handling flow simulation
    print("7. Testing error handling flow...")
    try:
        # Create a todo for testing
        create_response = requests.post(f'{BACKEND_URL}/todos',
                                      json={'text': 'Test error handling'},
                                      headers=HEADERS)
        
        if create_response.status_code == 201:
            todo_id = create_response.json()['id']
            
            # Test update with invalid data
            error_response = requests.put(f'{BACKEND_URL}/todos/{todo_id}',
                                        json={'completed': 'invalid'},
                                        headers=HEADERS)
            
            # Test delete non-existent
            not_found_response = requests.delete(f'{BACKEND_URL}/todos/99999')
            
            error_handling_works = (
                error_response.status_code == 400 and
                not_found_response.status_code == 404
            )
            
            print_test("Error handling flow", error_handling_works,
                      f"Invalid update: {error_response.status_code}, Missing delete: {not_found_response.status_code}")
            
            # Cleanup
            requests.delete(f'{BACKEND_URL}/todos/{todo_id}')
        else:
            print_test("Error handling flow", False, "Could not create test todo")
    except Exception as e:
        print_test("Error handling flow", False, f"Error: {e}")
    
    # Test 8: Frontend build size validation
    print("8. Testing frontend build optimization...")
    try:
        import os
        build_path = 'build/static/js'
        if os.path.exists(build_path):
            js_files = [f for f in os.listdir(build_path) if f.endswith('.js')]
            if js_files:
                # Check main bundle size (should be reasonable)
                main_file = max(js_files, key=lambda f: os.path.getsize(os.path.join(build_path, f)))
                size_kb = os.path.getsize(os.path.join(build_path, main_file)) / 1024
                
                # Reasonable size check (under 500KB for main bundle)
                size_ok = size_kb < 500
                print_test("Build optimization", size_ok,
                          f"Main bundle: {main_file} ({size_kb:.1f}KB)")
            else:
                print_test("Build optimization", False, "No JS files in build")
        else:
            print_test("Build optimization", False, "Build directory not found")
    except Exception as e:
        print_test("Build optimization", False, f"Error: {e}")
    
    # Final summary
    print("\n" + "="*60)
    print("Error Handling Enhancement Test Summary:")
    print(f"    Backend API: {BACKEND_URL}")
    print(f"    Components: Toast, Network Status, Enhanced Validation")
    print(f"    Features: Offline Mode, Retry Logic, Loading States")
    print("="*60)
    
    return True

def main():
    print("Error Handling and Validation Enhancement Test")
    print("="*50)
    
    # Check if backend is running
    print("Checking backend server...")
    if not wait_for_server(f"{BACKEND_URL}/health", timeout=5):
        print("❌ Backend server not accessible")
        print("   Please start: cd backend && python app.py")
        return 1
    
    print("✅ Backend server is running")
    print()
    
    # Run enhancement tests
    try:
        success = test_error_handling_enhancements()
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