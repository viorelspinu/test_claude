"""
API Routes for Todo Application

This module implements all the RESTful API endpoints for task management
according to the API contract specifications in parallel_dev_sync.md
"""

from flask import request, jsonify
from datetime import datetime
from sqlalchemy import or_, desc, asc
from app.api import api_bp
from app.models import Task
from app.extensions import db


@api_bp.route('/health', methods=['GET'])
def health_check():
    """
    GET /api/health - Health check endpoint
    """
    return jsonify({
        "status": "healthy",
        "message": "Todo API is running",
        "timestamp": datetime.utcnow().isoformat()
    })


def create_error_response(code, message, details=None, status_code=400):
    """
    Create standardized error response
    
    Args:
        code (str): Error code
        message (str): Human-readable error message
        details (dict): Optional field-specific error details
        status_code (int): HTTP status code
        
    Returns:
        tuple: (response_dict, status_code)
    """
    error_response = {
        "error": {
            "code": code,
            "message": message
        }
    }
    if details:
        error_response["error"]["details"] = details
    
    return jsonify(error_response), status_code


def create_success_response(data, meta=None):
    """
    Create standardized success response
    
    Args:
        data: Response data
        meta (dict): Optional metadata (pagination, etc.)
        
    Returns:
        dict: Formatted success response
    """
    response = {"data": data}
    if meta:
        response["meta"] = meta
    return response


def validate_task_data(data, required_fields=None):
    """
    Validate task data according to API contract
    
    Args:
        data (dict): Task data to validate
        required_fields (list): List of required fields
        
    Returns:
        tuple: (is_valid, errors_dict)
    """
    errors = {}
    
    if required_fields:
        for field in required_fields:
            if field not in data or not data[field]:
                errors[field] = f"{field} is required"
    
    # Validate title
    if 'title' in data:
        title = data['title'].strip() if data['title'] else ''
        if not title:
            errors['title'] = "Title cannot be empty"
        elif len(title) > 200:
            errors['title'] = "Title cannot exceed 200 characters"
    
    # Validate description
    if 'description' in data and data['description'] and len(data['description']) > 1000:
        errors['description'] = "Description cannot exceed 1000 characters"
    
    # Validate priority
    if 'priority' in data and data['priority'] not in ['High', 'Medium', 'Low']:
        errors['priority'] = "Priority must be one of: High, Medium, Low"
    
    # Validate completed (if present)
    if 'completed' in data and not isinstance(data['completed'], bool):
        errors['completed'] = "Completed must be a boolean value"
    
    return len(errors) == 0, errors


@api_bp.route('/tasks', methods=['GET'])
def get_tasks():
    """
    GET /api/tasks - Retrieve filtered and sorted task list
    
    Query Parameters:
        completed: 'true' or 'false' - Filter by completion status
        priority: 'High', 'Medium', or 'Low' - Filter by priority
        search: string - Search in title and description
        sort: 'created_at', 'updated_at', 'title', 'priority' - Sort field
        order: 'asc' or 'desc' - Sort order
        limit: int - Max items to return (default: 100)
        offset: int - Pagination offset (default: 0)
    """
    try:
        # Parse query parameters
        completed_filter = request.args.get('completed')
        priority_filter = request.args.get('priority')
        search_query = request.args.get('search', '').strip()
        sort_field = request.args.get('sort', 'created_at')
        sort_order = request.args.get('order', 'desc')
        
        # Handle pagination parameters
        page = int(request.args.get('page', 1))
        per_page = int(request.args.get('per_page', request.args.get('limit', 100)))
        limit = per_page
        offset = (page - 1) * per_page if page > 0 else 0
        
        # Validate parameters
        if sort_field not in ['created_at', 'updated_at', 'title', 'priority']:
            return create_error_response(
                "INVALID_SORT_FIELD",
                "Sort field must be one of: created_at, updated_at, title, priority",
                status_code=400
            )
        
        if sort_order not in ['asc', 'desc']:
            return create_error_response(
                "INVALID_SORT_ORDER",
                "Sort order must be 'asc' or 'desc'",
                status_code=400
            )
        
        if limit < 1 or limit > 1000:
            return create_error_response(
                "INVALID_LIMIT",
                "Limit must be between 1 and 1000",
                status_code=400
            )
        
        # Build query
        query = Task.query
        
        # Apply filters
        if completed_filter is not None:
            if completed_filter.lower() == 'true':
                query = query.filter(Task.completed == True)
            elif completed_filter.lower() == 'false':
                query = query.filter(Task.completed == False)
        
        if priority_filter and priority_filter in ['High', 'Medium', 'Low']:
            query = query.filter(Task.priority == priority_filter)
        
        if search_query:
            search_pattern = f"%{search_query}%"
            query = query.filter(or_(
                Task.title.ilike(search_pattern),
                Task.description.ilike(search_pattern)
            ))
        
        # Get total count before pagination
        total_count = query.count()
        
        # Apply sorting
        sort_column = getattr(Task, sort_field)
        if sort_order == 'desc':
            query = query.order_by(desc(sort_column))
        else:
            query = query.order_by(asc(sort_column))
        
        # Apply pagination
        query = query.offset(offset).limit(limit)
        
        # Execute query
        tasks = query.all()
        
        # Prepare response
        task_list = [task.to_dict() for task in tasks]
        
        # Calculate pagination info
        current_page = page
        total_pages = (total_count + per_page - 1) // per_page if per_page > 0 else 1
        has_next = current_page < total_pages
        has_prev = current_page > 1
        
        response_data = {
            "tasks": task_list,
            "pagination": {
                "total": total_count,
                "page": current_page,
                "per_page": per_page,
                "pages": total_pages,
                "has_next": has_next,
                "has_prev": has_prev
            }
        }
        
        return jsonify(response_data)
        
    except ValueError as e:
        return create_error_response(
            "INVALID_PARAMETER",
            "Invalid parameter format",
            {"parameter": str(e)},
            status_code=400
        )
    except Exception as e:
        return create_error_response(
            "INTERNAL_ERROR",
            "An internal error occurred",
            status_code=500
        )


