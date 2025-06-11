"""
Marshmallow schemas for Todo API request validation and response serialization.

This module defines schemas for creating, updating, and serializing Todo objects,
ensuring data integrity and consistent API interfaces.
"""

from datetime import date
from marshmallow import Schema, fields, validate, ValidationError, pre_load, post_load, post_dump
from app.models.todo import PriorityEnum, StatusEnum


class EnumField(fields.Field):
    """Custom field for serializing enum values."""
    
    def __init__(self, enum_class, *args, **kwargs):
        self.enum_class = enum_class
        super().__init__(*args, **kwargs)
    
    def _serialize(self, value, attr, obj, **kwargs):
        if value is None:
            return None
        if hasattr(value, 'value'):
            return value.value
        return value
    
    def _deserialize(self, value, attr, data, **kwargs):
        if value is None:
            return None
        try:
            return self.enum_class(value.lower() if isinstance(value, str) else value)
        except ValueError:
            raise ValidationError(f'Invalid value for {self.enum_class.__name__}: {value}')


class TodoSchema(Schema):
    """Base schema for Todo serialization and validation."""
    
    id = fields.Integer(dump_only=True)
    title = fields.String(
        required=True,
        validate=validate.Length(min=1, max=200)
    )
    description = fields.String(
        allow_none=True,
        validate=validate.Length(max=1000)
    )
    priority = EnumField(PriorityEnum, allow_none=True)
    status = EnumField(StatusEnum, allow_none=True)
    due_date = fields.Date(allow_none=True)
    created_at = fields.DateTime(dump_only=True)
    updated_at = fields.DateTime(dump_only=True)
    
    @pre_load
    def process_input(self, data, **kwargs):
        """Pre-process input data."""
        # Strip whitespace from string fields
        if 'title' in data and data['title']:
            data['title'] = data['title'].strip()
        if 'description' in data and data['description']:
            data['description'] = data['description'].strip()
        
        return data
    
    def validate_due_date(self, value):
        """Validate that due_date is not in the past."""
        if value and value < date.today():
            raise ValidationError("Due date cannot be in the past")
        return value


class TodoCreateSchema(TodoSchema):
    """Schema for creating new todos."""
    
    # Remove dump_only fields for creation
    id = fields.Integer(dump_only=True)
    created_at = fields.DateTime(dump_only=True)
    updated_at = fields.DateTime(dump_only=True)
    
    # Make title required for creation
    title = fields.String(
        required=True,
        validate=validate.Length(min=1, max=200),
        error_messages={
            'required': 'Title is required',
            'invalid': 'Title must be a string'
        }
    )


class TodoUpdateSchema(Schema):
    """Schema for updating existing todos."""
    
    title = fields.String(validate=validate.Length(min=1, max=200))
    description = fields.String(
        allow_none=True,
        validate=validate.Length(max=1000)
    )
    priority = EnumField(PriorityEnum, allow_none=True)
    status = EnumField(StatusEnum, allow_none=True)
    due_date = fields.Date(allow_none=True)
    
    @pre_load
    def process_input(self, data, **kwargs):
        """Pre-process input data."""
        # Strip whitespace from string fields
        if 'title' in data and data['title']:
            data['title'] = data['title'].strip()
        if 'description' in data and data['description']:
            data['description'] = data['description'].strip()
        
        return data
    
    def validate_due_date(self, value):
        """Validate that due_date is not in the past."""
        if value and value < date.today():
            raise ValidationError("Due date cannot be in the past")
        return value


class TodoListSchema(Schema):
    """Schema for todo list responses with pagination."""
    
    success = fields.Boolean()
    data = fields.List(fields.Nested(TodoSchema))
    message = fields.String()
    pagination = fields.Dict()


class ErrorSchema(Schema):
    """Schema for error responses."""
    
    success = fields.Boolean()
    error = fields.Dict(required=True)


class SuccessResponseSchema(Schema):
    """Schema for successful API responses."""
    
    success = fields.Boolean()
    data = fields.Raw()
    message = fields.String()


# Schema instances for reuse
todo_schema = TodoSchema()
todo_create_schema = TodoCreateSchema()
todo_update_schema = TodoUpdateSchema()
todo_list_schema = TodoListSchema()
class BulkOperationSchema(Schema):
    """Schema for bulk operation requests."""
    
    operation = fields.String(
        required=True,
        validate=validate.OneOf(['delete', 'mark_complete', 'mark_pending']),
        error_messages={
            'required': 'Operation is required',
            'invalid': 'Operation must be delete, mark_complete, or mark_pending'
        }
    )
    todo_ids = fields.List(
        fields.Integer(strict=True),
        required=True,
        validate=validate.Length(min=1, max=50),
        error_messages={
            'required': 'Todo IDs are required',
            'invalid': 'Todo IDs must be a list of integers'
        }
    )
    options = fields.Dict(load_default=dict)
    
    @pre_load
    def validate_todo_ids(self, data, **kwargs):
        """Validate todo_ids array."""
        if 'todo_ids' in data:
            if not isinstance(data['todo_ids'], list):
                raise ValidationError("todo_ids must be a list")
            
            # Check for duplicates
            if len(data['todo_ids']) != len(set(data['todo_ids'])):
                raise ValidationError("Duplicate todo IDs are not allowed")
            
            # Check for valid integers
            for todo_id in data['todo_ids']:
                if not isinstance(todo_id, int) or todo_id <= 0:
                    raise ValidationError("All todo IDs must be positive integers")
        
        return data


class BulkOperationResponseSchema(Schema):
    """Schema for bulk operation responses."""
    
    success = fields.Boolean()
    operation = fields.String()
    processed_count = fields.Integer()
    failed_count = fields.Integer()
    results = fields.List(fields.Dict())
    progress_id = fields.String(allow_none=True)


error_schema = ErrorSchema()
success_response_schema = SuccessResponseSchema()
bulk_operation_schema = BulkOperationSchema()
bulk_operation_response_schema = BulkOperationResponseSchema()