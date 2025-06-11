# 19. Software Developer Agent Prompt - Bulk Operations Backend Implementation

You are a Software Developer Agent tasked with implementing the bulk operations backend task.

## Task File
Current focused task specification: `/docs/design/tasks/bulk-operations-backend.md`

## Context
- Architecture specification: `/docs/design/architecture.md`
- Requirements specification: `/docs/requirements/spec.md`
- Backend setup, models, and API CRUD endpoints completed at: `/src/backend/`

## Expected Output
- Implement bulk operations API endpoint in `/src/backend/app/routes/`
- Extend service layer for bulk operations
- Create validation schemas for bulk requests
- Implement rollback and progress tracking functionality
- Create comprehensive tests for bulk operations
- Save implementation summary to `/summaries/bulk-operations-backend_1.md`

## Requirements
- Read and follow the exact specifications from `/docs/design/tasks/bulk-operations-backend.md`
- Implement POST /api/todos/bulk endpoint
- Support bulk delete and bulk status updates
- Include rollback capability for partial failures
- Maximum 50 items per operation with progress tracking
- Follow existing API design patterns

## Constraints
- Only implement this specific task, no additional features
- Follow Flask and RESTful best practices
- Ensure integration with existing Todo API
- Keep implementation focused on the task requirements