@api_bp.route('/tasks', methods=['POST'])
def create_task():
    """
    POST /api/tasks - Create new task
    
    Request Body:
        title (required): string - Task title
        description (optional): string - Task description
        priority (optional): string - Task priority (High, Medium, Low)
    """
    try:
        data = request.get_json()
        
        if not data:
            return create_error_response(
                "INVALID_JSON",
                "Request body must contain valid JSON",
                status_code=400
            )
        
        # Validate required fields and data
        is_valid, errors = validate_task_data(data, required_fields=['title'])
        
        if not is_valid:
            if 'title' in errors:
                return create_error_response(
                    "MISSING_TITLE",
                    errors['title'],
                    status_code=400
                )
            if 'priority' in errors:
                return create_error_response(
                    "INVALID_PRIORITY",
                    errors['priority'],
                    status_code=400
                )
            return create_error_response(
                "VALIDATION_ERROR",
                "Invalid task data",
                errors,
                status_code=400
            )
        
        # Create new task
        task = Task(
            title=data['title'].strip(),
            description=data.get('description', '').strip() or None,
            priority=data.get('priority', 'Medium'),
            completed=data.get('completed', False)
        )
        
        # Set completed_at if task is created as completed
        if data.get('completed', False):
            task.completed_at = datetime.utcnow()
        
        # Save to database
        db.session.add(task)
        db.session.commit()
        
        # Return created task
        return jsonify({"task": task.to_dict()}), 201
        
    except Exception as e:
        db.session.rollback()
        return create_error_response(
            "INTERNAL_ERROR",
            "An error occurred while creating the task",
            status_code=500
        )


@api_bp.route('/tasks/<int:task_id>', methods=['PUT'])
def update_task(task_id):
    """
    PUT /api/tasks/{id} - Update existing task
    
    Request Body (all fields optional):
        title: string - Task title
        description: string - Task description
        priority: string - Task priority (High, Medium, Low)
        completed: boolean - Completion status
    """
    try:
        # Find task
        task = Task.query.get(task_id)
        if not task:
            return create_error_response(
                "TASK_NOT_FOUND",
                f"Task with id {task_id} not found",
                status_code=404
            )
        
        data = request.get_json()
        
        if not data:
            return create_error_response(
                "INVALID_JSON",
                "Request body must contain valid JSON",
                status_code=400
            )
        
        # Validate data
        is_valid, errors = validate_task_data(data)
        
        if not is_valid:
            return create_error_response(
                "VALIDATION_ERROR",
                "Invalid task data",
                errors,
                status_code=422
            )
        
        # Track if completed status changed to set completed_at
        was_completed = task.completed
        
        # Update task fields
        if 'title' in data:
            task.title = data['title'].strip()
        
        if 'description' in data:
            task.description = data['description'].strip() or None
        
        if 'priority' in data:
            task.priority = data['priority']
        
        if 'completed' in data:
            task.completed = data['completed']
            
            # Set completed_at timestamp
            if data['completed'] and not was_completed:
                # Task was just completed
                task.completed_at = datetime.utcnow()
            elif not data['completed'] and was_completed:
                # Task was uncompleted
                task.completed_at = None
        
        # Update timestamp
        task.updated_at = datetime.utcnow()
        
        # Save changes
        db.session.commit()
        
        return jsonify({"task": task.to_dict()})
        
    except Exception as e:
        db.session.rollback()
        return create_error_response(
            "INTERNAL_ERROR",
            "An error occurred while updating the task",
            status_code=500
        )


