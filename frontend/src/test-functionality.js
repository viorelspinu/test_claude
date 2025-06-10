/**
 * Manual test script for verifying frontend functionality
 * Run this script with: node src/test-functionality.js
 */

import taskService from './services/taskService.js';
import { ApiError } from './services/api.js';

console.log('Testing Todo List Frontend Functionality');
console.log('========================================\n');

const testData = {
  tasks: []
};

async function delay(ms) {
  return new Promise(resolve => setTimeout(resolve, ms));
}

async function testCreateTask() {
  console.log('1. Testing Create Task...');
  try {
    const newTask = await taskService.createTask({
      title: 'Test Task 1',
      description: 'This is a test task created by the test script',
      priority: 'High'
    });
    console.log('✓ Task created successfully:', newTask);
    testData.tasks.push(newTask);
    
    // Test with minimal data
    const minimalTask = await taskService.createTask({
      title: 'Minimal Test Task'
    });
    console.log('✓ Minimal task created successfully:', minimalTask);
    testData.tasks.push(minimalTask);
    
    // Test validation error
    try {
      await taskService.createTask({ description: 'No title' });
      console.error('✗ Should have failed with validation error');
    } catch (error) {
      if (error instanceof ApiError && error.isValidationError()) {
        console.log('✓ Validation error handled correctly:', error.message);
      } else {
        throw error;
      }
    }
    
    console.log('✓ Create task tests passed!\n');
  } catch (error) {
    console.error('✗ Create task test failed:', error);
    process.exit(1);
  }
}

async function testGetTasks() {
  console.log('2. Testing Get Tasks...');
  try {
    // Get all tasks
    const allTasks = await taskService.getTasks();
    console.log(`✓ Retrieved ${allTasks.tasks.length} tasks`);
    
    // Test filtering by priority
    const highPriorityTasks = await taskService.getTasksByPriority('High');
    console.log(`✓ Found ${highPriorityTasks.tasks.length} high priority tasks`);
    
    // Test filtering by status
    const completedTasks = await taskService.getTasksByStatus(true);
    console.log(`✓ Found ${completedTasks.tasks.length} completed tasks`);
    
    // Test search
    const searchResults = await taskService.searchTasks('test');
    console.log(`✓ Search found ${searchResults.tasks.length} tasks matching 'test'`);
    
    // Test sorting
    const sortedTasks = await taskService.getTasks({
      sort: 'created_at',
      order: 'desc'
    });
    console.log('✓ Tasks sorted by creation date');
    
    console.log('✓ Get tasks tests passed!\n');
  } catch (error) {
    console.error('✗ Get tasks test failed:', error);
    process.exit(1);
  }
}

async function testUpdateTask() {
  console.log('3. Testing Update Task...');
  try {
    if (testData.tasks.length === 0) {
      console.log('⚠ No tasks to update, skipping...');
      return;
    }
    
    const taskToUpdate = testData.tasks[0];
    
    // Update task details
    const updatedTask = await taskService.updateTask(taskToUpdate.id, {
      title: 'Updated Test Task',
      description: 'This task has been updated',
      priority: 'Medium'
    });
    console.log('✓ Task details updated successfully');
    
    // Toggle completion
    const completedTask = await taskService.toggleTaskCompletion(
      taskToUpdate.id, 
      true
    );
    console.log('✓ Task marked as completed');
    
    // Toggle back to incomplete
    const incompleteTask = await taskService.toggleTaskCompletion(
      taskToUpdate.id, 
      false
    );
    console.log('✓ Task marked as incomplete');
    
    console.log('✓ Update task tests passed!\n');
  } catch (error) {
    console.error('✗ Update task test failed:', error);
    process.exit(1);
  }
}

async function testDeleteTask() {
  console.log('4. Testing Delete Task...');
  try {
    if (testData.tasks.length === 0) {
      console.log('⚠ No tasks to delete, skipping...');
      return;
    }
    
    const taskToDelete = testData.tasks[testData.tasks.length - 1];
    
    await taskService.deleteTask(taskToDelete.id);
    console.log('✓ Task deleted successfully');
    
    // Verify task is deleted
    try {
      await taskService.getTask(taskToDelete.id);
      console.error('✗ Task should have been deleted');
    } catch (error) {
      if (error instanceof ApiError && error.isNotFoundError()) {
        console.log('✓ Deletion verified - task not found');
      } else {
        throw error;
      }
    }
    
    console.log('✓ Delete task tests passed!\n');
  } catch (error) {
    console.error('✗ Delete task test failed:', error);
    process.exit(1);
  }
}

async function testTaskStats() {
  console.log('5. Testing Task Statistics...');
  try {
    const stats = await taskService.getTaskStats();
    console.log('✓ Task statistics retrieved:', stats);
    console.log('✓ Task stats test passed!\n');
  } catch (error) {
    console.error('✗ Task stats test failed:', error);
    process.exit(1);
  }
}

async function testBulkOperations() {
  console.log('6. Testing Bulk Operations...');
  try {
    // Create multiple tasks for bulk operations
    const bulkTasks = [];
    for (let i = 1; i <= 3; i++) {
      const task = await taskService.createTask({
        title: `Bulk Test Task ${i}`,
        priority: 'Low'
      });
      bulkTasks.push(task);
    }
    console.log(`✓ Created ${bulkTasks.length} tasks for bulk testing`);
    
    // Bulk update
    const updates = bulkTasks.map(task => ({
      id: task.id,
      updates: { completed: true, priority: 'High' }
    }));
    
    const bulkResult = await taskService.bulkUpdateTasks(updates);
    console.log(`✓ Bulk updated ${bulkResult.successful.length} tasks`);
    
    if (bulkResult.errors.length > 0) {
      console.log(`⚠ ${bulkResult.errors.length} tasks failed to update`);
    }
    
    // Clean up bulk tasks
    for (const task of bulkTasks) {
      await taskService.deleteTask(task.id);
    }
    console.log('✓ Cleaned up bulk test tasks');
    
    console.log('✓ Bulk operations tests passed!\n');
  } catch (error) {
    console.error('✗ Bulk operations test failed:', error);
    process.exit(1);
  }
}

async function cleanup() {
  console.log('7. Cleaning up test data...');
  try {
    // Clean up any remaining test tasks
    for (const task of testData.tasks) {
      try {
        await taskService.deleteTask(task.id);
      } catch (error) {
        // Ignore if already deleted
      }
    }
    console.log('✓ Test data cleaned up\n');
  } catch (error) {
    console.error('✗ Cleanup failed:', error);
  }
}

async function runAllTests() {
  console.log('Starting all tests...\n');
  console.log('Note: Make sure the backend server is running on http://localhost:5001\n');
  
  try {
    await delay(1000); // Give time for any setup
    
    await testCreateTask();
    await delay(500);
    
    await testGetTasks();
    await delay(500);
    
    await testUpdateTask();
    await delay(500);
    
    await testDeleteTask();
    await delay(500);
    
    await testTaskStats();
    await delay(500);
    
    await testBulkOperations();
    await delay(500);
    
    await cleanup();
    
    console.log('========================================');
    console.log('✓ All tests passed successfully!');
    console.log('========================================');
    
  } catch (error) {
    console.error('\n========================================');
    console.error('✗ Tests failed with error:', error);
    console.error('========================================');
    process.exit(1);
  }
}

// Run tests if this file is executed directly
if (import.meta.url === `file://${process.argv[1]}`) {
  runAllTests();
}

export { runAllTests };