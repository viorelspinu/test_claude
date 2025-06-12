#!/usr/bin/env python3
"""
Test harness for Task 17: App Component Integration
Tests the complete application integration
"""

import os
import json
import re
from pathlib import Path

def test_app_integration():
    """Test App component integration implementation"""
    results = {
        'task_id': '17',
        'task_name': 'app_integration',
        'timestamp': '2025-01-23',
        'tests': []
    }
    
    app_file_path = '/Users/viorel/workspace/test_claude/frontend/src/App.js'
    todo_list_path = '/Users/viorel/workspace/test_claude/frontend/src/components/TodoList.js'
    
    # Test 1: App file exists and updated
    test_1 = {
        'name': 'app_file_updated',
        'description': 'App.js file updated with component integration',
        'status': 'fail',
        'details': ''
    }
    
    if os.path.exists(app_file_path):
        with open(app_file_path, 'r') as f:
            app_content = f.read()
        if 'TodoForm' in app_content and 'TodoList' in app_content:
            test_1['status'] = 'pass'
            test_1['details'] = 'App.js updated with TodoForm and TodoList integration'
        else:
            test_1['details'] = 'App.js exists but missing component imports'
    else:
        test_1['details'] = f'App.js file not found at {app_file_path}'
    
    results['tests'].append(test_1)
    
    # Read App.js content for remaining tests
    app_content = ''
    if os.path.exists(app_file_path):
        with open(app_file_path, 'r') as f:
            app_content = f.read()
    
    # Test 2: React imports and hooks
    test_2 = {
        'name': 'react_imports_hooks',
        'description': 'React, useState, useEffect imported for state management',
        'status': 'fail',
        'details': ''
    }
    
    required_imports = ['React', 'useState', 'useEffect']
    found_imports = []
    
    for imp in required_imports:
        if imp in app_content:
            found_imports.append(imp)
    
    if len(found_imports) == len(required_imports):
        test_2['status'] = 'pass'
        test_2['details'] = f'All React imports found: {", ".join(found_imports)}'
    else:
        missing = [imp for imp in required_imports if imp not in found_imports]
        test_2['details'] = f'Missing imports: {missing}'
    
    results['tests'].append(test_2)
    
    # Test 3: Component imports
    test_3 = {
        'name': 'component_imports',
        'description': 'TodoForm and TodoList components imported',
        'status': 'fail',
        'details': ''
    }
    
    component_imports = ['TodoForm', 'TodoList']
    found_components = []
    
    for comp in component_imports:
        if f'import {comp}' in app_content or f'from \'./components/{comp}\'' in app_content:
            found_components.append(comp)
    
    if len(found_components) == len(component_imports):
        test_3['status'] = 'pass'
        test_3['details'] = f'All components imported: {", ".join(found_components)}'
    else:
        missing = [comp for comp in component_imports if comp not in found_components]
        test_3['details'] = f'Missing component imports: {missing}'
    
    results['tests'].append(test_3)
    
    # Test 4: API service imports
    test_4 = {
        'name': 'api_service_imports',
        'description': 'API service functions imported for CRUD operations',
        'status': 'fail',
        'details': ''
    }
    
    api_functions = ['getTodos', 'createTodo', 'updateTodo', 'deleteTodo']
    found_api = []
    
    for func in api_functions:
        if func in app_content:
            found_api.append(func)
    
    if len(found_api) >= 3:
        test_4['status'] = 'pass'
        test_4['details'] = f'API functions imported: {", ".join(found_api)}'
    else:
        test_4['details'] = f'Insufficient API imports. Found: {found_api}'
    
    results['tests'].append(test_4)
    
    # Test 5: Global state management
    test_5 = {
        'name': 'global_state_management',
        'description': 'Global state with todos, loading, error',
        'status': 'fail',
        'details': ''
    }
    
    state_patterns = ['useState.*todos', 'useState.*loading', 'useState.*error']
    found_states = []
    
    for pattern in state_patterns:
        if re.search(pattern, app_content):
            found_states.append(pattern.split('.*')[1])
    
    if len(found_states) >= 3:
        test_5['status'] = 'pass'
        test_5['details'] = f'Global state management found: {", ".join(found_states)}'
    else:
        test_5['details'] = f'Insufficient global state. Found: {found_states}'
    
    results['tests'].append(test_5)
    
    # Test 6: CRUD operation handlers
    test_6 = {
        'name': 'crud_handlers',
        'description': 'Action handlers for all CRUD operations',
        'status': 'fail',
        'details': ''
    }
    
    handler_patterns = ['handleAddTodo', 'handleToggleTodo', 'handleDeleteTodo', 'loadTodos']
    found_handlers = [pattern for pattern in handler_patterns if pattern in app_content]
    
    if len(found_handlers) >= 3:
        test_6['status'] = 'pass'
        test_6['details'] = f'CRUD handlers found: {", ".join(found_handlers)}'
    else:
        test_6['details'] = f'Insufficient CRUD handlers. Found: {found_handlers}'
    
    results['tests'].append(test_6)
    
    # Test 7: Component rendering
    test_7 = {
        'name': 'component_rendering',
        'description': 'TodoForm and TodoList rendered in App',
        'status': 'fail',
        'details': ''
    }
    
    if '<TodoForm' in app_content and '<TodoList' in app_content:
        test_7['status'] = 'pass'
        test_7['details'] = 'TodoForm and TodoList components rendered in App'
    else:
        test_7['details'] = 'Component rendering not found or incomplete'
    
    results['tests'].append(test_7)
    
    # Test 8: Props passing
    test_8 = {
        'name': 'props_passing',
        'description': 'Props passed correctly to components',
        'status': 'fail',
        'details': ''
    }
    
    props_patterns = ['onAddTodo', 'todos=', 'onToggle', 'onDelete']
    found_props = [pattern for pattern in props_patterns if pattern in app_content]
    
    if len(found_props) >= 3:
        test_8['status'] = 'pass'
        test_8['details'] = f'Props passing found: {", ".join(found_props)}'
    else:
        test_8['details'] = f'Insufficient props passing. Found: {found_props}'
    
    results['tests'].append(test_8)
    
    # Test 9: Error handling
    test_9 = {
        'name': 'error_handling',
        'description': 'Error handling and retry functionality',
        'status': 'fail',
        'details': ''
    }
    
    error_patterns = ['try', 'catch', 'setError', 'retryLoad']
    found_errors = [pattern for pattern in error_patterns if pattern in app_content]
    
    if len(found_errors) >= 3:
        test_9['status'] = 'pass'
        test_9['details'] = f'Error handling patterns found: {", ".join(found_errors)}'
    else:
        test_9['details'] = f'Insufficient error handling. Found: {found_errors}'
    
    results['tests'].append(test_9)
    
    # Test 10: Loading states
    test_10 = {
        'name': 'loading_states',
        'description': 'Loading states and conditional rendering',
        'status': 'fail',
        'details': ''
    }
    
    if 'loading' in app_content and 'Loading todos' in app_content:
        test_10['status'] = 'pass'
        test_10['details'] = 'Loading states and conditional rendering found'
    else:
        test_10['details'] = 'Loading state implementation not found'
    
    results['tests'].append(test_10)
    
    # Test 11: TodoList refactor verification
    test_11 = {
        'name': 'todolist_refactor',
        'description': 'TodoList refactored to use props and TodoItem',
        'status': 'fail',
        'details': ''
    }
    
    if os.path.exists(todo_list_path):
        with open(todo_list_path, 'r') as f:
            todolist_content = f.read()
        
        props_check = 'todos, onToggle, onDelete' in todolist_content
        todoitem_check = 'TodoItem' in todolist_content
        
        if props_check and todoitem_check:
            test_11['status'] = 'pass'
            test_11['details'] = 'TodoList refactored with props and TodoItem integration'
        else:
            test_11['details'] = f'TodoList refactor incomplete. Props: {props_check}, TodoItem: {todoitem_check}'
    else:
        test_11['details'] = 'TodoList.js file not found'
    
    results['tests'].append(test_11)
    
    # Test 12: Application structure
    test_12 = {
        'name': 'application_structure',
        'description': 'Proper application layout with header, main, footer',
        'status': 'fail',
        'details': ''
    }
    
    structure_patterns = ['<header', '<main', '<footer', 'Todo Application']
    found_structure = [pattern for pattern in structure_patterns if pattern in app_content]
    
    if len(found_structure) >= 3:
        test_12['status'] = 'pass'
        test_12['details'] = f'Application structure found: {", ".join(found_structure)}'
    else:
        test_12['details'] = f'Insufficient application structure. Found: {found_structure}'
    
    results['tests'].append(test_12)
    
    # Test 13: useEffect for initialization
    test_13 = {
        'name': 'initialization_effect',
        'description': 'useEffect for loading todos on app initialization',
        'status': 'fail',
        'details': ''
    }
    
    if 'useEffect' in app_content and 'loadTodos' in app_content and '[]' in app_content:
        test_13['status'] = 'pass'
        test_13['details'] = 'useEffect initialization found'
    else:
        test_13['details'] = 'useEffect initialization not found or incomplete'
    
    results['tests'].append(test_13)
    
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
    results = test_app_integration()
    print(f"Task 17 App Integration Tests: {results['summary']['passed_tests']}/{results['summary']['total_tests']} passed")
    
    # Print test details
    for test in results['tests']:
        status_icon = '✅' if test['status'] == 'pass' else '❌'
        print(f"{status_icon} {test['name']}: {test['details']}")
    
    print(f"\\nOverall Success Rate: {results['summary']['success_rate']}")