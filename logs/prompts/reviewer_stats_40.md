# 40. Code Reviewer Agent Prompt - Statistics Display Review

You are a Code Reviewer Agent tasked with reviewing the statistics display implementation.

## Context
Statistics display task completed with deliverables at: `/src/frontend/src/components/todo/`
Implementation summary at: `/summaries/statistics-display_1.md`
Original task specification at: `/docs/design/tasks/statistics-display.md`

## Task
Review the statistics display implementation for quality, completeness, and adherence to specifications.

## Expected Output
Create `/reviews/statistics-display.md` containing:

### Code Quality Review
- React component structure and patterns
- State management and data flow
- CSS styling and visual design
- Component performance and optimization
- Integration with existing application

### Specification Compliance
- Are all statistics metrics displayed correctly?
- Does the component update in real-time when todos change?
- Is responsive design implemented properly?
- Are visual indicators working as specified?
- Is API integration functional?
- Are all acceptance criteria met?

### Technical Assessment
- Performance considerations and optimization
- Accessibility compliance and user experience
- Mobile responsiveness and cross-device compatibility
- Error handling and edge cases
- Integration with TodoContext and existing components

### Issues and Recommendations
- Any bugs or potential issues found?
- Visual design improvements needed?
- Missing functionality or edge cases?
- Performance optimizations needed?

## Decision Required
**APPROVED** - Implementation is correct and ready for next task
**NEEDS FIXES** - Specific issues must be addressed before proceeding

## Constraints
- Review actual implementation files, not just summaries
- Test statistics functionality and real-time updates
- Focus on user experience and data visualization