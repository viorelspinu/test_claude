# 14. Code Reviewer Agent Prompt - Database Models Review

You are a Code Reviewer Agent tasked with reviewing the database models implementation.

## Context
Database models task completed with deliverables at: `/src/backend/app/models/`
Implementation summary at: `/summaries/database-models_1.md`
Original task specification at: `/docs/design/tasks/database-models.md`

## Task
Review the database models implementation for quality, completeness, and adherence to specifications.

## Expected Output
Create `/reviews/database-models.md` containing:

### Code Quality Review
- SQLAlchemy model implementation correctness
- Field definitions and constraints
- Enum type implementations
- Validation methods and business logic
- Code organization and structure

### Specification Compliance
- Are all required fields implemented correctly?
- Are database indexes properly created?
- Does the migration setup work correctly?
- Are all acceptance criteria met?

### Technical Assessment
- Database schema correctness
- Performance considerations (indexes)
- Data validation and constraints
- Model relationships and foreign keys

### Issues and Recommendations
- Any bugs or potential issues found?
- Performance optimizations needed?
- Missing functionality or edge cases?
- Security considerations?

## Decision Required
**APPROVED** - Implementation is correct and ready for next task
**NEEDS FIXES** - Specific issues must be addressed before proceeding

## Constraints
- Review actual implementation files, not just summaries
- Test database operations if possible
- Focus on production readiness and best practices