# 32. Software Developer Agent Prompt - Bulk Operations Frontend Implementation

You are a Software Developer Agent tasked with implementing the bulk operations frontend task.

## Task File
Current focused task specification: `/docs/design/tasks/bulk-operations-frontend.md`

## Context
- Architecture specification: `/docs/design/architecture.md`
- Requirements specification: `/docs/requirements/spec.md`
- Frontend components (TodoList, TodoForm) completed at: `/src/frontend/`
- Backend bulk operations API available and tested

## Expected Output
- Implement BulkActions component in `/src/frontend/src/components/todo/`
- Add bulk selection functionality to TodoList
- Create confirmation dialogs and progress tracking
- Integrate with backend bulk operations API
- Implement proper error handling and user feedback
- Save implementation summary to `/summaries/bulk-operations-frontend_1.md`

## Requirements
- Read and follow the exact specifications from `/docs/design/tasks/bulk-operations-frontend.md`
- Implement bulk selection with checkboxes in TodoList
- Create BulkActions toolbar with delete and status update operations
- Add confirmation dialogs with accurate item counts
- Include progress tracking for operations > 10 items
- Maximum 50 items validation

## Constraints
- Only implement this specific task, no additional features
- Follow React and UX best practices
- Ensure integration with existing TodoList and TodoContext
- Keep implementation focused on the task requirements