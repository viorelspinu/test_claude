# 018 · Integration Testing Script

## Full-Stack Integration Test

This test script validates the complete todo application workflow from frontend to backend.

### Prerequisites
- Flask backend implemented with API routes
- React frontend with component structure
- Both servers configured for respective ports

### Test Execution Plan

#### Phase 1: Server Startup
1. Start Flask backend on port 8080
2. Verify backend API endpoints respond
3. Start React frontend on port 3000
4. Verify frontend loads without errors

#### Phase 2: Basic Integration
1. Open browser to localhost:3000
2. Verify initial todo data loads from backend
3. Check browser network tab for successful API calls
4. Verify CORS headers present in responses

#### Phase 3: CRUD Operations Testing
1. **Create Todo**: Use form to add new todo, verify it appears in list
2. **Read Todos**: Verify all todos display with correct data
3. **Update Todo**: Toggle completion status, edit title/description
4. **Delete Todo**: Delete todo with confirmation dialog

#### Phase 4: UI Features Testing
1. **Filtering**: Test All/Active/Completed filter buttons
2. **Counts**: Verify todo counts update correctly
3. **Loading States**: Observe loading indicators during API calls
4. **Form Validation**: Test required field validation

#### Phase 5: Error Handling
1. Stop backend server
2. Try to perform operations in frontend
3. Verify error messages display correctly
4. Test retry functionality

### Success Criteria
- All servers start without errors
- Frontend successfully communicates with backend
- All CRUD operations work through UI
- Error handling graceful and informative
- Professional user experience maintained