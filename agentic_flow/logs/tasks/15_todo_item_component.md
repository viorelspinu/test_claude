# Task 15: TodoItem Component
**Task ID**: 15  
**Name**: todo_item_component  
**Assigned**: Developer  
**Status**: In Progress  

## Objective
Create TodoItem component only

## Description  
Create the TodoItem component that represents an individual todo item. This component will receive todo data as props and handle individual todo operations like toggling completion status and deletion.

## Deliverable
`frontend/src/components/TodoItem.js`

## Dependencies
- Task 14 ✅ (TodoList component complete)

## Technical Requirements
1. **Component Structure**
   - Functional React component with props
   - PropTypes for type checking (optional but recommended)
   - Clean, semantic HTML structure

2. **Props Interface**
   - `todo` - Todo object with id, text, completed, created_at
   - `onToggle` - Function to handle completion toggle
   - `onDelete` - Function to handle todo deletion
   - `onUpdate` - Function to handle todo text updates (for future)

3. **Component Features**
   - Display todo text with completion styling
   - Toggle button for completion status
   - Delete button for todo removal
   - Visual indicators for completed/pending status
   - Accessible and semantic markup

4. **State Management**
   - Local loading states for individual actions
   - Error handling for failed operations
   - Optimistic updates for better UX

5. **API Integration**
   - Use API service functions via props (passed from parent)
   - Handle async operations with loading indicators
   - Error handling for API failures

## Implementation Scope
- **In Scope**: TodoItem component, props interface, action handlers
- **Out of Scope**: Direct API calls (handled by parent), todo creation

## Component Behavior
1. **Display**: Show todo text with completion status styling
2. **Toggle**: Handle completion status changes with loading state
3. **Delete**: Handle todo deletion with confirmation
4. **Error**: Show inline errors for failed operations

## Integration with TodoList
- TodoList will map over todos and render TodoItem components
- TodoList will pass todo data and action handlers as props
- TodoItem will trigger callbacks to parent for state updates

## Test Criteria
- TodoItem component renders todo data
- Toggle functionality works properly
- Delete functionality works properly
- Loading states display correctly
- Props interface clean and consistent

## Success Metrics
- ✅ TodoItem.js created in components directory
- ✅ Component receives and displays todo props
- ✅ Action handlers implemented (toggle, delete)
- ✅ Loading states for individual operations
- ✅ Ready for TodoList integration