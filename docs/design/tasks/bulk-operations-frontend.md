# Task: Bulk Operations Frontend Implementation

## Task ID
`task-020-bulk-operations-frontend`

## Title
Implement bulk operations frontend functionality

## Description
Create bulk delete and bulk status update UI with confirmation and progress tracking

## Type
frontend

## Dependencies
- task-019-bulk-selection-ui

## Estimated Time
2 hours

## Priority
high

## Acceptance Criteria
- [ ] Bulk actions toolbar appears when items selected
- [ ] "Delete Selected" button with confirmation dialog
- [ ] "Mark Selected as Complete/Pending" buttons
- [ ] Progress indicator for operations > 10 items
- [ ] Confirmation dialog shows accurate count
- [ ] Error handling for partial failures
- [ ] Maximum 50 items validation

## Deliverables
- `/frontend/src/components/todo/BulkActions.jsx`
- Bulk operations API integration
- Confirmation dialogs and progress tracking

## Test Requirements
- [ ] Bulk actions only appear when items selected
- [ ] Confirmation dialog prevents accidental operations
- [ ] Progress tracking works for large operations
- [ ] Error feedback shows specific failures

## Implementation Requirements

### Component Structure
- **BulkActions Component**: Main toolbar component that appears when todos are selected
- **Confirmation Dialogs**: Modals for confirming bulk operations with item counts
- **Progress Indicator**: Visual feedback for operations affecting > 10 items

### Functionality Details

#### Bulk Actions Toolbar
- Only visible when one or more todos are selected
- Contains action buttons for bulk operations
- Displays count of selected items
- Maximum 50 items validation with user feedback

#### Bulk Delete Operation
- "Delete Selected" button
- Confirmation dialog showing exact count of items to be deleted
- API integration with `/api/todos/bulk` endpoint
- Optimistic UI updates with rollback on failure

#### Bulk Status Update Operations
- "Mark Selected as Complete" button
- "Mark Selected as Pending" button
- Confirmation dialog for status change operations
- API integration for bulk status updates

#### Progress Tracking
- Progress bar or spinner for operations > 10 items
- Real-time feedback during bulk operations
- Ability to show partial completion status

#### Error Handling
- Detailed error reporting for individual item failures
- Partial failure scenarios (some items succeed, others fail)
- User-friendly error messages
- Retry mechanisms for failed operations

### Technical Specifications

#### API Integration
- Use existing bulk operations backend endpoint (`/api/todos/bulk`)
- Handle response format for bulk operations
- Process success/failure status for individual items

#### State Management
- Integrate with existing TodoContext
- Manage bulk operation loading states
- Handle selection state updates after operations

#### User Experience
- Clear visual feedback for all operations
- Prevent accidental bulk operations through confirmation
- Intuitive button placement and labeling
- Responsive design for mobile devices

### Constraints
- Maximum 50 items per bulk operation
- Performance requirement: operations should complete within 10 seconds
- Must integrate with existing selection UI (task-019)
- Follow existing component patterns and styling