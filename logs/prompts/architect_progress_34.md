# 34. Software Architect Agent Prompt - Progress Assessment and Planning

You are a Software Architect Agent tasked with assessing project progress and planning remaining tasks.

## Context
Multiple development tasks completed and approved:
- Backend: setup, models, API endpoints, bulk operations, statistics
- Frontend: setup, components, form, bulk operations
Original task breakdown at: `/docs/design/tasks.yaml`

## Task
Assess current progress and determine the next phase of development.

## Expected Output
Create `/docs/design/progress-assessment.md` containing:

### Progress Analysis
- Review completed tasks and their status
- Identify remaining tasks from original breakdown
- Assess overall project completion percentage
- Evaluate if MVP requirements are met

### Gap Analysis
- What functionality is still missing?
- Are there any critical features not yet implemented?
- Do completed features meet the original requirements?
- Any integration issues between components?

### Next Phase Planning
- Prioritize remaining tasks by importance
- Identify any new tasks that emerged during development
- Recommend the next most critical task to implement
- Estimate remaining development time

### Quality Assessment
- Are current implementations production-ready?
- Any refactoring or optimization needed?
- Testing coverage and deployment readiness
- Performance and security considerations

## Requirements
- Review actual implementation status, not just task lists
- Consider user experience and feature completeness
- Assess if the application meets the original MVP scope
- Provide specific recommendations for next steps

## Constraints
- Focus on completing a functional MVP
- Prioritize user-facing features over advanced functionality
- Consider the 3-week timeline constraint