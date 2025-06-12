#!/usr/bin/env python3
"""
Test harness for Task 16: TodoForm Component
Tests the TodoForm React component implementation
"""

import os
import json
import re
from pathlib import Path

def test_todo_form_component():
    """Test TodoForm component implementation"""
    results = {
        'task_id': '16',
        'task_name': 'todo_form_component',
        'timestamp': '2025-01-23',
        'tests': []
    }
    
    component_file_path = '/Users/viorel/workspace/test_claude/frontend/src/components/TodoForm.js'
    
    # Test 1: Component file exists
    test_1 = {
        'name': 'component_file_exists',
        'description': 'TodoForm component file exists at correct location',
        'status': 'fail',
        'details': ''
    }
    
    if os.path.exists(component_file_path):
        test_1['status'] = 'pass'
        test_1['details'] = 'TodoForm component found at frontend/src/components/TodoForm.js'
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
    
    required_imports = ['React', 'useState']
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
    
    # Test 3: Props interface
    test_3 = {
        'name': 'props_interface',
        'description': 'Component accepts onAddTodo prop',
        'status': 'fail',
        'details': ''
    }
    
    props_pattern = r'function TodoForm\(\s*\{\s*onAddTodo\s*\}'
    if re.search(props_pattern, component_content):
        test_3['status'] = 'pass'
        test_3['details'] = 'Props interface correctly defined: onAddTodo'
    else:
        test_3['details'] = 'Props interface not found or incorrect'
    
    results['tests'].append(test_3)
    
    # Test 4: Form state management
    test_4 = {
        'name': 'form_state_management',
        'description': 'Form state with inputValue, isSubmitting, error',
        'status': 'fail',
        'details': ''
    }
    
    state_patterns = ['inputValue', 'isSubmitting', 'error', 'useState']
    found_states = [pattern for pattern in state_patterns if pattern in component_content]
    
    if len(found_states) >= 3:
        test_4['status'] = 'pass'
        test_4['details'] = f'Form state management found: {", ".join(found_states)}'
    else:
        test_4['details'] = f'Insufficient form state management. Found: {found_states}'
    
    results['tests'].append(test_4)
    
    # Test 5: Form validation
    test_5 = {
        'name': 'form_validation',
        'description': 'Input validation for empty text and character limits',
        'status': 'fail',
        'details': ''
    }
    
    validation_patterns = ['trim()', 'length', 'Please enter', 'characters']
    found_validation = [pattern for pattern in validation_patterns if pattern in component_content]
    
    if len(found_validation) >= 3:
        test_5['status'] = 'pass'
        test_5['details'] = f'Form validation patterns found: {", ".join(found_validation)}'
    else:
        test_5['details'] = f'Insufficient form validation. Found: {found_validation}'
    
    results['tests'].append(test_5)
    
    # Test 6: Form submission
    test_6 = {
        'name': 'form_submission',
        'description': 'Form submission handling with onSubmit',
        'status': 'fail',
        'details': ''
    }
    
    submission_patterns = ['onSubmit', 'handleSubmit', 'preventDefault', 'onAddTodo']
    found_submission = [pattern for pattern in submission_patterns if pattern in component_content]
    
    if len(found_submission) >= 3:
        test_6['status'] = 'pass'
        test_6['details'] = f'Form submission patterns found: {", ".join(found_submission)}'
    else:
        test_6['details'] = f'Insufficient form submission handling. Found: {found_submission}'
    
    results['tests'].append(test_6)
    
    # Test 7: Keyboard support
    test_7 = {
        'name': 'keyboard_support',
        'description': 'Enter key submission support',
        'status': 'fail',
        'details': ''
    }
    
    if 'onKeyPress' in component_content and 'Enter' in component_content:
        test_7['status'] = 'pass'
        test_7['details'] = 'Enter key submission support found'
    else:
        test_7['details'] = 'Keyboard support not found or incomplete'
    
    results['tests'].append(test_7)
    
    # Test 8: Error handling
    test_8 = {
        'name': 'error_handling',
        'description': 'Error states and user feedback',
        'status': 'fail',
        'details': ''
    }
    
    error_patterns = ['try', 'catch', 'setError', 'error-message']
    found_errors = [pattern for pattern in error_patterns if pattern in component_content]
    
    if len(found_errors) >= 3:
        test_8['status'] = 'pass'
        test_8['details'] = f'Error handling patterns found: {", ".join(found_errors)}'
    else:
        test_8['details'] = f'Insufficient error handling. Found: {found_errors}'
    
    results['tests'].append(test_8)
    
    # Test 9: Loading states
    test_9 = {
        'name': 'loading_states',
        'description': 'Loading indicators and disabled states',
        'status': 'fail',
        'details': ''
    }
    
    if 'isSubmitting' in component_content and 'disabled' in component_content and '⏳' in component_content:
        test_9['status'] = 'pass'
        test_9['details'] = 'Loading states with visual indicators found'
    else:
        test_9['details'] = 'Loading state implementation not found or incomplete'
    
    results['tests'].append(test_9)
    
    # Test 10: Form elements
    test_10 = {
        'name': 'form_elements',
        'description': 'Proper form, input, and button elements',
        'status': 'fail',
        'details': ''
    }
    
    element_patterns = ['<form', '<input', '<button', 'type="submit"']
    found_elements = [pattern for pattern in element_patterns if pattern in component_content]
    
    if len(found_elements) >= 3:
        test_10['status'] = 'pass'
        test_10['details'] = f'Form elements found: {", ".join(found_elements)}'
    else:
        test_10['details'] = f'Insufficient form elements. Found: {found_elements}'
    
    results['tests'].append(test_10)
    
    # Test 11: User experience features
    test_11 = {
        'name': 'user_experience',
        'description': 'UX features like placeholder, autofocus, character counter',
        'status': 'fail',
        'details': ''
    }
    
    ux_patterns = ['placeholder', 'autoFocus', 'maxLength', 'characters']
    found_ux = [pattern for pattern in ux_patterns if pattern in component_content]
    
    if len(found_ux) >= 3:
        test_11['status'] = 'pass'
        test_11['details'] = f'UX features found: {", ".join(found_ux)}'
    else:
        test_11['details'] = f'Insufficient UX features. Found: {found_ux}'
    
    results['tests'].append(test_11)
    
    # Test 12: Component export
    test_12 = {
        'name': 'component_export',
        'description': 'Component properly exported as default',
        'status': 'fail',
        'details': ''
    }
    
    if 'export default TodoForm' in component_content:
        test_12['status'] = 'pass'
        test_12['details'] = 'Component exported as default'
    else:
        test_12['details'] = 'Default export not found'
    
    results['tests'].append(test_12)
    
    # Test 13: JSDoc documentation
    test_13 = {
        'name': 'jsdoc_documentation',
        'description': 'JSDoc documentation for component and functions',
        'status': 'fail',
        'details': ''
    }
    
    jsdoc_patterns = ['/**', '@param', 'TodoForm Component']
    found_docs = [pattern for pattern in jsdoc_patterns if pattern in component_content]
    
    if len(found_docs) >= 2:
        test_13['status'] = 'pass'
        test_13['details'] = f'JSDoc documentation found: {", ".join(found_docs)}'
    else:
        test_13['details'] = f'Insufficient JSDoc documentation. Found: {found_docs}'
    
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
    results = test_todo_form_component()
    print(f"Task 16 TodoForm Component Tests: {results['summary']['passed_tests']}/{results['summary']['total_tests']} passed")
    
    # Print test details
    for test in results['tests']:
        status_icon = '✅' if test['status'] == 'pass' else '❌'
        print(f"{status_icon} {test['name']}: {test['details']}")
    
    print(f"\\nOverall Success Rate: {results['summary']['success_rate']}")