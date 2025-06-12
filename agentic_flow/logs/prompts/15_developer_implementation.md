# Prompt 15: Developer - TodoItem Component Implementation  
**Timestamp**: 2025-01-23 (estimated)  
**Role**: Developer  
**Action**: Implement Task 15 - TodoItem component  

## Task Context
- **Objective**: Create TodoItem component only
- **Deliverable**: frontend/src/components/TodoItem.js
- **Dependencies**: Task 14 ✅ (TodoList component complete)

## Implementation Plan
1. Create TodoItem functional component with props interface
2. Implement todo display with completion styling
3. Add toggle and delete action handlers
4. Implement loading states for individual operations
5. Add error handling for failed operations
6. Prepare for integration with TodoList component

## Technical Specifications
- Functional React component with props
- Props: todo, onToggle, onDelete for action callbacks
- Local state for loading and error states
- Semantic HTML with accessibility considerations
- Clean action handler implementation

## Component Interface
```javascript
function TodoItem({ todo, onToggle, onDelete })
// Props:
// - todo: {id, text, completed, created_at}
// - onToggle: (id) => Promise
// - onDelete: (id) => Promise
```

## Integration Strategy
- Parent (TodoList) passes todo data and action handlers
- Child (TodoItem) triggers callbacks for state changes
- Parent handles API calls and state updates
- Child handles local loading states

## Implementation Approach
Component-first development with clear props interface for composition.