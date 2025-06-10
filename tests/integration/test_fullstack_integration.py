"""
Full-stack integration tests for Todo application

These tests verify the complete integration between frontend and backend,
including API communication, CORS handling, and data flow.
"""

import pytest
import json
import time
import subprocess
import requests
from requests.exceptions import ConnectionError
import sys
import os

# Add parent directory to path for imports
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../../backend')))

from app import create_app, db
from app.models import Task

# Configuration
BACKEND_URL = "http://localhost:5001"
FRONTEND_URL = "http://localhost:3000"
API_BASE_URL = f"{BACKEND_URL}/api"
MAX_WAIT_TIME = 30
CHECK_INTERVAL = 1


class TestFullStackIntegration:
    """Test full-stack integration between React frontend and Flask backend"""
    
    @classmethod
    def setup_class(cls):
        """Setup test environment"""
        cls.backend_process = None
        cls.frontend_process = None
        cls.app = create_app('testing')
        cls.client = cls.app.test_client()
        
        # Check if services are already running
        cls.backend_already_running = cls._check_service(API_BASE_URL + "/health")
        cls.frontend_already_running = cls._check_service(FRONTEND_URL)
        
        if not cls.backend_already_running or not cls.frontend_already_running:
            pytest.skip("Services must be running. Start with: npm run dev")
    
    @staticmethod
    def _check_service(url):
        """Check if a service is accessible"""
        try:
            response = requests.get(url, timeout=5)
            return response.status_code == 200
        except (ConnectionError, requests.Timeout):
            return False
    
    @staticmethod
    def _wait_for_service(url, service_name):
        """Wait for a service to be ready"""
        wait_time = 0
        while wait_time < MAX_WAIT_TIME:
            if TestFullStackIntegration._check_service(url):
                print(f"✅ {service_name} is ready")
                return True
            
            print(f"⏳ Waiting for {service_name}... ({wait_time}s)")
            time.sleep(CHECK_INTERVAL)
            wait_time += CHECK_INTERVAL
        
        print(f"❌ {service_name} failed to start within {MAX_WAIT_TIME}s")
        return False
    
    def test_health_check(self):
        """Test API health endpoint"""
        response = requests.get(f"{API_BASE_URL}/health")
        assert response.status_code == 200
        
        data = response.json()
        assert data['status'] == 'healthy'
        assert 'timestamp' in data
        assert 'message' in data
    
    def test_cors_headers(self):
        """Test CORS configuration"""
        headers = {
            'Origin': FRONTEND_URL,
            'Access-Control-Request-Method': 'POST',
            'Access-Control-Request-Headers': 'Content-Type'
        }
        
        # Test preflight request
        response = requests.options(f"{API_BASE_URL}/tasks", headers=headers)
        assert response.status_code == 200
        assert 'Access-Control-Allow-Origin' in response.headers
        assert response.headers['Access-Control-Allow-Origin'] in [FRONTEND_URL, '*']
        
        # Test actual request with origin
        response = requests.get(f"{API_BASE_URL}/tasks", headers={'Origin': FRONTEND_URL})
        assert response.status_code == 200
        assert 'Access-Control-Allow-Origin' in response.headers
    
    def test_create_and_retrieve_task(self):
        """Test creating a task through API and retrieving it"""
        # Create a task
        task_data = {
            'title': 'Integration Test Task',
            'description': 'Created by integration test',
            'priority': 'High'
        }
        
        create_response = requests.post(
            f"{API_BASE_URL}/tasks",
            json=task_data,
            headers={'Content-Type': 'application/json', 'Origin': FRONTEND_URL}
        )
        
        assert create_response.status_code == 201
        created_task = create_response.json()['task']
        assert created_task['title'] == task_data['title']
        assert created_task['description'] == task_data['description']
        assert created_task['priority'] == task_data['priority']
        assert 'id' in created_task
        
        task_id = created_task['id']
        
        # Retrieve the task
        get_response = requests.get(f"{API_BASE_URL}/tasks/{task_id}")
        assert get_response.status_code == 200
        
        retrieved_task = get_response.json()['task']
        assert retrieved_task['id'] == task_id
        assert retrieved_task['title'] == task_data['title']
        
        # Clean up
        delete_response = requests.delete(f"{API_BASE_URL}/tasks/{task_id}")
        assert delete_response.status_code == 204
    
    def test_task_lifecycle(self):
        """Test complete task lifecycle: create, update, complete, delete"""
        # Create
        task_data = {'title': 'Lifecycle Test Task', 'priority': 'Medium'}
        create_response = requests.post(f"{API_BASE_URL}/tasks", json=task_data)
        assert create_response.status_code == 201
        
        task = create_response.json()['task']
        task_id = task['id']
        assert task['completed'] is False
        
        # Update
        update_data = {
            'description': 'Updated description',
            'priority': 'High'
        }
        update_response = requests.put(f"{API_BASE_URL}/tasks/{task_id}", json=update_data)
        assert update_response.status_code == 200
        
        updated_task = update_response.json()['task']
        assert updated_task['description'] == update_data['description']
        assert updated_task['priority'] == update_data['priority']
        
        # Complete
        complete_response = requests.put(
            f"{API_BASE_URL}/tasks/{task_id}",
            json={'completed': True}
        )
        assert complete_response.status_code == 200
        assert complete_response.json()['task']['completed'] is True
        
        # Delete
        delete_response = requests.delete(f"{API_BASE_URL}/tasks/{task_id}")
        assert delete_response.status_code == 204
        
        # Verify deletion
        get_response = requests.get(f"{API_BASE_URL}/tasks/{task_id}")
        assert get_response.status_code == 404
    
    def test_task_filtering(self):
        """Test task filtering capabilities"""
        # Create test tasks
        test_tasks = [
            {'title': 'Completed Task 1', 'completed': True, 'priority': 'High'},
            {'title': 'Completed Task 2', 'completed': True, 'priority': 'Low'},
            {'title': 'Pending Task 1', 'completed': False, 'priority': 'High'},
            {'title': 'Pending Task 2', 'completed': False, 'priority': 'Medium'}
        ]
        
        created_ids = []
        for task_data in test_tasks:
            response = requests.post(f"{API_BASE_URL}/tasks", json=task_data)
            assert response.status_code == 201
            created_ids.append(response.json()['task']['id'])
        
        # Test filtering by completion status
        completed_response = requests.get(f"{API_BASE_URL}/tasks?completed=true")
        assert completed_response.status_code == 200
        completed_tasks = completed_response.json()['tasks']
        
        for task in completed_tasks:
            if task['id'] in created_ids:
                assert task['completed'] is True
        
        # Test filtering by priority
        high_priority_response = requests.get(f"{API_BASE_URL}/tasks?priority=High")
        assert high_priority_response.status_code == 200
        high_priority_tasks = high_priority_response.json()['tasks']
        
        for task in high_priority_tasks:
            if task['id'] in created_ids:
                assert task['priority'] == 'High'
        
        # Clean up
        for task_id in created_ids:
            requests.delete(f"{API_BASE_URL}/tasks/{task_id}")
    
    def test_pagination(self):
        """Test pagination functionality"""
        # Create multiple tasks
        created_ids = []
        for i in range(15):
            response = requests.post(
                f"{API_BASE_URL}/tasks",
                json={'title': f'Pagination Test Task {i}'}
            )
            created_ids.append(response.json()['task']['id'])
        
        # Test first page
        page1_response = requests.get(f"{API_BASE_URL}/tasks?page=1&per_page=10")
        assert page1_response.status_code == 200
        
        page1_data = page1_response.json()
        assert len(page1_data['tasks']) <= 10
        assert page1_data['pagination']['page'] == 1
        assert page1_data['pagination']['per_page'] == 10
        
        # Test second page
        page2_response = requests.get(f"{API_BASE_URL}/tasks?page=2&per_page=10")
        assert page2_response.status_code == 200
        
        page2_data = page2_response.json()
        assert page2_data['pagination']['page'] == 2
        
        # Clean up
        for task_id in created_ids:
            requests.delete(f"{API_BASE_URL}/tasks/{task_id}")
    
    def test_bulk_operations(self):
        """Test bulk update functionality"""
        # Create test tasks
        task_ids = []
        for i in range(3):
            response = requests.post(
                f"{API_BASE_URL}/tasks",
                json={'title': f'Bulk Test Task {i}', 'priority': 'Low'}
            )
            task_ids.append(response.json()['task']['id'])
        
        # Bulk update
        bulk_data = {
            'task_ids': task_ids,
            'updates': {'completed': True, 'priority': 'High'}
        }
        
        bulk_response = requests.put(f"{API_BASE_URL}/tasks/bulk", json=bulk_data)
        assert bulk_response.status_code == 200
        
        updated_tasks = bulk_response.json()['tasks']
        assert len(updated_tasks) == 3
        
        for task in updated_tasks:
            assert task['completed'] is True
            assert task['priority'] == 'High'
        
        # Clean up
        for task_id in task_ids:
            requests.delete(f"{API_BASE_URL}/tasks/{task_id}")
    
    def test_task_statistics(self):
        """Test task statistics endpoint"""
        # Create test data
        test_tasks = [
            {'title': 'Stats Test 1', 'completed': True, 'priority': 'High'},
            {'title': 'Stats Test 2', 'completed': True, 'priority': 'Medium'},
            {'title': 'Stats Test 3', 'completed': False, 'priority': 'Low'},
            {'title': 'Stats Test 4', 'completed': False, 'priority': 'High'}
        ]
        
        created_ids = []
        for task_data in test_tasks:
            response = requests.post(f"{API_BASE_URL}/tasks", json=task_data)
            created_ids.append(response.json()['task']['id'])
        
        # Get statistics
        stats_response = requests.get(f"{API_BASE_URL}/tasks/stats")
        assert stats_response.status_code == 200
        
        stats = stats_response.json()['stats']
        assert 'total_tasks' in stats
        assert 'completed_tasks' in stats
        assert 'pending_tasks' in stats
        assert 'completion_rate' in stats
        assert 'priority_breakdown' in stats
        
        # Clean up
        for task_id in created_ids:
            requests.delete(f"{API_BASE_URL}/tasks/{task_id}")
    
    def test_error_handling(self):
        """Test API error handling"""
        # Test missing required field
        response = requests.post(
            f"{API_BASE_URL}/tasks",
            json={'description': 'No title provided'}
        )
        assert response.status_code == 400
        error_data = response.json()
        assert 'error' in error_data
        assert error_data['error']['code'] == 'MISSING_TITLE'
        
        # Test invalid priority
        response = requests.post(
            f"{API_BASE_URL}/tasks",
            json={'title': 'Test', 'priority': 'InvalidPriority'}
        )
        assert response.status_code == 400
        assert response.json()['error']['code'] == 'INVALID_PRIORITY'
        
        # Test non-existent task
        response = requests.get(f"{API_BASE_URL}/tasks/999999")
        assert response.status_code == 404
        assert response.json()['error']['code'] == 'TASK_NOT_FOUND'
    
    def test_concurrent_requests(self):
        """Test handling of concurrent requests"""
        import concurrent.futures
        
        def create_task(index):
            response = requests.post(
                f"{API_BASE_URL}/tasks",
                json={'title': f'Concurrent Task {index}', 'priority': 'Medium'}
            )
            return response.status_code == 201, response.json().get('task', {}).get('id')
        
        # Create tasks concurrently
        with concurrent.futures.ThreadPoolExecutor(max_workers=5) as executor:
            futures = [executor.submit(create_task, i) for i in range(10)]
            results = [future.result() for future in concurrent.futures.as_completed(futures)]
        
        # Verify all succeeded
        created_ids = []
        for success, task_id in results:
            assert success
            if task_id:
                created_ids.append(task_id)
        
        assert len(created_ids) == 10
        
        # Clean up
        for task_id in created_ids:
            requests.delete(f"{API_BASE_URL}/tasks/{task_id}")
    
    def test_frontend_proxy(self):
        """Test that frontend proxy to backend works correctly"""
        # This test assumes the frontend dev server is running with proxy configured
        if not self.frontend_already_running:
            pytest.skip("Frontend must be running for proxy test")
        
        # Make request through frontend proxy
        proxy_response = requests.get(f"{FRONTEND_URL}/api/health")
        assert proxy_response.status_code == 200
        assert proxy_response.json()['status'] == 'healthy'
    
    @classmethod
    def teardown_class(cls):
        """Cleanup after all tests"""
        # Note: We don't stop services that were already running
        pass


if __name__ == "__main__":
    pytest.main([__file__, "-v", "--tb=short"])