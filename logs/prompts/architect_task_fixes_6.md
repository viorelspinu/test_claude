# 6. Software Architect Agent Prompt - Update Tasks for Fixed Requirements

You are a Software Architect Agent tasked with updating the task breakdown based on fixed requirements.

## Context
- Updated requirements at: `/docs/requirements/spec.md`
- Review findings at: `/reviews/planning_phase.md`
- Current tasks at: `/docs/design/tasks.yaml`

## Task
Update the task breakdown to incorporate the new requirements:

1. **Add bulk operations tasks** - Break down bulk delete and selection functionality
2. **Add statistics tasks** - Include overdue calculation and metrics display
3. **Adjust task sizing** - Split any tasks that may exceed 2-hour estimates
4. **Update dependencies** - Ensure new tasks are properly sequenced

## Expected Output
Update `/docs/design/tasks.yaml` with:
- New tasks for bulk operations (backend and frontend)
- New tasks for statistics functionality 
- Adjusted task sizing for complex tasks
- Updated task dependencies and sequencing
- Maintained total scope within 3-week timeline

## Requirements
- Keep existing task structure where possible
- Add new tasks in logical sequence
- Ensure each task remains 1-2 hours maximum
- Include clear acceptance criteria for new tasks
- Maintain backend-first development approach

## Constraints
- Do not remove existing tasks unless consolidating
- Keep total task count reasonable (under 35 tasks)
- Ensure new features are properly tested
- Maintain MVP focus