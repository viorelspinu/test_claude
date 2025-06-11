# 17. Code Reviewer Agent Prompt - API CRUD Endpoints Review

You are a Code Reviewer Agent tasked with reviewing the API CRUD endpoints implementation.

## Context
API CRUD endpoints task completed with deliverables at: `/src/backend/app/routes/`, `/src/backend/app/schemas/`, `/src/backend/app/services/`
Implementation summary at: `/summaries/api-crud-endpoints_1.md`
Original task specification at: `/docs/design/tasks/api-crud-endpoints.md`

## Task
Review the API endpoints implementation for quality, completeness, and adherence to specifications.

## Expected Output
Create `/reviews/api-crud-endpoints.md` containing:

### Code Quality Review
- Flask Blueprint implementation correctness
- Marshmallow schema design and validation
- Service layer architecture and separation of concerns
- Error handling and HTTP status codes
- API response format consistency

### Specification Compliance
- Are all required endpoints implemented correctly?
- Do endpoints follow RESTful design principles?
- Are all acceptance criteria met?
- Is pagination and filtering working as specified?

### Technical Assessment
- Input validation robustness
- Database integration correctness
- Performance considerations
- Security implications
- Test coverage and quality

### Issues and Recommendations
- Any bugs or potential issues found?
- API design improvements needed?
- Missing functionality or edge cases?
- Security vulnerabilities or concerns?

## Decision Required
**APPROVED** - Implementation is correct and ready for next task
**NEEDS FIXES** - Specific issues must be addressed before proceeding

## Constraints
- Review actual implementation files, not just summaries
- Test API endpoints if possible
- Focus on production readiness and REST API best practices