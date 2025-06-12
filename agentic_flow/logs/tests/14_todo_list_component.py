#!/usr/bin/env python3
"""
Test harness for Task 14: TodoList Component
Tests the TodoList React component implementation
"""

import os
import json
import re
from pathlib import Path

def test_todo_list_component():
    """Test TodoList component implementation"""
    results = {
        'task_id': '14',
        'task_name': 'todo_list_component',
        'timestamp': '2025-01-23',
        'tests': []
    }
    
    component_file_path = '/Users/viorel/workspace/test_claude/frontend/src/components/TodoList.js'
    
    # Test 1: Component file exists
    test_1 = {
        'name': 'component_file_exists',
        'description': 'TodoList component file exists at correct location',
        'status': 'fail',
        'details': ''
    }
    
    if os.path.exists(component_file_path):
        test_1['status'] = 'pass'
        test_1['details'] = 'TodoList component found at frontend/src/components/TodoList.js'
    else:
        test_1['details'] = f'Component file not found at {component_file_path}'
    
    results['tests'].append(test_1)
    
    # Read component file content for remaining tests
    component_content = ''
    if os.path.exists(component_file_path):
        with open(component_file_path, 'r') as f:
            component_content = f.read()
    
    # Test 2: React imports
    test_2 = {
        'name': 'react_imports',
        'description': 'React and hooks properly imported',
        'status': 'fail',
        'details': ''
    }
    
    required_imports = ['React', 'useState', 'useEffect']
    found_imports = []
    
    for imp in required_imports:
        if imp in component_content:
            found_imports.append(imp)
    
    if len(found_imports) == len(required_imports):
        test_2['status'] = 'pass'
        test_2['details'] = f'All React imports found: {", ".join(found_imports)}'
    else:
        missing = [imp for imp in required_imports if imp not in found_imports]
        test_2['details'] = f'Missing imports: {missing}'
    
    results['tests'].append(test_2)
    
    # Test 3: API service import
    test_3 = {
        'name': 'api_service_import',
        'description': 'API service properly imported from Task 13',
        'status': 'fail',
        'details': ''
    }
    
    if 'getTodos' in component_content and '../services/api' in component_content:
        test_3['status'] = 'pass'
        test_3['details'] = 'getTodos imported from API service layer'
    else:
        test_3['details'] = 'API service import not found or incorrect'
    
    results['tests'].append(test_3)
    
    # Test 4: State management hooks
    test_4 = {
        'name': 'state_management',
        'description': 'useState hooks for component state',
        'status': 'fail',
        'details': ''
    }
    
    state_patterns = ['useState.*todos', 'useState.*loading', 'useState.*error']
    found_states = []
    
    for pattern in state_patterns:
        if re.search(pattern, component_content):
            found_states.append(pattern.split('.*')[1])
    
    if len(found_states) >= 3:
        test_4['status'] = 'pass'
        test_4['details'] = f'State management found: {", ".join(found_states)}'
    else:
        test_4['details'] = f'Insufficient state management. Found: {found_states}'
    
    results['tests'].append(test_4)
    
    # Test 5: useEffect for data fetching
    test_5 = {
        'name': 'data_fetching',
        'description': 'useEffect hook for data fetching on mount',
        'status': 'fail',
        'details': ''
    }
    
    if 'useEffect' in component_content and 'getTodos' in component_content and '[]' in component_content:
        test_5['status'] = 'pass'
        test_5['details'] = 'useEffect with getTodos and empty dependency array found'
    else:
        test_5['details'] = 'useEffect data fetching not found or incorrect'
    
    results['tests'].append(test_5)
    
    # Test 6: Error handling
    test_6 = {
        'name': 'error_handling',
        'description': 'Error handling and retry functionality',
        'status': 'fail',
        'details': ''
    }
    
    error_patterns = ['try', 'catch', 'setError', 'handleRetry']
    found_errors = [pattern for pattern in error_patterns if pattern in component_content]
    
    if len(found_errors) >= 3:
        test_6['status'] = 'pass'
        test_6['details'] = f'Error handling patterns found: {", ".join(found_errors)}'
    else:
        test_6['details'] = f'Insufficient error handling. Found: {found_errors}'
    
    results['tests'].append(test_6)
    
    # Test 7: Loading states
    test_7 = {
        'name': 'loading_states',
        'description': 'Loading state management and display',
        'status': 'fail',
        'details': ''
    }
    
    if 'loading' in component_content and 'Loading todos' in component_content and 'setLoading' in component_content:
        test_7['status'] = 'pass'
        test_7['details'] = 'Loading state management and display found'
    else:
        test_7['details'] = 'Loading state implementation not found or incomplete'
    
    results['tests'].append(test_7)
    
    # Test 8: Component export
    test_8 = {
        'name': 'component_export',
        'description': 'Component properly exported as default',
        'status': 'fail',
        'details': ''
    }
    
    if 'export default TodoList' in component_content:
        test_8['status'] = 'pass'
        test_8['details'] = 'Component exported as default'
    else:
        test_8['details'] = 'Default export not found'
    
    results['tests'].append(test_8)
    
    # Test 9: Todo rendering logic
    test_9 = {
        'name': 'todo_rendering',
        'description': 'Todo list rendering and empty state handling',
        'status': 'fail',
        'details': ''
    }
    
    rendering_patterns = ['todos.map', 'todo.text', 'todos.length']
    found_rendering = [pattern for pattern in rendering_patterns if pattern in component_content]
    
    if len(found_rendering) >= 2:
        test_9['status'] = 'pass'
        test_9['details'] = f'Todo rendering patterns found: {", ".join(found_rendering)}'
    else:
        test_9['details'] = f'Insufficient todo rendering. Found: {found_rendering}'
    
    results['tests'].append(test_9)
    
    # Test 10: Component structure
    test_10 = {
        'name': 'component_structure',
        'description': 'Proper React functional component structure',
        'status': 'fail',
        'details': ''
    }
    
    if 'function TodoList' in component_content and 'return (' in component_content:
        test_10['status'] = 'pass'
        test_10['details'] = 'Proper functional component structure found'
    else:
        test_10['details'] = 'Component structure not found or incorrect'
    
    results['tests'].append(test_10)
    
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
    results = test_todo_list_component()
    print(f"Task 14 TodoList Component Tests: {results['summary']['passed_tests']}/{results['summary']['total_tests']} passed")
    
    # Print test details
    for test in results['tests']:
        status_icon = '✅' if test['status'] == 'pass' else '❌'
        print(f"{status_icon} {test['name']}: {test['details']}")
    
    print(f"\\nOverall Success Rate: {results['summary']['success_rate']}")