# 37. Code Reviewer Agent Prompt - TodoItem Component Review

You are a Code Reviewer Agent tasked with reviewing the TodoItem component implementation.

## Context
TodoItem component task completed with deliverables at: `/src/frontend/src/components/todo/`
Implementation summary at: `/summaries/todo-item_1.md`
Original task specification at: `/docs/design/tasks/todo-item.md`

## Task
Review the TodoItem component implementation for quality, completeness, and adherence to specifications.

## Expected Output
Create `/reviews/todo-item.md` containing:

### Code Quality Review
- React component structure and patterns
- PropTypes validation and error handling
- CSS module styling and visual design
- Component reusability and maintainability
- Integration with existing components

### Specification Compliance
- Are all display requirements met (title, description, priority, due date)?
- Do interactive elements work correctly (toggle, edit, delete)?
- Is priority color coding implemented?
- Are overdue items highlighted properly?
- Is TodoContext integration functional?
- Are all acceptance criteria met?

### Technical Assessment
- Component performance and optimization
- Accessibility compliance (ARIA, keyboard navigation)
- Mobile responsiveness and cross-device compatibility
- State management patterns and data flow
- Integration with TodoList component

### Issues and Recommendations
- Any bugs or potential issues found?
- Component improvements needed?
- Missing functionality or edge cases?
- Performance optimizations needed?

## Decision Required
**APPROVED** - Implementation is correct and ready for next task
**NEEDS FIXES** - Specific issues must be addressed before proceeding

## Constraints
- Review actual implementation files, not just summaries
- Test component functionality and user interactions
- Focus on user experience and production readiness