# Task: Statistics Backend Implementation

## Task ID
task-009-api-stats-endpoint

## Title
Implement statistics API endpoint with overdue calculation

## Description
Create endpoint to return comprehensive statistics including overdue todos calculation. This endpoint provides real-time statistics about the todo list including total counts, completion rates, and overdue items with proper timezone handling.

## Type
Backend

## Dependencies
- task-008-bulk-operations-backend

## Estimated Time
1.5 hours

## Priority
Medium

## Acceptance Criteria
- [ ] /api/todos/stats endpoint implemented
- [ ] Returns total, completed, pending, and overdue counts
- [ ] Overdue logic: due_date < current_date AND status = 'pending'
- [ ] Completion rate percentage calculation
- [ ] Efficient database queries with proper indexing
- [ ] Last updated timestamp included
- [ ] Proper timezone handling for overdue calculation

## Deliverables
- Statistics endpoint in todos routes
- Overdue calculation logic in service layer
- Statistics response schema validation

## Test Requirements
- [ ] Statistics endpoint returns correct data format
- [ ] Overdue count calculation is accurate
- [ ] Completion rate calculation works
- [ ] Performance is under 50ms for 1000+ todos

## API Specification

### Endpoint
```
GET /api/todos/stats
```

### Response Format
```json
{
  "total": 0,
  "completed": 0,
  "pending": 0,
  "overdue": 0,
  "completion_rate": 0.0,
  "last_updated": "2024-01-01T00:00:00Z"
}
```

### Response Fields
- `total`: Total number of todos (excluding soft-deleted)
- `completed`: Number of todos with status 'completed'
- `pending`: Number of todos with status 'pending'
- `overdue`: Number of todos where due_date < current_date AND status = 'pending'
- `completion_rate`: Percentage of completed todos (completed/total * 100)
- `last_updated`: ISO timestamp of when statistics were calculated

## Technical Requirements

### Performance
- Response time must be under 50ms for datasets with 1000+ todos
- Use efficient SQL queries with proper aggregations
- Leverage existing database indexes

### Timezone Handling
- Use UTC for all date calculations
- Ensure consistent timezone handling across the application
- Current date should be calculated server-side to avoid client timezone issues

### Database Optimization
- Use aggregate queries to calculate counts efficiently
- Minimize number of database round trips
- Consider adding database indexes if needed for performance

## Implementation Notes

### Service Layer Changes
- Add statistics calculation method to TodoService
- Implement overdue calculation logic
- Ensure timezone-aware date comparisons

### Route Handler
- Add new statistics endpoint to todos routes
- Include proper error handling and response formatting
- Add response schema validation

### Testing Strategy
- Unit tests for overdue calculation logic
- Integration tests for the API endpoint
- Performance tests with large datasets
- Edge case testing (empty database, all overdue, etc.)

## Business Rules
- Soft-deleted todos should not be included in any counts
- Overdue calculation only applies to pending todos
- Completion rate should handle division by zero (return 0 when no todos exist)
- Statistics should reflect real-time data (no caching initially)

## Error Handling
- Return appropriate HTTP status codes
- Handle database connection errors gracefully
- Provide meaningful error messages for debugging
- Ensure endpoint doesn't crash on edge cases (empty database, invalid dates)