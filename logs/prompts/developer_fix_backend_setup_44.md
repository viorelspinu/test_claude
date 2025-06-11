# 44. Software Developer Agent Prompt - Fix Backend Virtual Environment

You are a Software Developer Agent tasked with fixing the backend setup issue.

## Issue
User trying to start backend but virtual environment doesn't exist at `/src/backend/venv/`
Error: "source: no such file or directory: venv/bin/activate"

## Task
Set up the Python virtual environment and dependencies for the backend.

## Expected Output
- Create virtual environment in `/src/backend/`
- Install all Python dependencies from requirements.txt
- Verify Flask application starts correctly
- Test database initialization
- Provide corrected startup commands

## Requirements
- Create Python virtual environment using appropriate method
- Install dependencies from requirements.txt
- Ensure Flask app runs on port 5000
- Test that database initializes correctly
- Verify API endpoints are accessible

## Constraints
- Work within the existing backend directory structure
- Use the existing requirements.txt file
- Ensure compatibility with the implemented Flask application
- Test that the backend connects properly with frontend