"""
Todo API route handlers.

This module implements RESTful API endpoints for Todo CRUD operations.
All endpoints follow consistent response formats and proper HTTP status codes.
"""

import logging
from flask import Blueprint, request, jsonify
from marshmallow import ValidationError
from app.services.todo_service import TodoService
from app.schemas.todo import (
    todo_schema, 
    todo_create_schema, 
    todo_update_schema,
    todo_list_schema,
    bulk_operation_schema
)

# Create the todos blueprint
todos_bp = Blueprint('todos', __name__)

# Set up logging
logger = logging.getLogger(__name__)


def create_success_response(data=None, message="Operation completed successfully", status_code=200):
    """Create a standardized success response."""
    response = {
        "success": True,
        "message": message
    }
    if data is not None:
        response["data"] = data
    
    return jsonify(response), status_code


def create_error_response(message, code="UNKNOWN_ERROR", details=None, status_code=400):
    """Create a standardized error response."""
    error_response = {
        "success": False,
        "error": {
            "code": code,
            "message": message
        }
    }
    if details:
        error_response["error"]["details"] = details
    
    return jsonify(error_response), status_code


@todos_bp.route('', methods=['GET'])
def get_todos():
    """
    GET /api/todos - Retrieve all todos with pagination and filtering.
    
    Query Parameters:
        - page (int): Page number (default: 1)
        - per_page (int): Items per page (default: 20, max: 100)
        - status (str): Filter by status ('pending' or 'completed')
        - priority (str): Filter by priority ('low', 'medium', 'high')
    
    Returns:
        200: List of todos with pagination info
        400: Invalid query parameters
        500: Internal server error
    """
    try:
        # Parse query parameters
        page = request.args.get('page', 1, type=int)
        per_page = min(request.args.get('per_page', 20, type=int), 100)  # Max 100 per page
        status = request.args.get('status')
        priority = request.args.get('priority')
        
        # Validate page and per_page
        if page < 1:
            return create_error_response(
                "Page number must be positive",
                "INVALID_PARAMETER",
                status_code=400
            )
        
        if per_page < 1:
            return create_error_response(
                "Per page value must be positive",
                "INVALID_PARAMETER",
                status_code=400
            )
        
        # Get todos from service
        todos, pagination_info = TodoService.get_all_todos(
            page=page,
            per_page=per_page,
            status=status,
            priority=priority
        )
        
        # Serialize todos
        serialized_todos = todo_schema.dump(todos, many=True)
        
        # Create response
        response_data = {
            "todos": serialized_todos,
            "pagination": pagination_info
        }
        
        return create_success_response(
            data=response_data,
            message="Todos retrieved successfully"
        )
        
    except ValueError as e:
        logger.warning(f"Invalid parameter in get_todos: {str(e)}")
        return create_error_response(
            str(e),
            "INVALID_PARAMETER",
            status_code=400
        )
    except Exception as e:
        logger.error(f"Error in get_todos: {str(e)}")
        return create_error_response(
            "Failed to retrieve todos",
            "INTERNAL_ERROR",
            status_code=500
        )


@todos_bp.route('/<int:todo_id>', methods=['GET'])
def get_todo(todo_id):
    """
    GET /api/todos/{id} - Retrieve a specific todo by ID.
    
    Args:
        todo_id (int): The todo ID
    
    Returns:
        200: Todo object
        404: Todo not found
        500: Internal server error
    """
    try:
        todo = TodoService.get_todo_by_id(todo_id)
        
        if not todo:
            return create_error_response(
                f"Todo with id {todo_id} not found",
                "NOT_FOUND",
                status_code=404
            )
        
        serialized_todo = todo_schema.dump(todo)
        
        return create_success_response(
            data=serialized_todo,
            message="Todo retrieved successfully"
        )
        
    except Exception as e:
        logger.error(f"Error in get_todo: {str(e)}")
        return create_error_response(
            "Failed to retrieve todo",
            "INTERNAL_ERROR",
            status_code=500
        )


@todos_bp.route('', methods=['POST'])
def create_todo():
    """
    POST /api/todos - Create a new todo.
    
    Request Body:
        {
            "title": "string (required, 1-200 chars)",
            "description": "string (optional, max 1000 chars)",
            "priority": "low|medium|high (optional, default: medium)",
            "due_date": "YYYY-MM-DD (optional)"
        }
    
    Returns:
        201: Created todo object
        400: Validation error
        500: Internal server error
    """
    try:
        # Validate request has JSON content
        if not request.is_json:
            return create_error_response(
                "Request must contain JSON data",
                "INVALID_CONTENT_TYPE",
                status_code=400
            )
        
        # Parse and validate request data
        try:
            data = todo_create_schema.load(request.json)
        except ValidationError as e:
            return create_error_response(
                "Validation failed",
                "VALIDATION_ERROR",
                details=e.messages,
                status_code=400
            )
        
        # Create todo via service
        todo = TodoService.create_todo(data)
        
        # Serialize response
        serialized_todo = todo_schema.dump(todo)
        
        return create_success_response(
            data=serialized_todo,
            message="Todo created successfully",
            status_code=201
        )
        
    except ValueError as e:
        logger.warning(f"Validation error in create_todo: {str(e)}")
        return create_error_response(
            str(e),
            "VALIDATION_ERROR",
            status_code=400
        )
    except Exception as e:
        logger.error(f"Error in create_todo: {str(e)}")
        return create_error_response(
            "Failed to create todo",
            "INTERNAL_ERROR",
            status_code=500
        )


