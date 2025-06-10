#!/bin/bash

# Full Stack Connection Test Script
# This script verifies that the React frontend and Flask backend work together correctly

set -e  # Exit on any error

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Configuration
BACKEND_URL="http://localhost:5001"
FRONTEND_URL="http://localhost:3000"
API_BASE_URL="$BACKEND_URL/api"
MAX_WAIT_TIME=60
CHECK_INTERVAL=2

echo -e "${BLUE}🚀 Full Stack Connection Test${NC}"
echo "=================================="

# Function to check if a service is running
check_service() {
    local url=$1
    local service_name=$2
    
    echo -e "${YELLOW}Checking $service_name at $url...${NC}"
    
    if curl -f -s "$url" > /dev/null; then
        echo -e "${GREEN}✅ $service_name is running${NC}"
        return 0
    else
        echo -e "${RED}❌ $service_name is not responding${NC}"
        return 1
    fi
}

# Function to wait for service to be ready
wait_for_service() {
    local url=$1
    local service_name=$2
    local wait_time=0
    
    echo -e "${YELLOW}Waiting for $service_name to be ready...${NC}"
    
    while [ $wait_time -lt $MAX_WAIT_TIME ]; do
        if curl -f -s "$url" > /dev/null; then
            echo -e "${GREEN}✅ $service_name is ready!${NC}"
            return 0
        fi
        
        echo -e "${YELLOW}⏳ Waiting for $service_name... (${wait_time}s)${NC}"
        sleep $CHECK_INTERVAL
        wait_time=$((wait_time + CHECK_INTERVAL))
    done
    
    echo -e "${RED}❌ $service_name failed to start within ${MAX_WAIT_TIME}s${NC}"
    return 1
}

# Function to test API endpoints
test_api_endpoints() {
    echo -e "\n${BLUE}🧪 Testing API Endpoints${NC}"
    echo "-------------------------"
    
    # Test health endpoint
    echo -e "${YELLOW}Testing health endpoint...${NC}"
    if response=$(curl -s "$API_BASE_URL/health"); then
        if echo "$response" | grep -q "healthy"; then
            echo -e "${GREEN}✅ Health endpoint working${NC}"
        else
            echo -e "${RED}❌ Health endpoint returned unexpected response${NC}"
            echo "Response: $response"
            return 1
        fi
    else
        echo -e "${RED}❌ Health endpoint failed${NC}"
        return 1
    fi
    
    # Test get tasks endpoint
    echo -e "${YELLOW}Testing get tasks endpoint...${NC}"
    if response=$(curl -s "$API_BASE_URL/tasks"); then
        if echo "$response" | grep -q "tasks"; then
            echo -e "${GREEN}✅ Get tasks endpoint working${NC}"
        else
            echo -e "${RED}❌ Get tasks endpoint returned unexpected response${NC}"
            echo "Response: $response"
            return 1
        fi
    else
        echo -e "${RED}❌ Get tasks endpoint failed${NC}"
        return 1
    fi
    
    # Test create task endpoint
    echo -e "${YELLOW}Testing create task endpoint...${NC}"
    test_task_data='{"title":"Test Task from Script","description":"This task was created by the test script","priority":"Medium"}'
    
    if response=$(curl -s -X POST -H "Content-Type: application/json" -d "$test_task_data" "$API_BASE_URL/tasks"); then
        if echo "$response" | grep -q "Test Task from Script"; then
            echo -e "${GREEN}✅ Create task endpoint working${NC}"
            
            # Extract task ID for cleanup
            task_id=$(echo "$response" | grep -o '"id":[0-9]*' | grep -o '[0-9]*')
            
            if [ -n "$task_id" ]; then
                echo -e "${YELLOW}Testing delete task endpoint...${NC}"
                if curl -s -X DELETE "$API_BASE_URL/tasks/$task_id" > /dev/null; then
                    echo -e "${GREEN}✅ Delete task endpoint working${NC}"
                else
                    echo -e "${RED}❌ Delete task endpoint failed${NC}"
                fi
            fi
        else
            echo -e "${RED}❌ Create task endpoint returned unexpected response${NC}"
            echo "Response: $response"
            return 1
        fi
    else
        echo -e "${RED}❌ Create task endpoint failed${NC}"
        return 1
    fi
    
    # Test stats endpoint
    echo -e "${YELLOW}Testing stats endpoint...${NC}"
    if response=$(curl -s "$API_BASE_URL/tasks/stats"); then
        if echo "$response" | grep -q "stats"; then
            echo -e "${GREEN}✅ Stats endpoint working${NC}"
        else
            echo -e "${RED}❌ Stats endpoint returned unexpected response${NC}"
            echo "Response: $response"
            return 1
        fi
    else
        echo -e "${RED}❌ Stats endpoint failed${NC}"
        return 1
    fi
}

# Function to test CORS headers
test_cors() {
    echo -e "\n${BLUE}🌐 Testing CORS Configuration${NC}"
    echo "------------------------------"
    
    echo -e "${YELLOW}Testing CORS headers...${NC}"
    response_headers=$(curl -s -I -H "Origin: http://localhost:3000" "$API_BASE_URL/health")
    
    if echo "$response_headers" | grep -q "Access-Control-Allow-Origin"; then
        echo -e "${GREEN}✅ CORS headers present${NC}"
    else
        echo -e "${RED}❌ CORS headers missing${NC}"
        echo "Headers received:"
        echo "$response_headers"
        return 1
    fi
}

