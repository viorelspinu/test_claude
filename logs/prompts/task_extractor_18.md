# 18. Task Extractor Agent Prompt - Extract Bulk Operations Backend Task

You are a Task Extractor Agent tasked with extracting the next development task.

## Context
Full task breakdown available at: `/docs/design/tasks.yaml`
Previous tasks completed: backend-setup, database-models, api-crud-endpoints

## Task
Extract the next pending task (task ID: `bulk-operations-backend`) from the full task breakdown.

## Expected Output
Create `/docs/design/tasks/bulk-operations-backend.md` containing:
- Complete task specification for bulk-operations-backend
- All acceptance criteria and requirements
- Dependencies and constraints
- Estimated time and priority
- Clear, focused task description without other tasks

## Requirements
- Extract only the bulk-operations-backend task details
- Maintain all original task information
- Format as clean markdown for developer consumption
- Include all acceptance criteria exactly as specified

## Constraints
- Do not include other tasks or the full breakdown
- Keep extraction precise and complete
- Focus only on the bulk operations backend task