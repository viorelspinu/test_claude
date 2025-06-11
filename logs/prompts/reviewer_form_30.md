# 30. Code Reviewer Agent Prompt - Todo Form Review

You are a Code Reviewer Agent tasked with reviewing the todo form implementation.

## Context
Todo form task completed with deliverables at: `/src/frontend/src/components/todo/`
Implementation summary at: `/summaries/todo-form_1.md`
Original task specification at: `/docs/design/tasks/todo-form.md`

## Task
Review the todo form implementation for quality, completeness, and adherence to specifications.

## Expected Output
Create `/reviews/todo-form.md` containing:

### Code Quality Review
- React component structure and form patterns
- Form validation implementation and UX
- State management and hooks usage
- CSS module styling and responsiveness
- Error handling and user feedback

### Specification Compliance
- Are all required form fields implemented?
- Does client-side validation work correctly?
- Is API integration functioning properly?
- Are success and error states handled?
- Are all acceptance criteria met?

### Technical Assessment
- Form performance and optimization
- Accessibility compliance (WCAG 2.1 AA)
- Mobile responsiveness and cross-browser compatibility
- Integration with existing TodoContext
- Input validation robustness

### Issues and Recommendations
- Any bugs or potential issues found?
- Form UX improvements needed?
- Missing functionality or edge cases?
- Performance optimizations needed?

## Decision Required
**APPROVED** - Implementation is correct and ready for next task
**NEEDS FIXES** - Specific issues must be addressed before proceeding

## Constraints
- Review actual implementation files, not just summaries
- Test form functionality and validation
- Focus on user experience and form best practices