# Task: Statistics Display Component

## Task ID: task-024-statistics-display

## Title
Create statistics dashboard component

## Description
Build component to display todo statistics (total, completed, pending, overdue)

## Task Type
frontend

## Dependencies
- task-023-pagination-implementation

## Estimated Time
1.5 hours

## Acceptance Criteria
- Statistics component with visual display
- API integration with statistics endpoint
- Real-time updates when todos change
- Visual indicators for different metrics
- Responsive design for various screen sizes

## Deliverables
- `/frontend/src/components/todo/TodoStats.jsx`
- Statistics API integration

## Test Requirements
- Statistics display correctly
- Statistics update when todos change
- Component renders on different screen sizes

## Implementation Details

### Component Requirements
1. **TodoStats Component**
   - Display total number of todos
   - Display completed count
   - Display pending count
   - Display overdue count
   - Show completion rate percentage
   - Include last updated timestamp

2. **Visual Design**
   - Card-based layout for each metric
   - Color-coded indicators:
     - Green for completed
     - Blue for pending
     - Red for overdue
     - Gray for total
   - Progress bar or chart for completion rate
   - Icons for each metric type

3. **API Integration**
   - Connect to `/api/todos/stats` endpoint
   - Handle loading states
   - Handle error states
   - Auto-refresh when todo list changes

4. **Responsive Behavior**
   - Mobile: Stacked cards (1 column)
   - Tablet: 2x2 grid
   - Desktop: Single row with 4 columns
   - Maintain readability at all sizes

### Technical Considerations
- Use React Context to share state with todo list
- Implement useEffect hook for data fetching
- Consider using a library like recharts for visual elements
- Ensure component re-renders when todos are added/updated/deleted
- Handle timezone considerations for overdue calculation display

### Priority
Medium

### Status
Pending