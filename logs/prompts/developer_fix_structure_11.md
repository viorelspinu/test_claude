# 11. Software Developer Agent Prompt - Fix Backend Directory Structure

You are a Software Developer Agent tasked with fixing the incorrect directory structure from the backend setup task.

## Issue
The backend setup was implemented in `/src/backend-setup/` but should be in `/src/backend/` according to the architecture specification.

## Task
Move and reorganize the backend implementation to the correct location:

## Expected Output
- Move all files from `/src/backend-setup/backend/` to `/src/backend/`
- Remove the incorrect `/src/backend-setup/` directory
- Verify all files are in the correct locations
- Test that the application still works correctly
- Update implementation summary in `/summaries/backend-setup_1.md`

## Requirements
- Preserve all existing functionality
- Maintain file structure and imports
- Ensure the Flask app still runs correctly
- Follow the architecture specification directory layout

## Constraints
- Do not modify code content, only move files
- Ensure no functionality is lost
- Keep the same project structure within the backend directory