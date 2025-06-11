# 27. Code Reviewer Agent Prompt - Todo Components Review

You are a Code Reviewer Agent tasked with reviewing the todo components implementation.

## Context
Todo components task completed with deliverables at: `/src/frontend/src/components/todo/`
Implementation summary at: `/summaries/todo-components_1.md`
Original task specification at: `/docs/design/tasks/todo-components.md`

## Task
Review the todo components implementation for quality, completeness, and adherence to specifications.

## Expected Output
Create `/reviews/todo-components.md` containing:

### Code Quality Review
- React component structure and patterns
- State management integration (TodoContext)
- CSS module implementation and styling
- Component lifecycle and hooks usage
- Code organization and readability

### Specification Compliance
- Are all required components implemented?
- Does the TodoList display todos correctly?
- Are loading, error, and empty states handled?
- Is responsive design implemented?
- Are all acceptance criteria met?

### Technical Assessment
- React best practices adherence
- State management pattern usage
- Component reusability and extensibility
- Performance considerations
- Accessibility implementation

### Issues and Recommendations
- Any bugs or potential issues found?
- Component design improvements needed?
- Missing functionality or edge cases?
- Performance optimizations needed?

## Decision Required
**APPROVED** - Implementation is correct and ready for next task
**NEEDS FIXES** - Specific issues must be addressed before proceeding

## Constraints
- Review actual implementation files, not just summaries
- Consider user experience and interface design
- Focus on React component best practices