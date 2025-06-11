# 33. Code Reviewer Agent Prompt - Bulk Operations Frontend Review

You are a Code Reviewer Agent tasked with reviewing the bulk operations frontend implementation.

## Context
Bulk operations frontend task completed with deliverables at: `/src/frontend/src/components/todo/`
Implementation summary at: `/summaries/bulk-operations-frontend_1.md`
Original task specification at: `/docs/design/tasks/bulk-operations-frontend.md`

## Task
Review the bulk operations frontend implementation for quality, completeness, and adherence to specifications.

## Expected Output
Create `/reviews/bulk-operations-frontend.md` containing:

### Code Quality Review
- React component structure and patterns
- State management integration with TodoContext
- UI/UX design and user interaction patterns
- Component reusability and modularity
- Error handling and user feedback

### Specification Compliance
- Are bulk selection checkboxes implemented correctly?
- Does the BulkActions toolbar function as specified?
- Are confirmation dialogs working with accurate counts?
- Is progress tracking implemented for operations > 10 items?
- Is the 50-item maximum limit enforced?
- Are all acceptance criteria met?

### Technical Assessment
- Integration with backend bulk operations API
- Performance considerations for large selections
- Accessibility compliance and keyboard navigation
- Mobile responsiveness and cross-device compatibility
- State management patterns and data flow

### Issues and Recommendations
- Any bugs or potential issues found?
- UX improvements needed?
- Missing functionality or edge cases?
- Performance optimizations needed?

## Decision Required
**APPROVED** - Implementation is correct and ready for next task
**NEEDS FIXES** - Specific issues must be addressed before proceeding

## Constraints
- Review actual implementation files, not just summaries
- Test bulk operations functionality and user flows
- Focus on user experience and production readiness