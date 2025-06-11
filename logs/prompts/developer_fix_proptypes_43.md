# 43. Software Developer Agent Prompt - Fix PropTypes Dependency

You are a Software Developer Agent tasked with fixing a missing dependency issue.

## Issue
Frontend failing to start with error: Failed to resolve import "prop-types" from TodoItem.jsx
The prop-types package is not installed in the frontend dependencies.

## Task
Fix the missing prop-types dependency in the frontend project.

## Expected Output
- Install prop-types package in frontend
- Verify the frontend starts without errors
- Test that TodoItem component loads correctly
- Update package.json with the dependency

## Requirements
- Install prop-types using npm
- Ensure version compatibility with React 18+
- Test that the application starts successfully
- Verify no other missing dependencies

## Constraints
- Only fix this specific dependency issue
- Do not modify component code, just add the missing package
- Ensure frontend development server starts without errors