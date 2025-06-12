#!/usr/bin/env python3
"""
Test harness for Task 15: TodoItem Component
Tests the TodoItem React component implementation
"""

import os
import json
import re
from pathlib import Path

def test_todo_item_component():
    """Test TodoItem component implementation"""
    results = {
        'task_id': '15',
        'task_name': 'todo_item_component',
        'timestamp': '2025-01-23',
        'tests': []
    }
    
    component_file_path = '/Users/viorel/workspace/test_claude/frontend/src/components/TodoItem.js'
    
    # Test 1: Component file exists
    test_1 = {
        'name': 'component_file_exists',
        'description': 'TodoItem component file exists at correct location',
        'status': 'fail',
        'details': ''
    }
    
    if os.path.exists(component_file_path):
        test_1['status'] = 'pass'
        test_1['details'] = 'TodoItem component found at frontend/src/components/TodoItem.js'
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
        'description': 'Component accepts correct props (todo, onToggle, onDelete)',
        'status': 'fail',
        'details': ''
    }
    
    props_pattern = r'function TodoItem\(\s*\{\s*todo,\s*onToggle,\s*onDelete\s*\}'
    if re.search(props_pattern, component_content):
        test_3['status'] = 'pass'
        test_3['details'] = 'Props interface correctly defined: todo, onToggle, onDelete'
    else:
        test_3['details'] = 'Props interface not found or incorrect'
    
    results['tests'].append(test_3)
    
    # Test 4: Local state management
    test_4 = {
        'name': 'local_state_management',
        'description': 'Local state for loading and error states',
        'status': 'fail',
        'details': ''
    }
    
    state_patterns = ['isToggling', 'isDeleting', 'error', 'useState']
    found_states = [pattern for pattern in state_patterns if pattern in component_content]
    
    if len(found_states) >= 3:
        test_4['status'] = 'pass'
        test_4['details'] = f'Local state management found: {", ".join(found_states)}'
    else:
        test_4['details'] = f'Insufficient local state management. Found: {found_states}'
    
    results['tests'].append(test_4)
    
    # Test 5: Action handlers
    test_5 = {
        'name': 'action_handlers',
        'description': 'Toggle and delete action handlers implemented',
        'status': 'fail',
        'details': ''
    }
    
    handler_patterns = ['handleToggle', 'handleDelete', 'onToggle', 'onDelete']
    found_handlers = [pattern for pattern in handler_patterns if pattern in component_content]
    
    if len(found_handlers) >= 3:
        test_5['status'] = 'pass'
        test_5['details'] = f'Action handlers found: {", ".join(found_handlers)}'
    else:
        test_5['details'] = f'Insufficient action handlers. Found: {found_handlers}'
    
    results['tests'].append(test_5)
    
    # Test 6: Error handling
    test_6 = {
        'name': 'error_handling',
        'description': 'Error handling and user feedback',
        'status': 'fail',
        'details': ''
    }
    
    error_patterns = ['try', 'catch', 'setError', 'error-message']
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
        'description': 'Loading indicators for async operations',
        'status': 'fail',
        'details': ''
    }
    
    if 'isToggling' in component_content and 'isDeleting' in component_content and '⏳' in component_content:
        test_7['status'] = 'pass'
        test_7['details'] = 'Loading states with visual indicators found'
    else:
        test_7['details'] = 'Loading state implementation not found or incomplete'
    
    results['tests'].append(test_7)
    
    # Test 8: Confirmation dialog
    test_8 = {
        'name': 'confirmation_dialog',
        'description': 'Delete confirmation for user safety',
        'status': 'fail',
        'details': ''
    }
    
    if 'window.confirm' in component_content or 'confirm(' in component_content:
        test_8['status'] = 'pass'
        test_8['details'] = 'Delete confirmation dialog implemented'
    else:
        test_8['details'] = 'Confirmation dialog not found'
    
    results['tests'].append(test_8)
    
    # Test 9: Accessibility features
    test_9 = {
        'name': 'accessibility_features',
        'description': 'ARIA labels and semantic markup',
        'status': 'fail',
        'details': ''
    }
    
    a11y_patterns = ['aria-label', 'button', 'disabled']
    found_a11y = [pattern for pattern in a11y_patterns if pattern in component_content]
    
    if len(found_a11y) >= 2:
        test_9['status'] = 'pass'
        test_9['details'] = f'Accessibility features found: {", ".join(found_a11y)}'
    else:
        test_9['details'] = f'Insufficient accessibility features. Found: {found_a11y}'
    
    results['tests'].append(test_9)
    
    # Test 10: Component export
    test_10 = {
        'name': 'component_export',
        'description': 'Component properly exported as default',
        'status': 'fail',
        'details': ''
    }
    
    if 'export default TodoItem' in component_content:
        test_10['status'] = 'pass'
        test_10['details'] = 'Component exported as default'
    else:
        test_10['details'] = 'Default export not found'
    
    results['tests'].append(test_10)
    
    # Test 11: JSDoc documentation
    test_11 = {
        'name': 'jsdoc_documentation',
        'description': 'JSDoc documentation for component and props',
        'status': 'fail',
        'details': ''
    }
    
    jsdoc_patterns = ['/**', '@param', 'TodoItem Component']
    found_docs = [pattern for pattern in jsdoc_patterns if pattern in component_content]
    
    if len(found_docs) >= 2:
        test_11['status'] = 'pass'
        test_11['details'] = f'JSDoc documentation found: {", ".join(found_docs)}'
    else:
        test_11['details'] = f'Insufficient JSDoc documentation. Found: {found_docs}'
    
    results['tests'].append(test_11)
    
    # Test 12: Visual indicators
    test_12 = {
        'name': 'visual_indicators',
        'description': 'Visual status indicators for completed/pending',
        'status': 'fail',
        'details': ''
    }
    
    if '✅' in component_content and '⭕' in component_content and 'completed' in component_content:
        test_12['status'] = 'pass'
        test_12['details'] = 'Visual status indicators found (✅/⭕ for completion)'
    else:
        test_12['details'] = 'Visual indicators not found or incomplete'
    
    results['tests'].append(test_12)
    
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
    results = test_todo_item_component()
    print(f"Task 15 TodoItem Component Tests: {results['summary']['passed_tests']}/{results['summary']['total_tests']} passed")
    
    # Print test details
    for test in results['tests']:
        status_icon = '✅' if test['status'] == 'pass' else '❌'
        print(f"{status_icon} {test['name']}: {test['details']}")
    
    print(f"\\nOverall Success Rate: {results['summary']['success_rate']}")