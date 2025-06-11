"""
Todo service layer providing business logic for Todo operations.

This module encapsulates the business logic for Todo CRUD operations,
keeping the route handlers thin and focused on HTTP concerns.
"""

from typing import List, Dict, Optional, Tuple
from sqlalchemy.exc import SQLAlchemyError
from datetime import datetime
import uuid
import time
from app import db
from app.models.todo import Todo, PriorityEnum, StatusEnum


class TodoService:
    """Service class for Todo business logic operations."""
    
    @staticmethod
    def get_all_todos(page: int = 1, per_page: int = 20, 
                     status: Optional[str] = None,
                     priority: Optional[str] = None) -> Tuple[List[Todo], Dict]:
        """
        Retrieve all todos with optional filtering and pagination.
        
        Args:
            page (int): Page number (1-based)
            per_page (int): Number of items per page
            status (str, optional): Filter by status ('pending' or 'completed')
            priority (str, optional): Filter by priority ('low', 'medium', 'high')
            
        Returns:
            tuple: (list of todos, pagination info dict)
        """
        try:
            query = Todo.query
            
            # Apply filters
            if status:
                try:
                    status_enum = StatusEnum(status.lower())
                    query = query.filter(Todo.status == status_enum)
                except ValueError:
                    raise ValueError(f"Invalid status: {status}")
            
            if priority:
                try:
                    priority_enum = PriorityEnum(priority.lower())
                    query = query.filter(Todo.priority == priority_enum)
                except ValueError:
                    raise ValueError(f"Invalid priority: {priority}")
            
            # Order by creation date (newest first)
            query = query.order_by(Todo.created_at.desc())
            
            # Apply pagination
            pagination = query.paginate(
                page=page,
                per_page=per_page,
                error_out=False
            )
            
            pagination_info = {
                'page': pagination.page,
                'per_page': pagination.per_page,
                'total': pagination.total,
                'pages': pagination.pages,
                'has_next': pagination.has_next,
                'has_prev': pagination.has_prev
            }
            
            return pagination.items, pagination_info
            
        except SQLAlchemyError as e:
            raise Exception(f"Database error: {str(e)}")
    
    @staticmethod
    def get_todo_by_id(todo_id: int) -> Optional[Todo]:
        """
        Retrieve a specific todo by ID.
        
        Args:
            todo_id (int): The todo ID
            
        Returns:
            Todo or None: The todo if found, None otherwise
        """
        try:
            return Todo.query.get(todo_id)
        except SQLAlchemyError as e:
            raise Exception(f"Database error: {str(e)}")
    
    @staticmethod
    def create_todo(data: Dict) -> Todo:
        """
        Create a new todo.
        
        Args:
            data (dict): Todo data (validated by schema)
            
        Returns:
            Todo: The created todo
            
        Raises:
            ValueError: If data validation fails
            Exception: If database operation fails
        """
        try:
            # Create todo directly with validated data from schema
            todo = Todo(
                title=data['title'],
                description=data.get('description'),
                priority=data.get('priority', PriorityEnum.MEDIUM),
                status=data.get('status', StatusEnum.PENDING),
                due_date=data.get('due_date')
            )
            db.session.add(todo)
            db.session.commit()
            return todo
        except SQLAlchemyError as e:
            db.session.rollback()
            raise Exception(f"Database error: {str(e)}")
    
    @staticmethod
    def update_todo(todo_id: int, data: Dict) -> Optional[Todo]:
        """
        Update an existing todo.
        
        Args:
            todo_id (int): The todo ID
            data (dict): Updated todo data (validated by schema)
            
        Returns:
            Todo or None: The updated todo if found, None otherwise
            
        Raises:
            ValueError: If data validation fails
            Exception: If database operation fails
        """
        try:
            todo = Todo.query.get(todo_id)
            if not todo:
                return None
            
            # Update fields directly with validated data from schema
            if 'title' in data:
                todo.title = data['title']
            if 'description' in data:
                todo.description = data['description']
            if 'priority' in data:
                todo.priority = data['priority']
            if 'status' in data:
                todo.status = data['status']
            if 'due_date' in data:
                todo.due_date = data['due_date']
            
            # Update timestamp
            todo.updated_at = datetime.utcnow()
            
            db.session.commit()
            return todo
        except SQLAlchemyError as e:
            db.session.rollback()
            raise Exception(f"Database error: {str(e)}")
    
    @staticmethod
    def delete_todo(todo_id: int) -> bool:
        """
        Delete a todo (hard delete for MVP).
        
        Args:
            todo_id (int): The todo ID
            
        Returns:
            bool: True if deleted, False if not found
            
        Raises:
            Exception: If database operation fails
        """
        try:
            todo = Todo.query.get(todo_id)
            if not todo:
                return False
            
            db.session.delete(todo)
            db.session.commit()
            return True
        except SQLAlchemyError as e:
            db.session.rollback()
            raise Exception(f"Database error: {str(e)}")
    
    @staticmethod
    def get_todo_stats() -> Dict:
        """
        Get todo statistics.
        
        Returns:
            dict: Statistics including total, completed, pending, and overdue counts
        """
        try:
            from datetime import date
            
            total_count = Todo.query.count()
            completed_count = Todo.query.filter(Todo.status == StatusEnum.COMPLETED).count()
            pending_count = Todo.query.filter(Todo.status == StatusEnum.PENDING).count()
            
            # Count overdue todos (pending todos with due_date < today)
            overdue_count = Todo.query.filter(
                Todo.status == StatusEnum.PENDING,
                Todo.due_date < date.today()
            ).count()
            
            completion_rate = (completed_count / total_count * 100) if total_count > 0 else 0
            
            return {
                'total_count': total_count,
                'completed_count': completed_count,
                'pending_count': pending_count,
                'overdue_count': overdue_count,
                'completion_rate': round(completion_rate, 2)
            }
        except SQLAlchemyError as e:
            raise Exception(f"Database error: {str(e)}")
    
    @staticmethod
    def bulk_operation(operation: str, todo_ids: List[int], options: Dict = None) -> Dict:
        """
        Perform bulk operations on todos.
        
        Args:
            operation (str): The operation to perform ('delete', 'mark_complete', 'mark_pending')
            todo_ids (List[int]): List of todo IDs to operate on
            options (Dict, optional): Additional options for the operation
            
        Returns:
            dict: Operation results with success/failure details for each item
            
        Raises:
            ValueError: If operation is invalid
            Exception: If database operation fails
        """
        if not options:
            options = {}
        
        # Validate operation
        valid_operations = ['delete', 'mark_complete', 'mark_pending']
        if operation not in valid_operations:
            raise ValueError(f"Invalid operation: {operation}")
        
        # Validate todo_ids
        if not todo_ids or len(todo_ids) > 50:
            raise ValueError("todo_ids must contain 1-50 items")
        
        # Generate progress_id for operations > 10 items
        progress_id = None
        if len(todo_ids) > 10 and options.get('track_progress', False):
            progress_id = str(uuid.uuid4())
        
        start_time = time.time()
        results = []
        processed_count = 0
        failed_count = 0
        
        # Use database transaction for atomicity
        try:
            # Get all todos that exist for the given IDs
            existing_todos = Todo.query.filter(Todo.id.in_(todo_ids)).all()
            existing_todo_ids = {todo.id for todo in existing_todos}
            
            # Process each todo_id
            for todo_id in todo_ids:
                try:
                    if todo_id not in existing_todo_ids:
                        # Todo doesn't exist
                        results.append({
                            'todo_id': todo_id,
                            'success': False,
                            'error': f'Todo with id {todo_id} not found'
                        })
                        failed_count += 1
                        continue
                    
                    # Find the todo object
                    todo = next(t for t in existing_todos if t.id == todo_id)
                    
                    # Perform the operation
                    if operation == 'delete':
                        db.session.delete(todo)
                    elif operation == 'mark_complete':
                        todo.status = StatusEnum.COMPLETED
                        todo.updated_at = datetime.utcnow()
                    elif operation == 'mark_pending':
                        todo.status = StatusEnum.PENDING
                        todo.updated_at = datetime.utcnow()
                    
                    results.append({
                        'todo_id': todo_id,
                        'success': True,
                        'error': None
                    })
                    processed_count += 1
                    
                    # Check for timeout (10 seconds max)
                    if time.time() - start_time > 10:
                        raise Exception("Operation timeout exceeded")
                    
                except Exception as e:
                    results.append({
                        'todo_id': todo_id,
                        'success': False,
                        'error': str(e)
                    })
                    failed_count += 1
            
            # If any operation failed, rollback the transaction
            if failed_count > 0:
                db.session.rollback()
                # Reset all results to failed due to rollback
                for result in results:
                    if result['success']:
                        result['success'] = False
                        result['error'] = 'Operation rolled back due to partial failure'
                processed_count = 0
                failed_count = len(todo_ids)
            else:
                # All operations succeeded, commit the transaction
                db.session.commit()
            
            return {
                'success': failed_count == 0,
                'operation': operation,
                'processed_count': processed_count,
                'failed_count': failed_count,
                'results': results,
                'progress_id': progress_id
            }
            
        except SQLAlchemyError as e:
            db.session.rollback()
            raise Exception(f"Database error during bulk operation: {str(e)}")
        except Exception as e:
            db.session.rollback()
            raise Exception(f"Error during bulk operation: {str(e)}")
    
    @staticmethod
    def bulk_delete(todo_ids: List[int], options: Dict = None) -> Dict:
        """
        Bulk delete todos.
        
        Args:
            todo_ids (List[int]): List of todo IDs to delete
            options (Dict, optional): Additional options for the operation
            
        Returns:
            dict: Operation results
        """
        return TodoService.bulk_operation('delete', todo_ids, options)
    
    @staticmethod
    def bulk_mark_complete(todo_ids: List[int], options: Dict = None) -> Dict:
        """
        Bulk mark todos as complete.
        
        Args:
            todo_ids (List[int]): List of todo IDs to mark as complete
            options (Dict, optional): Additional options for the operation
            
        Returns:
            dict: Operation results
        """
        return TodoService.bulk_operation('mark_complete', todo_ids, options)
    
    @staticmethod
    def bulk_mark_pending(todo_ids: List[int], options: Dict = None) -> Dict:
        """
        Bulk mark todos as pending.
        
        Args:
            todo_ids (List[int]): List of todo IDs to mark as pending
            options (Dict, optional): Additional options for the operation
            
        Returns:
            dict: Operation results
        """
        return TodoService.bulk_operation('mark_pending', todo_ids, options)