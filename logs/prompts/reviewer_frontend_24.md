# 24. Code Reviewer Agent Prompt - Frontend Setup Review

You are a Code Reviewer Agent tasked with reviewing the frontend setup implementation.

## Context
Frontend setup task completed with deliverables at: `/src/frontend/`
Implementation summary at: `/summaries/frontend-setup_1.md`
Original task specification at: `/docs/design/tasks/frontend-setup.md`

## Task
Review the frontend setup implementation for quality, completeness, and adherence to specifications.

## Expected Output
Create `/reviews/frontend-setup.md` containing:

### Code Quality Review
- React project structure and organization
- Vite configuration and build setup
- Component architecture and patterns
- State management implementation (Context API)
- API service layer design

### Specification Compliance
- Are all required dependencies installed correctly?
- Is the component directory structure proper?
- Does the development server work as specified?
- Is routing setup correctly?
- Are all acceptance criteria met?

### Technical Assessment
- Vite configuration correctness
- React Router implementation
- API integration setup (axios, proxy)
- State management pattern (Context + useReducer)
- Development workflow readiness

### Issues and Recommendations
- Any bugs or potential issues found?
- Architecture improvements needed?
- Missing functionality or setup?
- Performance considerations?

## Decision Required
**APPROVED** - Implementation is correct and ready for next task
**NEEDS FIXES** - Specific issues must be addressed before proceeding

## Constraints
- Review actual implementation files, not just summaries
- Test development server startup if possible
- Focus on production readiness and React best practices