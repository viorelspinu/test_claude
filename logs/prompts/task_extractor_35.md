# 35. Task Extractor Agent Prompt - Extract TodoItem Component Task

You are a Task Extractor Agent tasked with extracting the next critical development task.

## Context
Full task breakdown available at: `/docs/design/tasks.yaml`
Progress assessment completed showing TodoItem component as highest priority

## Task
Extract the next pending task (task ID: `todo-item`) from the full task breakdown.

## Expected Output
Create `/docs/design/tasks/todo-item.md` containing:
- Complete task specification for todo-item
- All acceptance criteria and requirements
- Dependencies and constraints
- Estimated time and priority
- Clear, focused task description without other tasks

## Requirements
- Extract only the todo-item task details
- Maintain all original task information
- Format as clean markdown for developer consumption
- Include all acceptance criteria exactly as specified

## Constraints
- Do not include other tasks or the full breakdown
- Keep extraction precise and complete
- Focus only on the TodoItem component task