@todos_bp.route('/<int:todo_id>', methods=['PUT'])
def update_todo(todo_id):
    """
    PUT /api/todos/{id} - Update an existing todo.
    
    Args:
        todo_id (int): The todo ID
    
    Request Body:
        {
            "title": "string (optional, 1-200 chars)",
            "description": "string (optional, max 1000 chars)",
            "priority": "low|medium|high (optional)",
            "status": "pending|completed (optional)",
            "due_date": "YYYY-MM-DD (optional)"
        }
    
    Returns:
        200: Updated todo object
        400: Validation error
        404: Todo not found
        500: Internal server error
    """
    try:
        # Validate request has JSON content
        if not request.is_json:
            return create_error_response(
                "Request must contain JSON data",
                "INVALID_CONTENT_TYPE",
                status_code=400
            )
        
        # Parse and validate request data
        try:
            data = todo_update_schema.load(request.json)
        except ValidationError as e:
            return create_error_response(
                "Validation failed",
                "VALIDATION_ERROR",
                details=e.messages,
                status_code=400
            )
        
        # Update todo via service
        todo = TodoService.update_todo(todo_id, data)
        
        if not todo:
            return create_error_response(
                f"Todo with id {todo_id} not found",
                "NOT_FOUND",
                status_code=404
            )
        
        # Serialize response
        serialized_todo = todo_schema.dump(todo)
        
        return create_success_response(
            data=serialized_todo,
            message="Todo updated successfully"
        )
        
    except ValueError as e:
        logger.warning(f"Validation error in update_todo: {str(e)}")
        return create_error_response(
            str(e),
            "VALIDATION_ERROR",
            status_code=400
        )
    except Exception as e:
        logger.error(f"Error in update_todo: {str(e)}")
        return create_error_response(
            "Failed to update todo",
            "INTERNAL_ERROR",
            status_code=500
        )


@todos_bp.route('/<int:todo_id>', methods=['DELETE'])
def delete_todo(todo_id):
    """
    DELETE /api/todos/{id} - Delete a todo.
    
    Args:
        todo_id (int): The todo ID
    
    Returns:
        204: Todo deleted successfully
        404: Todo not found
        500: Internal server error
    """
    try:
        # Delete todo via service
        deleted = TodoService.delete_todo(todo_id)
        
        if not deleted:
            return create_error_response(
                f"Todo with id {todo_id} not found",
                "NOT_FOUND",
                status_code=404
            )
        
        # Return 204 No Content for successful deletion
        return '', 204
        
    except Exception as e:
        logger.error(f"Error in delete_todo: {str(e)}")
        return create_error_response(
            "Failed to delete todo",
            "INTERNAL_ERROR",
            status_code=500
        )


@todos_bp.route('/stats', methods=['GET'])
def get_todo_stats():
    """
    GET /api/todos/stats - Get todo statistics.
    
    Returns:
        200: Statistics object with counts and completion rate
        500: Internal server error
    """
    try:
        stats = TodoService.get_todo_stats()
        
        return create_success_response(
            data=stats,
            message="Statistics retrieved successfully"
        )
        
    except Exception as e:
        logger.error(f"Error in get_todo_stats: {str(e)}")
        return create_error_response(
            "Failed to retrieve statistics",
            "INTERNAL_ERROR",
            status_code=500
        )


@todos_bp.route('/bulk', methods=['POST'])
def bulk_operations():
    """
    POST /api/todos/bulk - Perform bulk operations on todos.
    
    Request Body:
        {
            "operation": "delete|mark_complete|mark_pending",
            "todo_ids": [1, 2, 3, ...],
            "options": {
                "track_progress": boolean
            }
        }
    
    Returns:
        200: Bulk operation results
        400: Validation error
        500: Internal server error
    """
    try:
        # Validate request has JSON content
        if not request.is_json:
            return create_error_response(
                "Request must contain JSON data",
                "INVALID_CONTENT_TYPE",
                status_code=400
            )
        
        # Parse and validate request data
        try:
            data = bulk_operation_schema.load(request.json)
        except ValidationError as e:
            return create_error_response(
                "Validation failed",
                "VALIDATION_ERROR",
                details=e.messages,
                status_code=400
            )
        
        # Perform bulk operation via service
        result = TodoService.bulk_operation(
            operation=data['operation'],
            todo_ids=data['todo_ids'],
            options=data.get('options', {})
        )
        
        # Create response based on overall success
        if result['success']:
            message = f"Bulk {data['operation']} completed successfully"
            status_code = 200
        else:
            message = f"Bulk {data['operation']} completed with errors"
            status_code = 200  # Still 200 as request was processed
        
        return create_success_response(
            data=result,
            message=message,
            status_code=status_code
        )
        
    except ValueError as e:
        logger.warning(f"Validation error in bulk_operations: {str(e)}")
        return create_error_response(
            str(e),
            "VALIDATION_ERROR",
            status_code=400
        )
    except Exception as e:
        logger.error(f"Error in bulk_operations: {str(e)}")
        return create_error_response(
            "Failed to perform bulk operation",
            "INTERNAL_ERROR",
            status_code=500
        )


# Error handlers for the blueprint
@todos_bp.errorhandler(404)
def handle_not_found(e):
    """Handle 404 errors within the todos blueprint."""
    return create_error_response(
        "The requested todo resource was not found",
        "NOT_FOUND",
        status_code=404
    )


@todos_bp.errorhandler(405)
def handle_method_not_allowed(e):
    """Handle 405 Method Not Allowed errors."""
    return create_error_response(
        "Method not allowed for this endpoint",
        "METHOD_NOT_ALLOWED",
        status_code=405
    )