#!/usr/bin/env python3
"""
Test harness for Task 19: Basic Styling
Tests the CSS styling implementation for TodoList component
"""

import os
import json
import re
from pathlib import Path

def test_basic_styling():
    """Test basic styling implementation"""
    results = {
        'task_id': '19',
        'task_name': 'basic_styling',
        'timestamp': '2025-01-23',
        'tests': []
    }
    
    frontend_path = '/Users/viorel/workspace/test_claude/frontend'
    css_file_path = os.path.join(frontend_path, 'src/components/TodoList.css')
    js_file_path = os.path.join(frontend_path, 'src/components/TodoList.js')
    
    # Test 1: CSS file exists
    test_1 = {
        'name': 'css_file_exists',
        'description': 'TodoList.css file exists at correct location',
        'status': 'fail',
        'details': ''
    }
    
    if os.path.exists(css_file_path):
        test_1['status'] = 'pass'
        test_1['details'] = 'TodoList.css found at frontend/src/components/TodoList.css'
    else:
        test_1['details'] = f'CSS file not found at {css_file_path}'
    
    results['tests'].append(test_1)
    
    # Read CSS file content for remaining tests
    css_content = ''
    if os.path.exists(css_file_path):
        with open(css_file_path, 'r') as f:
            css_content = f.read()
    
    # Test 2: CSS import in component
    test_2 = {
        'name': 'css_import_added',
        'description': 'CSS file properly imported in TodoList component',
        'status': 'fail',
        'details': ''
    }
    
    if os.path.exists(js_file_path):
        with open(js_file_path, 'r') as f:
            js_content = f.read()
        
        if './TodoList.css' in js_content or 'TodoList.css' in js_content:
            test_2['status'] = 'pass'
            test_2['details'] = 'CSS import found in TodoList.js'
        else:
            test_2['details'] = 'CSS import not found in component file'
    else:
        test_2['details'] = 'TodoList.js file not found'
    
    results['tests'].append(test_2)
    
    # Test 3: Main component styling
    test_3 = {
        'name': 'main_component_styling',
        'description': 'Main .todo-list class with container styling',
        'status': 'fail',
        'details': ''
    }
    
    main_selectors = ['.todo-list', 'max-width', 'margin', 'padding', 'background']
    found_selectors = [sel for sel in main_selectors if sel in css_content]
    
    if len(found_selectors) >= 4:
        test_3['status'] = 'pass'
        test_3['details'] = f'Main component styling found: {", ".join(found_selectors)}'
    else:
        test_3['details'] = f'Insufficient main styling. Found: {found_selectors}'
    
    results['tests'].append(test_3)
    
    # Test 4: Typography styling
    test_4 = {
        'name': 'typography_styling',
        'description': 'Typography styles for headers and text',
        'status': 'fail',
        'details': ''
    }
    
    typography_patterns = ['font-size', 'font-weight', 'color', 'h2']
    found_typography = [pattern for pattern in typography_patterns if pattern in css_content]
    
    if len(found_typography) >= 3:
        test_4['status'] = 'pass'
        test_4['details'] = f'Typography styling found: {", ".join(found_typography)}'
    else:
        test_4['details'] = f'Insufficient typography styling. Found: {found_typography}'
    
    results['tests'].append(test_4)
    
    # Test 5: Layout and spacing
    test_5 = {
        'name': 'layout_spacing',
        'description': 'Layout and spacing properties implemented',
        'status': 'fail',
        'details': ''
    }
    
    layout_patterns = ['display: flex', 'gap', 'padding', 'margin', 'border-radius']
    found_layout = [pattern for pattern in layout_patterns if pattern in css_content]
    
    if len(found_layout) >= 4:
        test_5['status'] = 'pass'
        test_5['details'] = f'Layout properties found: {", ".join(found_layout)}'
    else:
        test_5['details'] = f'Insufficient layout styling. Found: {found_layout}'
    
    results['tests'].append(test_5)
    
    # Test 6: Interactive elements styling
    test_6 = {
        'name': 'interactive_elements',
        'description': 'Buttons and interactive elements styled',
        'status': 'fail',
        'details': ''
    }
    
    interactive_patterns = ['button', 'cursor: pointer', ':hover', 'transition']
    found_interactive = [pattern for pattern in interactive_patterns if pattern in css_content]
    
    if len(found_interactive) >= 3:
        test_6['status'] = 'pass'
        test_6['details'] = f'Interactive styling found: {", ".join(found_interactive)}'
    else:
        test_6['details'] = f'Insufficient interactive styling. Found: {found_interactive}'
    
    results['tests'].append(test_6)
    
    # Test 7: State-based styling
    test_7 = {
        'name': 'state_styling',
        'description': 'Different states styled (completed, hover, disabled)',
        'status': 'fail',
        'details': ''
    }
    
    state_patterns = ['.completed', ':hover', ':disabled', ':focus']
    found_states = [pattern for pattern in state_patterns if pattern in css_content]
    
    if len(found_states) >= 3:
        test_7['status'] = 'pass'
        test_7['details'] = f'State styling found: {", ".join(found_states)}'
    else:
        test_7['details'] = f'Insufficient state styling. Found: {found_states}'
    
    results['tests'].append(test_7)
    
    # Test 8: Responsive design
    test_8 = {
        'name': 'responsive_design',
        'description': 'Responsive design with media queries',
        'status': 'fail',
        'details': ''
    }
    
    responsive_patterns = ['@media', 'max-width', '640px']
    found_responsive = [pattern for pattern in responsive_patterns if pattern in css_content]
    
    if len(found_responsive) >= 2:
        test_8['status'] = 'pass'
        test_8['details'] = f'Responsive design found: {", ".join(found_responsive)}'
    else:
        test_8['details'] = f'Insufficient responsive design. Found: {found_responsive}'
    
    results['tests'].append(test_8)
    
    # Test 9: Accessibility features
    test_9 = {
        'name': 'accessibility_features',
        'description': 'Accessibility features implemented',
        'status': 'fail',
        'details': ''
    }
    
    a11y_patterns = ['outline', 'focus', 'prefers-contrast', 'prefers-reduced-motion']
    found_a11y = [pattern for pattern in a11y_patterns if pattern in css_content]
    
    if len(found_a11y) >= 2:
        test_9['status'] = 'pass'
        test_9['details'] = f'Accessibility features found: {", ".join(found_a11y)}'
    else:
        test_9['details'] = f'Insufficient accessibility features. Found: {found_a11y}'
    
    results['tests'].append(test_9)
    
    # Test 10: Color scheme
    test_10 = {
        'name': 'color_scheme',
        'description': 'Professional color scheme implemented',
        'status': 'fail',
        'details': ''
    }
    
    # Check for hex colors and color keywords
    color_patterns = ['#[0-9a-fA-F]{6}', '#[0-9a-fA-F]{3}', 'rgba?\\(', 'white', 'background']
    found_colors = []
    
    for pattern in color_patterns:
        if re.search(pattern, css_content):
            found_colors.append(pattern.replace('\\', ''))
    
    if len(found_colors) >= 3:
        test_10['status'] = 'pass'
        test_10['details'] = f'Color scheme implemented with: {", ".join(found_colors[:3])}'
    else:
        test_10['details'] = f'Insufficient color scheme. Found: {found_colors}'
    
    results['tests'].append(test_10)
    
    # Test 11: Empty state styling
    test_11 = {
        'name': 'empty_state_styling',
        'description': 'Empty state properly styled',
        'status': 'fail',
        'details': ''
    }
    
    if '.empty-state' in css_content and 'text-align' in css_content:
        test_11['status'] = 'pass'
        test_11['details'] = 'Empty state styling found'
    else:
        test_11['details'] = 'Empty state styling not found or incomplete'
    
    results['tests'].append(test_11)
    
    # Test 12: CSS organization
    test_12 = {
        'name': 'css_organization',
        'description': 'CSS well-organized with comments and structure',
        'status': 'fail',
        'details': ''
    }
    
    organization_patterns = ['/*', 'TodoList', 'Component']
    comment_count = css_content.count('/*')
    
    if comment_count >= 3:
        test_12['status'] = 'pass'
        test_12['details'] = f'CSS well-organized with {comment_count} comment sections'
    else:
        test_12['details'] = f'Insufficient CSS organization. Found {comment_count} comments'
    
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
    results = test_basic_styling()
    print(f"Task 19 Basic Styling Tests: {results['summary']['passed_tests']}/{results['summary']['total_tests']} passed")
    
    # Print test details
    for test in results['tests']:
        status_icon = '✅' if test['status'] == 'pass' else '❌'
        print(f"{status_icon} {test['name']}: {test['details']}")
    
    print(f"\\nOverall Success Rate: {results['summary']['success_rate']}")