@api_bp.route('/tasks/<int:task_id>', methods=['DELETE'])
def delete_task(task_id):
    """
    DELETE /api/tasks/{id} - Delete task
    """
    try:
        # Find task
        task = Task.query.get(task_id)
        if not task:
            return create_error_response(
                "TASK_NOT_FOUND",
                f"Task with id {task_id} not found",
                status_code=404
            )
        
        # Delete task
        db.session.delete(task)
        db.session.commit()
        
        return '', 204
        
    except Exception as e:
        db.session.rollback()
        return create_error_response(
            "INTERNAL_ERROR",
            "An error occurred while deleting the task",
            status_code=500
        )


@api_bp.route('/tasks/<int:task_id>', methods=['GET'])
def get_task(task_id):
    """
    GET /api/tasks/{id} - Get specific task
    """
    try:
        task = Task.query.get(task_id)
        if not task:
            return create_error_response(
                "TASK_NOT_FOUND",
                f"Task with id {task_id} not found",
                status_code=404
            )
        
        return jsonify({"task": task.to_dict()})
        
    except Exception as e:
        return create_error_response(
            "INTERNAL_ERROR",
            "An error occurred while retrieving the task",
            status_code=500
        )


@api_bp.route('/tasks/bulk', methods=['PUT'])
def bulk_update_tasks():
    """
    PUT /api/tasks/bulk - Bulk update tasks
    """
    try:
        data = request.get_json()
        
        if not data or 'task_ids' not in data or 'updates' not in data:
            return create_error_response(
                "INVALID_REQUEST",
                "Request must contain task_ids and updates",
                status_code=400
            )
        
        task_ids = data['task_ids']
        updates = data['updates']
        
        # Validate updates
        is_valid, errors = validate_task_data(updates)
        if not is_valid:
            return create_error_response(
                "VALIDATION_ERROR",
                "Invalid update data",
                errors,
                status_code=422
            )
        
        # Get tasks to update
        tasks = Task.query.filter(Task.id.in_(task_ids)).all()
        
        updated_tasks = []
        for task in tasks:
            # Apply updates
            if 'title' in updates:
                task.title = updates['title'].strip()
            if 'description' in updates:
                task.description = updates['description'].strip() or None
            if 'priority' in updates:
                task.priority = updates['priority']
            if 'completed' in updates:
                task.completed = updates['completed']
                if updates['completed'] and not task.completed_at:
                    task.completed_at = datetime.utcnow()
                elif not updates['completed']:
                    task.completed_at = None
            
            task.updated_at = datetime.utcnow()
            updated_tasks.append(task.to_dict())
        
        db.session.commit()
        
        return jsonify({"tasks": updated_tasks})
        
    except Exception as e:
        db.session.rollback()
        return create_error_response(
            "INTERNAL_ERROR",
            "An error occurred while updating tasks",
            status_code=500
        )


@api_bp.route('/tasks/stats', methods=['GET'])
def get_task_stats():
    """
    GET /api/tasks/stats - Retrieve task statistics
    """
    try:
        # Get basic counts
        total_tasks = Task.query.count()
        completed_tasks = Task.query.filter(Task.completed == True).count()
        pending_tasks = total_tasks - completed_tasks
        
        # Calculate completion rate
        completion_rate = (completed_tasks / total_tasks * 100) if total_tasks > 0 else 0
        completion_rate = round(completion_rate, 2)
        
        # Get priority breakdown
        high_priority = Task.query.filter(Task.priority == 'High').count()
        medium_priority = Task.query.filter(Task.priority == 'Medium').count()
        low_priority = Task.query.filter(Task.priority == 'Low').count()
        
        stats_data = {
            "total_tasks": total_tasks,
            "completed_tasks": completed_tasks,
            "pending_tasks": pending_tasks,
            "completion_rate": completion_rate,
            "priority_breakdown": {
                "high": high_priority,
                "medium": medium_priority,
                "low": low_priority
            }
        }
        
        return jsonify({"stats": stats_data})
        
    except Exception as e:
        return create_error_response(
            "INTERNAL_ERROR",
            "An error occurred while retrieving task statistics",
            status_code=500
        )