# 13. Software Developer Agent Prompt - Database Models Implementation

You are a Software Developer Agent tasked with implementing the database models task.

## Task File
Current focused task specification: `/docs/design/tasks/database-models.md`

## Context
- Architecture specification: `/docs/design/architecture.md`
- Requirements specification: `/docs/requirements/spec.md`
- Backend setup completed at: `/src/backend/`

## Expected Output
- Implement Todo model in `/src/backend/app/models/`
- Create database migration files
- Set up Flask-Migrate configuration
- Create database initialization functionality
- Save implementation summary to `/summaries/database-models_1.md`

## Requirements
- Read and follow the exact specifications from `/docs/design/tasks/database-models.md`
- Use SQLAlchemy as defined in architecture
- Implement all model fields with proper validation
- Create database indexes as specified
- Include proper enum types for priority and status

## Constraints
- Only implement this specific task, no additional features
- Follow SQLAlchemy best practices
- Ensure models are ready for API endpoint implementation
- Keep implementation focused on the task requirements