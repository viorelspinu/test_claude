#!/usr/bin/env node

/**
 * Basic integration tests for full-stack communication
 * These tests verify that the frontend and backend can communicate properly
 */

const axios = require('axios');
const colors = {
    red: '\x1b[31m',
    green: '\x1b[32m',
    yellow: '\x1b[33m',
    blue: '\x1b[34m',
    reset: '\x1b[0m'
};

// Configuration
const BACKEND_URL = 'http://localhost:5001';
const FRONTEND_URL = 'http://localhost:3000';
const API_BASE_URL = `${BACKEND_URL}/api`;

// Helper functions
function print(message, color = 'reset') {
    console.log(`${colors[color]}${message}${colors.reset}`);
}

function printTest(name, passed, details = '') {
    const icon = passed ? '✅' : '❌';
    const color = passed ? 'green' : 'red';
    print(`${icon} ${name}${details ? ': ' + details : ''}`, color);
}

// Test functions
async function testHealthEndpoint() {
    try {
        const response = await axios.get(`${API_BASE_URL}/health`);
        const passed = response.status === 200 && response.data.status === 'healthy';
        printTest('Health endpoint', passed, response.data.message);
        return passed;
    } catch (error) {
        printTest('Health endpoint', false, error.message);
        return false;
    }
}

async function testCORS() {
    try {
        const response = await axios.get(`${API_BASE_URL}/health`, {
            headers: { 'Origin': FRONTEND_URL }
        });
        const passed = response.headers['access-control-allow-origin'] !== undefined;
        printTest('CORS headers', passed);
        return passed;
    } catch (error) {
        printTest('CORS headers', false, error.message);
        return false;
    }
}

async function testTaskCRUD() {
    let taskId;
    try {
        // Create task
        const createResponse = await axios.post(`${API_BASE_URL}/tasks`, {
            title: 'Integration Test Task',
            description: 'Created by integration test',
            priority: 'Medium'
        });
        
        if (createResponse.status !== 201) {
            throw new Error('Failed to create task');
        }
        
        taskId = createResponse.data.task.id;
        print('  Created task with ID: ' + taskId, 'green');
        
        // Get task
        const getResponse = await axios.get(`${API_BASE_URL}/tasks/${taskId}`);
        if (getResponse.status !== 200) {
            throw new Error('Failed to get task');
        }
        print('  Retrieved task successfully', 'green');
        
        // Update task
        const updateResponse = await axios.put(`${API_BASE_URL}/tasks/${taskId}`, {
            completed: true
        });
        if (updateResponse.status !== 200) {
            throw new Error('Failed to update task');
        }
        print('  Updated task successfully', 'green');
        
        // Delete task
        const deleteResponse = await axios.delete(`${API_BASE_URL}/tasks/${taskId}`);
        if (deleteResponse.status !== 204) {
            throw new Error('Failed to delete task');
        }
        print('  Deleted task successfully', 'green');
        
        printTest('Task CRUD operations', true);
        return true;
    } catch (error) {
        // Try to clean up
        if (taskId) {
            try {
                await axios.delete(`${API_BASE_URL}/tasks/${taskId}`);
            } catch (e) {
                // Ignore cleanup errors
            }
        }
        printTest('Task CRUD operations', false, error.message);
        return false;
    }
}

async function testTaskFiltering() {
    const createdTasks = [];
    
    try {
        // Create test tasks
        const testTasks = [
            { title: 'Completed Task', completed: true, priority: 'High' },
            { title: 'Pending Task', completed: false, priority: 'Low' }
        ];
        
        for (const task of testTasks) {
            const response = await axios.post(`${API_BASE_URL}/tasks`, task);
            createdTasks.push(response.data.task.id);
        }
        
        // Test filtering by completed status
        const completedResponse = await axios.get(`${API_BASE_URL}/tasks?completed=true`);
        const completedTasks = completedResponse.data.tasks.filter(
            t => createdTasks.includes(t.id)
        );
        
        if (completedTasks.length === 0 || !completedTasks.every(t => t.completed)) {
            throw new Error('Completed filter not working correctly');
        }
        
        printTest('Task filtering', true);
        return true;
    } catch (error) {
        printTest('Task filtering', false, error.message);
        return false;
    } finally {
        // Clean up
        for (const taskId of createdTasks) {
            try {
                await axios.delete(`${API_BASE_URL}/tasks/${taskId}`);
            } catch (e) {
                // Ignore cleanup errors
            }
        }
    }
}

async function testTaskStats() {
    try {
        const response = await axios.get(`${API_BASE_URL}/tasks/stats`);
        const stats = response.data.stats;
        
        const passed = response.status === 200 &&
            typeof stats.total_tasks === 'number' &&
            typeof stats.completed_tasks === 'number' &&
            typeof stats.pending_tasks === 'number' &&
            typeof stats.completion_rate === 'number';
        
        printTest('Task statistics', passed);
        return passed;
    } catch (error) {
        printTest('Task statistics', false, error.message);
        return false;
    }
}

async function testFrontendProxy() {
    try {
        // Test if frontend proxy forwards to backend
        const response = await axios.get(`${FRONTEND_URL}/api/health`);
        const passed = response.status === 200 && response.data.status === 'healthy';
        printTest('Frontend proxy', passed);
        return passed;
    } catch (error) {
        printTest('Frontend proxy', false, 'Make sure frontend proxy is configured');
        return false;
    }
}

async function checkService(url, name) {
    try {
        await axios.get(url, { timeout: 5000 });
        print(`✅ ${name} is running at ${url}`, 'green');
        return true;
    } catch (error) {
        print(`❌ ${name} is not accessible at ${url}`, 'red');
        return false;
    }
}

// Main test runner
async function runTests() {
    print('\n🧪 Running Integration Tests', 'blue');
    print('===========================\n', 'blue');
    
    // Check services
    print('Checking services...', 'yellow');
    const backendRunning = await checkService(`${API_BASE_URL}/health`, 'Backend');
    const frontendRunning = await checkService(FRONTEND_URL, 'Frontend');
    
    if (!backendRunning || !frontendRunning) {
        print('\n❌ Services must be running. Start with: npm run dev', 'red');
        process.exit(1);
    }
    
    print('\nRunning tests...', 'yellow');
    
    const tests = [
        { name: 'Health Endpoint', fn: testHealthEndpoint },
        { name: 'CORS Configuration', fn: testCORS },
        { name: 'Task CRUD Operations', fn: testTaskCRUD },
        { name: 'Task Filtering', fn: testTaskFiltering },
        { name: 'Task Statistics', fn: testTaskStats },
        { name: 'Frontend Proxy', fn: testFrontendProxy }
    ];
    
    const results = [];
    
    for (const test of tests) {
        print(`\nTesting ${test.name}...`, 'blue');
        const passed = await test.fn();
        results.push({ name: test.name, passed });
    }
    
    // Summary
    print('\n📊 Test Summary', 'blue');
    print('===============', 'blue');
    
    const passed = results.filter(r => r.passed).length;
    const failed = results.filter(r => !r.passed).length;
    
    print(`Total: ${results.length}`, 'blue');
    print(`Passed: ${passed}`, 'green');
    print(`Failed: ${failed}`, failed > 0 ? 'red' : 'green');
    
    if (failed === 0) {
        print('\n✨ All integration tests passed!', 'green');
        process.exit(0);
    } else {
        print('\n❌ Some tests failed. Check the output above.', 'red');
        process.exit(1);
    }
}

// Handle errors
process.on('unhandledRejection', (error) => {
    print(`\n❌ Unexpected error: ${error.message}`, 'red');
    process.exit(1);
});

// Run tests
runTests();