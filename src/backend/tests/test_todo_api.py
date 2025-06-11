"""
Comprehensive tests for Todo API endpoints.

This module tests all CRUD operations, error handling, validation, and edge cases
for the Todo API endpoints.
"""

import json
import pytest
from datetime import date, timedelta
from app.models.todo import Todo, PriorityEnum, StatusEnum
from app import db


class TestTodoAPI:
    """Test class for Todo API endpoints."""
    
    def test_get_todos_empty(self, client):
        """Test getting todos when none exist."""
        response = client.get('/api/todos')
        assert response.status_code == 200
        
        data = json.loads(response.data)
        assert data['success'] is True
        assert data['data']['todos'] == []
        assert data['data']['pagination']['total'] == 0
    
    def test_get_todos_with_data(self, client, create_sample_todos):
        """Test getting todos with existing data."""
        response = client.get('/api/todos')
        assert response.status_code == 200
        
        data = json.loads(response.data)
        assert data['success'] is True
        assert len(data['data']['todos']) == 4
        assert data['data']['pagination']['total'] == 4
        assert data['message'] == "Todos retrieved successfully"
    
    def test_get_todos_pagination(self, client, create_sample_todos):
        """Test todos pagination."""
        # Test first page with 2 items per page
        response = client.get('/api/todos?page=1&per_page=2')
        assert response.status_code == 200
        
        data = json.loads(response.data)
        assert len(data['data']['todos']) == 2
        assert data['data']['pagination']['page'] == 1
        assert data['data']['pagination']['per_page'] == 2
        assert data['data']['pagination']['total'] == 4
        assert data['data']['pagination']['pages'] == 2
        assert data['data']['pagination']['has_next'] is True
        assert data['data']['pagination']['has_prev'] is False
        
        # Test second page
        response = client.get('/api/todos?page=2&per_page=2')
        assert response.status_code == 200
        
        data = json.loads(response.data)
        assert len(data['data']['todos']) == 2
        assert data['data']['pagination']['page'] == 2
        assert data['data']['pagination']['has_next'] is False
        assert data['data']['pagination']['has_prev'] is True
    
    def test_get_todos_filter_by_status(self, client, create_sample_todos):
        """Test filtering todos by status."""
        # Filter by pending status
        response = client.get('/api/todos?status=pending')
        assert response.status_code == 200
        
        data = json.loads(response.data)
        pending_todos = data['data']['todos']
        assert len(pending_todos) == 3  # 3 pending todos
        for todo in pending_todos:
            assert todo['status'] == 'pending'
        
        # Filter by completed status
        response = client.get('/api/todos?status=completed')
        assert response.status_code == 200
        
        data = json.loads(response.data)
        completed_todos = data['data']['todos']
        assert len(completed_todos) == 1  # 1 completed todo
        assert completed_todos[0]['status'] == 'completed'
    
    def test_get_todos_filter_by_priority(self, client, create_sample_todos):
        """Test filtering todos by priority."""
        response = client.get('/api/todos?priority=high')
        assert response.status_code == 200
        
        data = json.loads(response.data)
        high_priority_todos = data['data']['todos']
        assert len(high_priority_todos) == 2  # 2 high priority todos
        for todo in high_priority_todos:
            assert todo['priority'] == 'high'
    
    def test_get_todos_invalid_parameters(self, client):
        """Test invalid query parameters."""
        # Invalid page number
        response = client.get('/api/todos?page=-1')
        assert response.status_code == 400
        
        data = json.loads(response.data)
        assert data['success'] is False
        assert 'positive' in data['error']['message'].lower()
        
        # Invalid per_page
        response = client.get('/api/todos?per_page=0')
        assert response.status_code == 400
        
        # Invalid status
        response = client.get('/api/todos?status=invalid')
        assert response.status_code == 400
        
        # Invalid priority
        response = client.get('/api/todos?priority=invalid')
        assert response.status_code == 400
    
    def test_get_todo_by_id(self, client, create_sample_todos):
        """Test getting a specific todo by ID."""
        todos = create_sample_todos
        todo_id = todos[0].id
        
        response = client.get(f'/api/todos/{todo_id}')
        assert response.status_code == 200
        
        data = json.loads(response.data)
        assert data['success'] is True
        assert data['data']['id'] == todo_id
        assert data['data']['title'] == "Completed Todo"
        assert data['message'] == "Todo retrieved successfully"
    
    def test_get_todo_not_found(self, client):
        """Test getting a non-existent todo."""
        response = client.get('/api/todos/999')
        assert response.status_code == 404
        
        data = json.loads(response.data)
        assert data['success'] is False
        assert data['error']['code'] == 'NOT_FOUND'
        assert '999' in data['error']['message']
    
    def test_create_todo_success(self, client, sample_todo_data):
        """Test creating a todo successfully."""
        response = client.post(
            '/api/todos',
            data=json.dumps(sample_todo_data),
            content_type='application/json'
        )
        assert response.status_code == 201
        
        data = json.loads(response.data)
        assert data['success'] is True
        assert data['data']['title'] == sample_todo_data['title']
        assert data['data']['description'] == sample_todo_data['description']
        assert data['data']['priority'] == sample_todo_data['priority']
        assert data['data']['status'] == 'pending'  # default
        assert data['data']['id'] is not None
        assert data['message'] == "Todo created successfully"
    
    def test_create_todo_minimal(self, client):
        """Test creating a todo with minimal data."""
        minimal_data = {'title': 'Minimal Todo'}
        
        response = client.post(
            '/api/todos',
            data=json.dumps(minimal_data),
            content_type='application/json'
        )
        assert response.status_code == 201
        
        data = json.loads(response.data)
        assert data['success'] is True
        assert data['data']['title'] == 'Minimal Todo'
        assert data['data']['description'] is None
        assert data['data']['priority'] == 'medium'  # default
        assert data['data']['status'] == 'pending'  # default
        assert data['data']['due_date'] is None
    
    def test_create_todo_validation_errors(self, client):
        """Test create todo validation errors."""
        # Missing title
        response = client.post(
            '/api/todos',
            data=json.dumps({}),
            content_type='application/json'
        )
        assert response.status_code == 400
        
        data = json.loads(response.data)
        assert data['success'] is False
        assert data['error']['code'] == 'VALIDATION_ERROR'
        assert 'title' in data['error']['details']
        
        # Empty title
        response = client.post(
            '/api/todos',
            data=json.dumps({'title': ''}),
            content_type='application/json'
        )
        assert response.status_code == 400
        
        # Title too long
        response = client.post(
            '/api/todos',
            data=json.dumps({'title': 'x' * 201}),
            content_type='application/json'
        )
        assert response.status_code == 400
        
        # Invalid priority
        response = client.post(
            '/api/todos',
            data=json.dumps({'title': 'Test', 'priority': 'invalid'}),
            content_type='application/json'
        )
        assert response.status_code == 400
        
        # Past due date
        past_date = (date.today() - timedelta(days=1)).isoformat()
        response = client.post(
            '/api/todos',
            data=json.dumps({'title': 'Test', 'due_date': past_date}),
            content_type='application/json'
        )
        assert response.status_code == 400
    
    def test_create_todo_invalid_content_type(self, client):
        """Test creating todo with invalid content type."""
        response = client.post('/api/todos', data='not json')
        assert response.status_code == 400
        
        data = json.loads(response.data)
        assert data['error']['code'] == 'INVALID_CONTENT_TYPE'
    
    def test_update_todo_success(self, client, create_sample_todos):
        """Test updating a todo successfully."""
        todos = create_sample_todos
        todo_id = todos[1].id  # pending todo
        
        update_data = {
            'title': 'Updated Todo Title',
            'description': 'Updated description',
            'priority': 'high',
            'status': 'completed'
        }
        
        response = client.put(
            f'/api/todos/{todo_id}',
            data=json.dumps(update_data),
            content_type='application/json'
        )
        assert response.status_code == 200
        
        data = json.loads(response.data)
        assert data['success'] is True
        assert data['data']['title'] == update_data['title']
        assert data['data']['description'] == update_data['description']
        assert data['data']['priority'] == update_data['priority']
        assert data['data']['status'] == update_data['status']
        assert data['message'] == "Todo updated successfully"
    
    def test_update_todo_partial(self, client, create_sample_todos):
        """Test partial update of a todo."""
        todos = create_sample_todos
        todo_id = todos[1].id
        original_title = todos[1].title
        
        update_data = {'priority': 'high'}
        
        response = client.put(
            f'/api/todos/{todo_id}',
            data=json.dumps(update_data),
            content_type='application/json'
        )
        assert response.status_code == 200
        
        data = json.loads(response.data)
        assert data['success'] is True
        assert data['data']['title'] == original_title  # unchanged
        assert data['data']['priority'] == 'high'  # updated
    
    def test_update_todo_not_found(self, client):
        """Test updating a non-existent todo."""
        update_data = {'title': 'Updated Title'}
        
        response = client.put(
            '/api/todos/999',
            data=json.dumps(update_data),
            content_type='application/json'
        )
        assert response.status_code == 404
        
        data = json.loads(response.data)
        assert data['success'] is False
        assert data['error']['code'] == 'NOT_FOUND'
    
    def test_update_todo_validation_errors(self, client, create_sample_todos):
        """Test update todo validation errors."""
        todos = create_sample_todos
        todo_id = todos[0].id
        
        # Empty title
        response = client.put(
            f'/api/todos/{todo_id}',
            data=json.dumps({'title': ''}),
            content_type='application/json'
        )
        assert response.status_code == 400
        
        # Invalid priority
        response = client.put(
            f'/api/todos/{todo_id}',
            data=json.dumps({'priority': 'invalid'}),
            content_type='application/json'
        )
        assert response.status_code == 400
    
    def test_delete_todo_success(self, client, create_sample_todos):
        """Test deleting a todo successfully."""
        todos = create_sample_todos
        todo_id = todos[0].id
        
        response = client.delete(f'/api/todos/{todo_id}')
        assert response.status_code == 204
        assert response.data == b''
        
        # Verify todo is deleted
        response = client.get(f'/api/todos/{todo_id}')
        assert response.status_code == 404
    
    def test_delete_todo_not_found(self, client):
        """Test deleting a non-existent todo."""
        response = client.delete('/api/todos/999')
        assert response.status_code == 404
        
        data = json.loads(response.data)
        assert data['success'] is False
        assert data['error']['code'] == 'NOT_FOUND'
    
    def test_get_todo_stats(self, client, create_sample_todos):
        """Test getting todo statistics."""
        response = client.get('/api/todos/stats')
        assert response.status_code == 200
        
        data = json.loads(response.data)
        assert data['success'] is True
        stats = data['data']
        
        assert stats['total_count'] == 4
        assert stats['completed_count'] == 1
        assert stats['pending_count'] == 3
        assert stats['overdue_count'] == 1  # one overdue todo
        assert stats['completion_rate'] == 25.0  # 1/4 * 100
        assert data['message'] == "Statistics retrieved successfully"
    
    def test_get_todo_stats_empty(self, client):
        """Test getting stats when no todos exist."""
        response = client.get('/api/todos/stats')
        assert response.status_code == 200
        
        data = json.loads(response.data)
        stats = data['data']
        
        assert stats['total_count'] == 0
        assert stats['completed_count'] == 0
        assert stats['pending_count'] == 0
        assert stats['overdue_count'] == 0
        assert stats['completion_rate'] == 0
    
    def test_method_not_allowed(self, client):
        """Test method not allowed responses."""
        # PATCH is not allowed
        response = client.patch('/api/todos/1')
        assert response.status_code == 405
        
        data = json.loads(response.data)
        assert data['error']['code'] == 'METHOD_NOT_ALLOWED'
    
    def test_response_format_consistency(self, client, sample_todo_data):
        """Test that all endpoints return consistent response formats."""
        # Create a todo first
        response = client.post(
            '/api/todos',
            data=json.dumps(sample_todo_data),
            content_type='application/json'
        )
        todo_id = json.loads(response.data)['data']['id']
        
        # Test all successful endpoints have consistent format
        endpoints = [
            ('GET', '/api/todos', 200),
            ('GET', f'/api/todos/{todo_id}', 200),
            ('PUT', f'/api/todos/{todo_id}', 200),
            ('GET', '/api/todos/stats', 200)
        ]
        
        for method, url, expected_status in endpoints:
            if method == 'PUT':
                response = client.put(
                    url,
                    data=json.dumps({'title': 'Updated'}),
                    content_type='application/json'
                )
            else:
                response = getattr(client, method.lower())(url)
            
            assert response.status_code == expected_status
            data = json.loads(response.data)
            
            # All successful responses should have these keys
            assert 'success' in data
            assert 'message' in data
            assert data['success'] is True
            
            if 'data' in data:
                assert data['data'] is not None
    
    def test_error_response_format_consistency(self, client):
        """Test that error responses have consistent format."""
        error_endpoints = [
            ('GET', '/api/todos/999', 404),
            ('PUT', '/api/todos/999', 404),
            ('DELETE', '/api/todos/999', 404),
            ('GET', '/api/todos?status=invalid', 400),
            ('POST', '/api/todos', 400)  # missing required data
        ]
        
        for method, url, expected_status in error_endpoints:
            if method == 'PUT':
                response = client.put(
                    url,
                    data=json.dumps({'title': 'Test'}),
                    content_type='application/json'
                )
            elif method == 'POST':
                response = client.post(
                    url,
                    data=json.dumps({}),
                    content_type='application/json'
                )
            else:
                response = getattr(client, method.lower())(url)
            
            assert response.status_code == expected_status
            
            if response.status_code != 204:  # DELETE success returns no content
                data = json.loads(response.data)
                
                # All error responses should have these keys
                assert 'success' in data
                assert 'error' in data
                assert data['success'] is False
                assert 'code' in data['error']
                assert 'message' in data['error']


