# Task 04: Storage Functions

## Objective
Create in-memory storage functions for todos

## Deliverable
Storage functions in `backend/models.py`

## Dependencies
Task 03 (todo_model) - COMPLETED

## Success Criteria
Storage functions work with Todo instances

## Implementation Details
- Add global in-memory storage list to models.py
- Create function to add todo to storage
- Create function to get all todos from storage
- Create function to get todo by ID
- Create function to update todo in storage
- Create function to delete todo from storage
- Ensure thread-safety considerations

## Testing Requirements
- Verify todos can be stored and retrieved
- Test CRUD operations work correctly
- Confirm storage persistence within session
- Test error handling for missing todos