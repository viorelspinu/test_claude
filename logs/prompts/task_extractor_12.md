# 12. Task Extractor Agent Prompt - Extract Database Models Task

You are a Task Extractor Agent tasked with extracting the next development task.

## Context
Full task breakdown available at: `/docs/design/tasks.yaml`
Previous task (backend-setup) completed and approved

## Task
Extract the next pending task (task ID: `database-models`) from the full task breakdown.

## Expected Output
Create `/docs/design/tasks/database-models.md` containing:
- Complete task specification for database-models
- All acceptance criteria and requirements
- Dependencies and constraints
- Estimated time and priority
- Clear, focused task description without other tasks

## Requirements
- Extract only the database-models task details
- Maintain all original task information
- Format as clean markdown for developer consumption
- Include all acceptance criteria exactly as specified

## Constraints
- Do not include other tasks or the full breakdown
- Keep extraction precise and complete
- Focus only on the database models task