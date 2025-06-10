"""
Integration tests for the Flask Todo API

Tests the complete API functionality including CORS headers.
"""

import json
import pytest
from app import create_app, db
from app.models import Task


@pytest.fixture
def app():
    """Create application for testing"""
    app = create_app('testing')
    
    with app.app_context():
        db.create_all()
        yield app
        db.drop_all()


@pytest.fixture
def client(app):
    """Create test client"""
    return app.test_client()


@pytest.fixture
def sample_task():
    """Sample task data for testing"""
    return {
        'title': 'Test Task',
        'description': 'This is a test task',
        'priority': 'High',
        'completed': False
    }


class TestAPIIntegration:
    """Test API integration functionality"""
    
    def test_health_endpoint(self, client):
        """Test health check endpoint"""
        response = client.get('/api/health')
        assert response.status_code == 200
        
        data = json.loads(response.data)
        assert data['status'] == 'healthy'
        assert 'timestamp' in data
        assert 'message' in data
    
    def test_cors_headers(self, client):
        """Test CORS headers are present"""
        response = client.get('/api/health', headers={'Origin': 'http://localhost:3000'})
        assert response.status_code == 200
        
        # Check for CORS headers
        assert 'Access-Control-Allow-Origin' in response.headers
    
    def test_get_empty_tasks(self, client):
        """Test getting tasks when database is empty"""
        response = client.get('/api/tasks')
        assert response.status_code == 200
        
        data = json.loads(response.data)
        assert data['tasks'] == []
        assert data['pagination']['total'] == 0
    
    def test_create_task(self, client, sample_task):
        """Test creating a new task"""
        response = client.post('/api/tasks', 
                             data=json.dumps(sample_task),
                             content_type='application/json')
        
        assert response.status_code == 201
        data = json.loads(response.data)
        
        assert 'task' in data
        assert data['task']['title'] == sample_task['title']
        assert data['task']['priority'] == sample_task['priority']
        assert data['task']['completed'] == False
        assert 'id' in data['task']
    
    def test_get_tasks_after_creation(self, client, sample_task):
        """Test getting tasks after creating one"""
        # Create a task first
        client.post('/api/tasks', 
                   data=json.dumps(sample_task),
                   content_type='application/json')
        
        # Get all tasks
        response = client.get('/api/tasks')
        assert response.status_code == 200
        
        data = json.loads(response.data)
        assert len(data['tasks']) == 1
        assert data['pagination']['total'] == 1
        assert data['tasks'][0]['title'] == sample_task['title']
    
    def test_get_specific_task(self, client, sample_task):
        """Test getting a specific task by ID"""
        # Create a task first
        create_response = client.post('/api/tasks', 
                                    data=json.dumps(sample_task),
                                    content_type='application/json')
        task_id = json.loads(create_response.data)['task']['id']
        
        # Get the specific task
        response = client.get(f'/api/tasks/{task_id}')
        assert response.status_code == 200
        
        data = json.loads(response.data)
        assert data['task']['id'] == task_id
        assert data['task']['title'] == sample_task['title']
    
    def test_update_task(self, client, sample_task):
        """Test updating a task"""
        # Create a task first
        create_response = client.post('/api/tasks', 
                                    data=json.dumps(sample_task),
                                    content_type='application/json')
        task_id = json.loads(create_response.data)['task']['id']
        
        # Update the task
        update_data = {'completed': True, 'priority': 'Low'}
        response = client.put(f'/api/tasks/{task_id}',
                            data=json.dumps(update_data),
                            content_type='application/json')
        
        assert response.status_code == 200
        data = json.loads(response.data)
        assert data['task']['completed'] == True
        assert data['task']['priority'] == 'Low'
    
    def test_delete_task(self, client, sample_task):
        """Test deleting a task"""
        # Create a task first
        create_response = client.post('/api/tasks', 
                                    data=json.dumps(sample_task),
                                    content_type='application/json')
        task_id = json.loads(create_response.data)['task']['id']
        
        # Delete the task
        response = client.delete(f'/api/tasks/{task_id}')
        assert response.status_code == 204
        
        # Verify task is deleted
        get_response = client.get(f'/api/tasks/{task_id}')
        assert get_response.status_code == 404
    
    def test_task_filtering(self, client):
        """Test task filtering functionality"""
        # Create multiple tasks
        tasks = [
            {'title': 'Completed Task', 'completed': True, 'priority': 'High'},
            {'title': 'Pending Task', 'completed': False, 'priority': 'Low'},
            {'title': 'Medium Task', 'completed': False, 'priority': 'Medium'}
        ]
        
        for task in tasks:
            client.post('/api/tasks', 
                       data=json.dumps(task),
                       content_type='application/json')
        
        # Test filtering by completed status
        response = client.get('/api/tasks?completed=true')
        data = json.loads(response.data)
        assert len(data['tasks']) == 1
        assert data['tasks'][0]['completed'] == True
        
        # Test filtering by priority
        response = client.get('/api/tasks?priority=High')
        data = json.loads(response.data)
        assert len(data['tasks']) == 1
        assert data['tasks'][0]['priority'] == 'High'
    
    def test_bulk_update(self, client):
        """Test bulk updating tasks"""
        # Create multiple tasks
        task_ids = []
        for i in range(3):
            response = client.post('/api/tasks', 
                                 data=json.dumps({
                                     'title': f'Task {i}',
                                     'priority': 'Medium'
                                 }),
                                 content_type='application/json')
            task_id = json.loads(response.data)['task']['id']
            task_ids.append(task_id)
        
        # Bulk update
        bulk_data = {
            'task_ids': task_ids,
            'updates': {'completed': True, 'priority': 'High'}
        }
        response = client.put('/api/tasks/bulk',
                            data=json.dumps(bulk_data),
                            content_type='application/json')
        
        assert response.status_code == 200
        data = json.loads(response.data)
        assert len(data['tasks']) == 3
        for task in data['tasks']:
            assert task['completed'] == True
            assert task['priority'] == 'High'
    
    def test_task_stats(self, client):
        """Test task statistics endpoint"""
        # Create test tasks
        tasks = [
            {'title': 'Task 1', 'completed': True, 'priority': 'High'},
            {'title': 'Task 2', 'completed': False, 'priority': 'Medium'},
            {'title': 'Task 3', 'completed': False, 'priority': 'Low'}
        ]
        
        for task in tasks:
            client.post('/api/tasks', 
                       data=json.dumps(task),
                       content_type='application/json')
        
        # Get stats
        response = client.get('/api/tasks/stats')
        assert response.status_code == 200
        
        data = json.loads(response.data)
        stats = data['stats']
        assert stats['total_tasks'] == 3
        assert stats['completed_tasks'] == 1
        assert stats['pending_tasks'] == 2
        assert stats['completion_rate'] == 33.33
        assert stats['priority_breakdown']['high'] == 1
        assert stats['priority_breakdown']['medium'] == 1
        assert stats['priority_breakdown']['low'] == 1
    
    def test_error_handling(self, client):
        """Test API error handling"""
        # Test creating task without title
        response = client.post('/api/tasks', 
                             data=json.dumps({'description': 'No title'}),
                             content_type='application/json')
        assert response.status_code == 400
        
        data = json.loads(response.data)
        assert 'error' in data
        assert data['error']['code'] == 'MISSING_TITLE'
        
        # Test getting non-existent task
        response = client.get('/api/tasks/999')
        assert response.status_code == 404
        
        # Test invalid priority
        response = client.post('/api/tasks', 
                             data=json.dumps({
                                 'title': 'Test',
                                 'priority': 'Invalid'
                             }),
                             content_type='application/json')
        assert response.status_code == 400
        
        data = json.loads(response.data)
        assert data['error']['code'] == 'INVALID_PRIORITY'
    
    def test_pagination(self, client):
        """Test task pagination"""
        # Create many tasks
        for i in range(25):
            client.post('/api/tasks', 
                       data=json.dumps({'title': f'Task {i}'}),
                       content_type='application/json')
        
        # Test first page
        response = client.get('/api/tasks?page=1&per_page=10')
        data = json.loads(response.data)
        
        assert len(data['tasks']) == 10
        assert data['pagination']['page'] == 1
        assert data['pagination']['total'] == 25
        assert data['pagination']['pages'] == 3
        assert data['pagination']['has_next'] == True
        assert data['pagination']['has_prev'] == False
        
        # Test second page
        response = client.get('/api/tasks?page=2&per_page=10')
        data = json.loads(response.data)
        
        assert len(data['tasks']) == 10
        assert data['pagination']['page'] == 2
        assert data['pagination']['has_next'] == True
        assert data['pagination']['has_prev'] == True