# Function to test frontend
test_frontend() {
    echo -e "\n${BLUE}🖥️  Testing Frontend${NC}"
    echo "--------------------"
    
    echo -e "${YELLOW}Testing frontend availability...${NC}"
    if response=$(curl -s "$FRONTEND_URL"); then
        if echo "$response" | grep -q "<!DOCTYPE html>"; then
            echo -e "${GREEN}✅ Frontend serving HTML${NC}"
        else
            echo -e "${RED}❌ Frontend not serving expected HTML${NC}"
            return 1
        fi
    else
        echo -e "${RED}❌ Frontend not accessible${NC}"
        return 1
    fi
}

# Function to show service status
show_status() {
    echo -e "\n${BLUE}📊 Service Status Summary${NC}"
    echo "========================="
    
    echo -e "${YELLOW}Backend (Flask):${NC}"
    if check_service "$API_BASE_URL/health" "Backend API"; then
        echo "  URL: $BACKEND_URL"
        echo "  API: $API_BASE_URL"
    fi
    
    echo -e "\n${YELLOW}Frontend (React):${NC}"
    if check_service "$FRONTEND_URL" "Frontend"; then
        echo "  URL: $FRONTEND_URL"
    fi
}

# Function to show useful commands
show_commands() {
    echo -e "\n${BLUE}🔧 Useful Development Commands${NC}"
    echo "==============================="
    echo "Start both servers:    npm run dev"
    echo "Start backend only:    npm run dev:backend"
    echo "Start frontend only:   npm run dev:frontend"
    echo "Run all tests:         npm run test:all"
    echo "Reset database:        npm run db:reset"
    echo "Seed database:         npm run db:seed"
    echo "Check API health:      curl $API_BASE_URL/health"
    echo "View API docs:         $BACKEND_URL/api/health"
}

# Main test execution
main() {
    echo -e "${YELLOW}Starting full stack connection test...${NC}\n"
    
    # Check if services are running
    backend_running=false
    frontend_running=false
    
    if check_service "$API_BASE_URL/health" "Backend API"; then
        backend_running=true
    fi
    
    if check_service "$FRONTEND_URL" "Frontend"; then
        frontend_running=true
    fi
    
    # If services aren't running, provide guidance
    if [ "$backend_running" = false ] || [ "$frontend_running" = false ]; then
        echo -e "\n${YELLOW}⚠️  Some services are not running.${NC}"
        echo -e "${YELLOW}To start the full stack:${NC}"
        echo "  1. cd /Users/viorel/workspace/test_claude"
        echo "  2. npm run setup (first time only)"
        echo "  3. npm run dev"
        echo ""
        echo -e "${YELLOW}Or start services individually:${NC}"
        echo "  Backend: npm run dev:backend"
        echo "  Frontend: npm run dev:frontend"
        echo ""
        
        # Ask if user wants to wait for services
        echo -e "${YELLOW}Do you want to wait for services to start? (y/n)${NC}"
        read -r answer
        
        if [ "$answer" = "y" ] || [ "$answer" = "Y" ]; then
            if [ "$backend_running" = false ]; then
                wait_for_service "$API_BASE_URL/health" "Backend API"
                backend_running=$?
            fi
            
            if [ "$frontend_running" = false ]; then
                wait_for_service "$FRONTEND_URL" "Frontend"
                frontend_running=$?
            fi
        else
            echo -e "${YELLOW}Skipping wait. Start the services and run this script again.${NC}"
            show_commands
            exit 0
        fi
    fi
    
    # Run tests if services are available
    if [ "$backend_running" = true ] && [ "$frontend_running" = true ]; then
        echo -e "\n${GREEN}🎉 Both services are running! Running comprehensive tests...${NC}"
        
        # Run all tests
        test_api_endpoints || { echo -e "${RED}API tests failed${NC}"; exit 1; }
        test_cors || { echo -e "${RED}CORS tests failed${NC}"; exit 1; }
        test_frontend || { echo -e "${RED}Frontend tests failed${NC}"; exit 1; }
        
        show_status
        
        echo -e "\n${GREEN}🎉 All tests passed! Full stack is working correctly.${NC}"
        echo -e "${GREEN}You can now access:${NC}"
        echo -e "${GREEN}  - Frontend: $FRONTEND_URL${NC}"
        echo -e "${GREEN}  - Backend API: $API_BASE_URL${NC}"
        
    else
        echo -e "${RED}❌ Cannot run full tests - services are not available${NC}"
        show_status
        exit 1
    fi
    
    show_commands
}

# Handle script arguments
case "${1:-}" in
    --help|-h)
        echo "Full Stack Connection Test Script"
        echo ""
        echo "Usage: $0 [options]"
        echo ""
        echo "Options:"
        echo "  --help, -h     Show this help message"
        echo "  --status, -s   Show service status only"
        echo "  --api-only     Test API endpoints only"
        echo "  --cors-only    Test CORS configuration only"
        echo ""
        exit 0
        ;;
    --status|-s)
        show_status
        exit 0
        ;;
    --api-only)
        if check_service "$API_BASE_URL/health" "Backend API"; then
            test_api_endpoints
        else
            echo -e "${RED}Backend API is not running${NC}"
            exit 1
        fi
        exit 0
        ;;
    --cors-only)
        if check_service "$API_BASE_URL/health" "Backend API"; then
            test_cors
        else
            echo -e "${RED}Backend API is not running${NC}"
            exit 1
        fi
        exit 0
        ;;
    *)
        main
        ;;
esac