class TestBulkOperationsAPI:
    """Test class for bulk operations API endpoints."""
    
    def test_bulk_delete_success(self, client, create_sample_todos):
        """Test successful bulk delete operation."""
        create_sample_todos  # Ensure todos are created
        
        # Get fresh todo instances from the database
        all_todos = Todo.query.all()
        todo_ids = [all_todos[0].id, all_todos[1].id]
        
        request_data = {
            'operation': 'delete',
            'todo_ids': todo_ids,
            'options': {'track_progress': True}
        }
        
        response = client.post(
            '/api/todos/bulk',
            data=json.dumps(request_data),
            content_type='application/json'
        )
        assert response.status_code == 200
        
        data = json.loads(response.data)
        assert data['success'] is True
        assert data['data']['success'] is True
        assert data['data']['operation'] == 'delete'
        assert data['data']['processed_count'] == 2
        assert data['data']['failed_count'] == 0
        assert len(data['data']['results']) == 2
        
        # Verify todos were actually deleted
        for todo_id in todo_ids:
            response = client.get(f'/api/todos/{todo_id}')
            assert response.status_code == 404
    
    def test_bulk_mark_complete_success(self, client, create_sample_todos):
        """Test successful bulk mark complete operation."""
        create_sample_todos  # Ensure todos are created
        
        # Get pending todos from fresh database query
        pending_todos = Todo.query.filter_by(status=StatusEnum.PENDING).all()
        pending_todo_ids = [todo.id for todo in pending_todos]
        
        request_data = {
            'operation': 'mark_complete',
            'todo_ids': pending_todo_ids[:2],  # Take first 2 pending todos
            'options': {}
        }
        
        response = client.post(
            '/api/todos/bulk',
            data=json.dumps(request_data),
            content_type='application/json'
        )
        assert response.status_code == 200
        
        data = json.loads(response.data)
        assert data['success'] is True
        assert data['data']['success'] is True
        assert data['data']['operation'] == 'mark_complete'
        assert data['data']['processed_count'] == 2
        assert data['data']['failed_count'] == 0
        
        # Verify todos were marked as complete
        for todo_id in pending_todo_ids[:2]:
            response = client.get(f'/api/todos/{todo_id}')
            todo_data = json.loads(response.data)
            assert todo_data['data']['status'] == 'completed'
    
    def test_bulk_mark_pending_success(self, client, create_sample_todos):
        """Test successful bulk mark pending operation."""
        create_sample_todos  # Ensure todos are created
        
        # Get completed todos from fresh database query
        completed_todos = Todo.query.filter_by(status=StatusEnum.COMPLETED).all()
        completed_todo_ids = [todo.id for todo in completed_todos]
        
        request_data = {
            'operation': 'mark_pending',
            'todo_ids': completed_todo_ids,
            'options': {}
        }
        
        response = client.post(
            '/api/todos/bulk',
            data=json.dumps(request_data),
            content_type='application/json'
        )
        assert response.status_code == 200
        
        data = json.loads(response.data)
        assert data['success'] is True
        assert data['data']['operation'] == 'mark_pending'
        assert data['data']['processed_count'] == 1  # Should be 1 completed todo
        assert data['data']['failed_count'] == 0
        
        # Verify todo was marked as pending
        for todo_id in completed_todo_ids:
            response = client.get(f'/api/todos/{todo_id}')
            todo_data = json.loads(response.data)
            assert todo_data['data']['status'] == 'pending'
    
    def test_bulk_operation_partial_failure(self, client, create_sample_todos):
        """Test bulk operation with some non-existent todos."""
        create_sample_todos  # Ensure todos are created
        
        # Get a valid todo ID from fresh database query
        first_todo = Todo.query.first()
        valid_todo_id = first_todo.id
        invalid_todo_ids = [999, 1000]
        
        request_data = {
            'operation': 'delete',
            'todo_ids': [valid_todo_id] + invalid_todo_ids,
            'options': {}
        }
        
        response = client.post(
            '/api/todos/bulk',
            data=json.dumps(request_data),
            content_type='application/json'
        )
        assert response.status_code == 200
        
        data = json.loads(response.data)
        assert data['success'] is True
        assert data['data']['success'] is False  # Overall operation failed due to rollback
        assert data['data']['operation'] == 'delete'
        assert data['data']['processed_count'] == 0  # Rolled back
        assert data['data']['failed_count'] == 3  # All failed due to rollback
        assert len(data['data']['results']) == 3
        
        # Check individual results
        for result in data['data']['results']:
            assert result['success'] is False
            assert 'error' in result
        
        # Verify the valid todo still exists (due to rollback)
        response = client.get(f'/api/todos/{valid_todo_id}')
        assert response.status_code == 200
    
    def test_bulk_operation_validation_errors(self, client):
        """Test bulk operation validation errors."""
        # Missing operation
        response = client.post(
            '/api/todos/bulk',
            data=json.dumps({'todo_ids': [1, 2, 3]}),
            content_type='application/json'
        )
        assert response.status_code == 400
        data = json.loads(response.data)
        assert data['error']['code'] == 'VALIDATION_ERROR'
        assert 'operation' in data['error']['details']
        
        # Missing todo_ids
        response = client.post(
            '/api/todos/bulk',
            data=json.dumps({'operation': 'delete'}),
            content_type='application/json'
        )
        assert response.status_code == 400
        data = json.loads(response.data)
        assert 'todo_ids' in data['error']['details']
        
        # Invalid operation
        response = client.post(
            '/api/todos/bulk',
            data=json.dumps({
                'operation': 'invalid_operation',
                'todo_ids': [1, 2, 3]
            }),
            content_type='application/json'
        )
        assert response.status_code == 400
        
        # Empty todo_ids
        response = client.post(
            '/api/todos/bulk',
            data=json.dumps({
                'operation': 'delete',
                'todo_ids': []
            }),
            content_type='application/json'
        )
        assert response.status_code == 400
        
        # Too many todo_ids
        response = client.post(
            '/api/todos/bulk',
            data=json.dumps({
                'operation': 'delete',
                'todo_ids': list(range(1, 52))  # 51 items, max is 50
            }),
            content_type='application/json'
        )
        assert response.status_code == 400
        
        # Duplicate todo_ids
        response = client.post(
            '/api/todos/bulk',
            data=json.dumps({
                'operation': 'delete',
                'todo_ids': [1, 2, 2, 3]  # Duplicate 2
            }),
            content_type='application/json'
        )
        assert response.status_code == 400
        
        # Invalid todo_ids (non-integer)
        response = client.post(
            '/api/todos/bulk',
            data=json.dumps({
                'operation': 'delete',
                'todo_ids': [1, 'invalid', 3]
            }),
            content_type='application/json'
        )
        assert response.status_code == 400
        
        # Invalid todo_ids (negative)
        response = client.post(
            '/api/todos/bulk',
            data=json.dumps({
                'operation': 'delete',
                'todo_ids': [1, -2, 3]
            }),
            content_type='application/json'
        )
        assert response.status_code == 400
    
    def test_bulk_operation_invalid_content_type(self, client):
        """Test bulk operation with invalid content type."""
        response = client.post('/api/todos/bulk', data='not json')
        assert response.status_code == 400
        
        data = json.loads(response.data)
        assert data['error']['code'] == 'INVALID_CONTENT_TYPE'
    
    def test_bulk_operation_progress_tracking(self, client, create_sample_todos):
        """Test bulk operation with progress tracking for large operations."""
        create_sample_todos  # Ensure todos are created
        
        # Create additional todos to have more than 10
        for i in range(7):  # We already have 4, so this makes 11 total
            new_todo = Todo(
                title=f"Additional Todo {i}",
                description=f"Description {i}",
                priority=PriorityEnum.MEDIUM,
                status=StatusEnum.PENDING
            )
            db.session.add(new_todo)
        db.session.commit()
        
        # Get all todo IDs
        all_todos = Todo.query.all()
        todo_ids = [todo.id for todo in all_todos]
        
        request_data = {
            'operation': 'mark_complete',
            'todo_ids': todo_ids,
            'options': {'track_progress': True}
        }
        
        response = client.post(
            '/api/todos/bulk',
            data=json.dumps(request_data),
            content_type='application/json'
        )
        assert response.status_code == 200
        
        data = json.loads(response.data)
        assert data['success'] is True
        assert data['data']['progress_id'] is not None
        assert len(data['data']['progress_id']) > 0
    
    def test_bulk_operation_no_progress_tracking_small_operation(self, client, create_sample_todos):
        """Test that progress tracking is not enabled for small operations."""
        create_sample_todos  # Ensure todos are created
        
        # Get todo IDs from fresh database query
        todos = Todo.query.limit(2).all()
        todo_ids = [todos[0].id, todos[1].id]
        
        request_data = {
            'operation': 'delete',
            'todo_ids': todo_ids,
            'options': {'track_progress': True}  # Request tracking but won't be used
        }
        
        response = client.post(
            '/api/todos/bulk',
            data=json.dumps(request_data),
            content_type='application/json'
        )
        assert response.status_code == 200
        
        data = json.loads(response.data)
        assert data['data']['progress_id'] is None  # No progress tracking for <= 10 items
    
    def test_bulk_operation_response_format(self, client, create_sample_todos):
        """Test that bulk operation response has correct format."""
        create_sample_todos  # Ensure todos are created
        
        # Get a todo ID from fresh database query
        first_todo = Todo.query.first()
        todo_ids = [first_todo.id]
        
        request_data = {
            'operation': 'delete',
            'todo_ids': todo_ids,
            'options': {}
        }
        
        response = client.post(
            '/api/todos/bulk',
            data=json.dumps(request_data),
            content_type='application/json'
        )
        assert response.status_code == 200
        
        data = json.loads(response.data)
        
        # Check response structure
        assert 'success' in data
        assert 'message' in data
        assert 'data' in data
        
        # Check bulk operation result structure
        result = data['data']
        assert 'success' in result
        assert 'operation' in result
        assert 'processed_count' in result
        assert 'failed_count' in result
        assert 'results' in result
        assert 'progress_id' in result
        
        # Check individual result structure
        assert len(result['results']) == 1
        individual_result = result['results'][0]
        assert 'todo_id' in individual_result
        assert 'success' in individual_result
        assert 'error' in individual_result
    
    def test_bulk_operation_performance(self, client, create_sample_todos):
        """Test that bulk operations complete within performance requirements."""
        import time
        
        create_sample_todos  # Ensure todos are created
        
        # Create more todos for performance test
        for i in range(20):
            new_todo = Todo(
                title=f"Performance Test Todo {i}",
                description=f"Description {i}",
                priority=PriorityEnum.MEDIUM,
                status=StatusEnum.PENDING
            )
            db.session.add(new_todo)
        db.session.commit()
        
        # Get all todo IDs
        all_todos = Todo.query.all()
        todo_ids = [todo.id for todo in all_todos]
        
        request_data = {
            'operation': 'mark_complete',
            'todo_ids': todo_ids,
            'options': {}
        }
        
        start_time = time.time()
        response = client.post(
            '/api/todos/bulk',
            data=json.dumps(request_data),
            content_type='application/json'
        )
        end_time = time.time()
        
        # Should complete within 10 seconds
        assert (end_time - start_time) < 10
        assert response.status_code == 200