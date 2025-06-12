#!/usr/bin/env python3
"""
Test harness for Task 13: API Service Layer
Tests the frontend API service implementation
"""

import os
import json
import re
from pathlib import Path

def test_api_service_implementation():
    """Test API service layer implementation"""
    results = {
        'task_id': '13',
        'task_name': 'api_service',
        'timestamp': '2025-01-23',
        'tests': []
    }
    
    api_file_path = '/Users/viorel/workspace/test_claude/frontend/src/services/api.js'
    
    # Test 1: API file exists
    test_1 = {
        'name': 'api_file_exists',
        'description': 'API service file exists at correct location',
        'status': 'fail',
        'details': ''
    }
    
    if os.path.exists(api_file_path):
        test_1['status'] = 'pass'
        test_1['details'] = 'API service file found at frontend/src/services/api.js'
    else:
        test_1['details'] = f'API service file not found at {api_file_path}'
    
    results['tests'].append(test_1)
    
    # Read API file content for remaining tests
    api_content = ''
    if os.path.exists(api_file_path):
        with open(api_file_path, 'r') as f:
            api_content = f.read()
    
    # Test 2: Required function exports
    test_2 = {
        'name': 'function_exports',
        'description': 'All required CRUD functions are exported',
        'status': 'fail',
        'details': ''
    }
    
    required_functions = ['getTodos', 'createTodo', 'updateTodo', 'deleteTodo']
    found_functions = []
    missing_functions = []
    
    for func in required_functions:
        if f'export async function {func}' in api_content or f'export function {func}' in api_content:
            found_functions.append(func)
        else:
            missing_functions.append(func)
    
    if len(found_functions) == len(required_functions):
        test_2['status'] = 'pass'
        test_2['details'] = f'All required functions found: {", ".join(found_functions)}'
    else:
        test_2['details'] = f'Found: {found_functions}, Missing: {missing_functions}'
    
    results['tests'].append(test_2)
    
    # Test 3: Base URL configuration
    test_3 = {
        'name': 'base_url_config',
        'description': 'API base URL properly configured',
        'status': 'fail',
        'details': ''
    }
    
    if 'localhost:5000' in api_content and '/api' in api_content:
        test_3['status'] = 'pass'
        test_3['details'] = 'Base URL configured for localhost:5000/api'
    else:
        test_3['details'] = 'Base URL configuration not found or incorrect'
    
    results['tests'].append(test_3)
    
    # Test 4: Content-Type headers
    test_4 = {
        'name': 'content_type_headers',
        'description': 'Content-Type headers properly set',
        'status': 'fail',
        'details': ''
    }
    
    if 'Content-Type' in api_content and 'application/json' in api_content:
        test_4['status'] = 'pass'
        test_4['details'] = 'Content-Type: application/json headers configured'
    else:
        test_4['details'] = 'Content-Type headers not found or incorrect'
    
    results['tests'].append(test_4)
    
    # Test 5: Error handling implementation
    test_5 = {
        'name': 'error_handling',
        'description': 'Comprehensive error handling implemented',
        'status': 'fail',
        'details': ''
    }
    
    error_patterns = ['try', 'catch', 'throw new Error', 'response.ok']
    found_patterns = [pattern for pattern in error_patterns if pattern in api_content]
    
    if len(found_patterns) >= 3:
        test_5['status'] = 'pass'
        test_5['details'] = f'Error handling patterns found: {", ".join(found_patterns)}'
    else:
        test_5['details'] = f'Insufficient error handling. Found: {found_patterns}'
    
    results['tests'].append(test_5)
    
    # Test 6: Input validation
    test_6 = {
        'name': 'input_validation',
        'description': 'Input validation for function parameters',
        'status': 'fail',
        'details': ''
    }
    
    validation_patterns = ['if (!text', 'if (!id', 'trim()', 'throw new Error']
    found_validations = [pattern for pattern in validation_patterns if pattern in api_content]
    
    if len(found_validations) >= 3:
        test_6['status'] = 'pass'
        test_6['details'] = f'Input validation patterns found: {", ".join(found_validations)}'
    else:
        test_6['details'] = f'Insufficient input validation. Found: {found_validations}'
    
    results['tests'].append(test_6)
    
    # Test 7: Async/await pattern
    test_7 = {
        'name': 'async_await_pattern',
        'description': 'Functions use async/await pattern',
        'status': 'fail',
        'details': ''
    }
    
    async_count = api_content.count('async function')
    await_count = api_content.count('await ')
    
    if async_count >= 4 and await_count >= 4:
        test_7['status'] = 'pass'
        test_7['details'] = f'Async/await pattern used ({async_count} async functions, {await_count} await calls)'
    else:
        test_7['details'] = f'Insufficient async/await usage ({async_count} async, {await_count} await)'
    
    results['tests'].append(test_7)
    
    # Test 8: JSDoc documentation
    test_8 = {
        'name': 'jsdoc_documentation',
        'description': 'JSDoc documentation present for functions',
        'status': 'fail',
        'details': ''
    }
    
    jsdoc_patterns = ['/**', '@param', '@returns']
    found_docs = [pattern for pattern in jsdoc_patterns if pattern in api_content]
    jsdoc_count = api_content.count('/**')
    
    if len(found_docs) == 3 and jsdoc_count >= 4:
        test_8['status'] = 'pass'
        test_8['details'] = f'JSDoc documentation found ({jsdoc_count} function docs)'
    else:
        test_8['details'] = f'Insufficient JSDoc documentation. Found: {found_docs}, Count: {jsdoc_count}'
    
    results['tests'].append(test_8)
    
    # Calculate overall results
    passed_tests = len([t for t in results['tests'] if t['status'] == 'pass'])
    total_tests = len(results['tests'])
    results['summary'] = {
        'total_tests': total_tests,
        'passed_tests': passed_tests,
        'failed_tests': total_tests - passed_tests,
        'success_rate': f'{(passed_tests/total_tests)*100:.1f}%'
    }
    
    return results

if __name__ == '__main__':
    results = test_api_service_implementation()
    print(f"Task 13 API Service Tests: {results['summary']['passed_tests']}/{results['summary']['total_tests']} passed")
    
    # Print test details
    for test in results['tests']:
        status_icon = '✅' if test['status'] == 'pass' else '❌'
        print(f"{status_icon} {test['name']}: {test['details']}")
    
    print(f"\\nOverall Success Rate: {results['summary']['success_rate']}")