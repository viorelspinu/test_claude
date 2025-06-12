# Task 03: Todo Model

## Objective
Create Todo data model class

## Deliverable
`backend/models.py` with Todo class definition only

## Dependencies
None

## Success Criteria
Todo class instantiates correctly

## Implementation Details
- Create `backend/models.py` file
- Define Todo class with required attributes:
  - id (unique identifier)
  - text (todo description)
  - completed (boolean status)
  - created_at (timestamp)
- Add constructor method
- Include string representation method
- Basic validation for required fields

## Testing Requirements
- Verify Todo class can be instantiated
- Test all attributes are properly set
- Verify string representation works
- Test default values and validation