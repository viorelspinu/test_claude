# 008 · Connect Frontend to Backend

## Task Details
- **ID:** 008 (Modified)
- **Title:** Connect Frontend to Backend
- **Priority:** High
- **Effort:** Medium
- **Dependencies:** 005 (completed), 002 (completed)

## Description
Integrate React frontend with Flask backend API to create a working full-stack todo application. Test all CRUD operations end-to-end with the current hardcoded backend data.

## Acceptance Criteria
- Both frontend and backend servers start successfully
- Frontend can fetch and display todos from backend API
- Users can create new todos through the UI
- Users can toggle todo completion status
- Users can edit existing todos
- Users can delete todos with confirmation
- All API responses are handled correctly (success/error)
- Loading states display during API calls
- Error messages show when backend is unavailable
- Todo filtering works with live data
- Full CRUD workflow functions end-to-end

## Testing Requirements
- Start backend server on localhost:8080
- Start frontend server on localhost:3000
- Verify cross-origin requests work (CORS)
- Test all todo operations through the UI
- Verify state synchronization between frontend and backend
- Test error handling when backend is stopped

## File Structure (No Changes Needed)
```
/backend/ - Flask API server
/frontend/ - React development server
```

## Sample Testing Workflow
1. Start Flask backend: `python app.py` (port 8080)
2. Start React frontend: `npm start` (port 3000)
3. Open browser to localhost:3000
4. Verify initial todos load from backend
5. Test creating a new todo
6. Test editing existing todo
7. Test toggling completion status
8. Test deleting a todo
9. Test filtering (all/active/completed)
10. Test error handling (stop backend, observe error message)

## Visible Effect
- Working todo application accessible in browser
- Real-time synchronization between frontend and backend
- All CRUD operations functional through UI
- Professional user experience with loading states and error handling
- Foundation ready for database integration