"""
Marshmallow schemas package for the Todo application.

This package contains schema definitions for request/response validation and serialization.
Schemas ensure data integrity and provide consistent API interfaces.
"""

from .todo import (
    TodoSchema, 
    TodoCreateSchema, 
    TodoUpdateSchema,
    TodoListSchema,
    ErrorSchema,
    SuccessResponseSchema,
    todo_schema,
    todo_create_schema,
    todo_update_schema,
    todo_list_schema,
    error_schema,
    success_response_schema
)