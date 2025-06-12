# 044 Port Configuration Update

**Timestamp:** 2025-01-06 12:47 UTC  
**User Request:** "start backend on 8080. update your data to remember this!"

## Configuration Change
- Backend Flask server: Port 8080 (was 5000)
- Frontend React server: Port 3000 (unchanged)
- Reason: Port 5000 conflict with AirPlay Receiver on macOS

## Actions Required
1. Start backend on port 8080
2. Update frontend API service to point to localhost:8080
3. Update CLAUDE.md or configuration files to document this change