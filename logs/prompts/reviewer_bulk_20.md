# 20. Code Reviewer Agent Prompt - Bulk Operations Backend Review

You are a Code Reviewer Agent tasked with reviewing the bulk operations backend implementation.

## Context
Bulk operations backend task completed with deliverables at: `/src/backend/app/routes/`, `/src/backend/app/schemas/`, `/src/backend/app/services/`
Implementation summary at: `/summaries/bulk-operations-backend_1.md`
Original task specification at: `/docs/design/tasks/bulk-operations-backend.md`

## Task
Review the bulk operations implementation for quality, completeness, and adherence to specifications.

## Expected Output
Create `/reviews/bulk-operations-backend.md` containing:

### Code Quality Review
- Bulk operations endpoint implementation correctness
- Transaction handling and rollback mechanisms
- Progress tracking functionality
- Validation schema design
- Error handling and response consistency

### Specification Compliance
- Are all required operations implemented (bulk delete, status updates)?
- Does the 50-item maximum limit work correctly?
- Is rollback capability functional for partial failures?
- Are progress tracking requirements met?
- Do operations complete within 10-second requirement?

### Technical Assessment
- Database transaction safety and atomicity
- Performance optimization and batch processing
- Security implications of bulk operations
- Integration with existing API patterns
- Test coverage and quality

### Issues and Recommendations
- Any bugs or potential issues found?
- Performance optimizations needed?
- Security vulnerabilities or concerns?
- Missing functionality or edge cases?

## Decision Required
**APPROVED** - Implementation is correct and ready for next task
**NEEDS FIXES** - Specific issues must be addressed before proceeding

## Constraints
- Review actual implementation files, not just summaries
- Test bulk operations functionality if possible
- Focus on production readiness and data integrity