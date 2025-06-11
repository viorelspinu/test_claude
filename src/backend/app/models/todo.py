"""
Todo SQLAlchemy model for the Todo application.

This module defines the Todo model with all required fields, validations, and constraints
as specified in the database requirements.
"""

import enum
import uuid
from datetime import datetime
from sqlalchemy import Index, CheckConstraint
from app import db


class PriorityEnum(enum.Enum):
    """Enumeration for todo priority levels."""
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"


class StatusEnum(enum.Enum):
    """Enumeration for todo status values."""
    PENDING = "pending"
    COMPLETED = "completed"


class Todo(db.Model):
    """
    Todo model representing a single todo item.
    
    Attributes:
        id (int): Primary key, auto-incrementing integer
        title (str): Todo title, required, max 200 characters
        description (str): Optional description text
        priority (PriorityEnum): Priority level (low, medium, high)
        status (StatusEnum): Completion status (pending, completed)
        due_date (date): Optional due date
        created_at (datetime): Auto-generated creation timestamp
        updated_at (datetime): Auto-updated modification timestamp
    """
    
    __tablename__ = 'todos'
    
    # Primary key - auto-incrementing integer as specified
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    
    # Title field - required, max 200 characters
    title = db.Column(
        db.String(200), 
        nullable=False,
        doc="Todo title, required field with maximum 200 characters"
    )
    
    # Description field - optional, unlimited length (TEXT type)
    description = db.Column(
        db.Text,
        nullable=True,
        doc="Optional description text with unlimited length"
    )
    
    # Priority field - enum with default 'medium'
    priority = db.Column(
        db.Enum(PriorityEnum),
        nullable=False,
        default=PriorityEnum.MEDIUM,
        doc="Priority level: low, medium, or high"
    )
    
    # Status field - enum with default 'pending'
    status = db.Column(
        db.Enum(StatusEnum),
        nullable=False,
        default=StatusEnum.PENDING,
        doc="Completion status: pending or completed"
    )
    
    # Due date field - optional
    due_date = db.Column(
        db.Date,
        nullable=True,
        doc="Optional due date for the todo"
    )
    
    # Auto-generated timestamps
    created_at = db.Column(
        db.DateTime,
        nullable=False,
        default=datetime.utcnow,
        doc="Auto-generated creation timestamp"
    )
    
    updated_at = db.Column(
        db.DateTime,
        nullable=False,
        default=datetime.utcnow,
        onupdate=datetime.utcnow,
        doc="Auto-updated modification timestamp"
    )
    
    # Table constraints
    __table_args__ = (
        # Check constraint for title not empty
        CheckConstraint(
            "LENGTH(TRIM(title)) > 0",
            name="check_title_not_empty"
        ),
        
        # Database indexes for performance as specified in requirements
        Index('idx_todos_status', 'status'),
        Index('idx_todos_due_date', 'due_date'),
        Index('idx_todos_created_at', 'created_at'),
        Index('idx_todos_status_due_date', 'status', 'due_date'),
    )
    
    def __init__(self, title, description=None, priority=PriorityEnum.MEDIUM, 
                 status=StatusEnum.PENDING, due_date=None):
        """
        Initialize a new Todo instance.
        
        Args:
            title (str): Todo title (required)
            description (str, optional): Todo description
            priority (PriorityEnum, optional): Priority level, defaults to MEDIUM
            status (StatusEnum, optional): Status, defaults to PENDING
            due_date (date, optional): Due date
        """
        self.title = title
        self.description = description
        self.priority = priority
        self.status = status
        self.due_date = due_date
    
    def __repr__(self):
        """Return a string representation of the Todo instance."""
        return f'<Todo {self.id}: "{self.title}" [{self.status.value}]>'
    
    def to_dict(self):
        """
        Convert Todo instance to dictionary for JSON serialization.
        
        Returns:
            dict: Dictionary representation of the Todo
        """
        return {
            'id': self.id,
            'title': self.title,
            'description': self.description,
            'priority': self.priority.value if self.priority else None,
            'status': self.status.value if self.status else None,
            'due_date': self.due_date.isoformat() if self.due_date else None,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        }
    
    @staticmethod
    def from_dict(data):
        """
        Create a Todo instance from dictionary data.
        
        Args:
            data (dict): Dictionary containing todo data
            
        Returns:
            Todo: New Todo instance
            
        Raises:
            ValueError: If required fields are missing or invalid
        """
        if not data.get('title'):
            raise ValueError("Title is required")
        
        if len(data['title'].strip()) == 0:
            raise ValueError("Title cannot be empty")
        
        if len(data['title']) > 200:
            raise ValueError("Title cannot exceed 200 characters")
        
        # Convert string priority to enum
        priority = PriorityEnum.MEDIUM  # default
        if 'priority' in data and data['priority']:
            try:
                priority = PriorityEnum(data['priority'].lower())
            except ValueError:
                raise ValueError(f"Invalid priority: {data['priority']}. Must be low, medium, or high")
        
        # Convert string status to enum
        status = StatusEnum.PENDING  # default
        if 'status' in data and data['status']:
            try:
                status = StatusEnum(data['status'].lower())
            except ValueError:
                raise ValueError(f"Invalid status: {data['status']}. Must be pending or completed")
        
        # Parse due_date if provided
        due_date = None
        if 'due_date' in data and data['due_date']:
            from datetime import datetime as dt
            try:
                due_date = dt.fromisoformat(data['due_date']).date()
            except ValueError:
                raise ValueError("Invalid due_date format. Use ISO format (YYYY-MM-DD)")
        
        return Todo(
            title=data['title'].strip(),
            description=data.get('description', '').strip() if data.get('description') else None,
            priority=priority,
            status=status,
            due_date=due_date
        )
    
    def update_from_dict(self, data):
        """
        Update Todo instance fields from dictionary data.
        
        Args:
            data (dict): Dictionary containing updated todo data
            
        Raises:
            ValueError: If invalid data is provided
        """
        # Update title if provided
        if 'title' in data:
            if not data['title'] or len(data['title'].strip()) == 0:
                raise ValueError("Title cannot be empty")
            if len(data['title']) > 200:
                raise ValueError("Title cannot exceed 200 characters")
            self.title = data['title'].strip()
        
        # Update description if provided
        if 'description' in data:
            self.description = data['description'].strip() if data['description'] else None
        
        # Update priority if provided
        if 'priority' in data and data['priority']:
            try:
                self.priority = PriorityEnum(data['priority'].lower())
            except ValueError:
                raise ValueError(f"Invalid priority: {data['priority']}. Must be low, medium, or high")
        
        # Update status if provided
        if 'status' in data and data['status']:
            try:
                self.status = StatusEnum(data['status'].lower())
            except ValueError:
                raise ValueError(f"Invalid status: {data['status']}. Must be pending or completed")
        
        # Update due_date if provided
        if 'due_date' in data:
            if data['due_date']:
                from datetime import datetime as dt
                try:
                    self.due_date = dt.fromisoformat(data['due_date']).date()
                except ValueError:
                    raise ValueError("Invalid due_date format. Use ISO format (YYYY-MM-DD)")
            else:
                self.due_date = None
        
        # Update the updated_at timestamp
        self.updated_at = datetime.utcnow()
    
    def is_overdue(self):
        """
        Check if the todo is overdue.
        
        Returns:
            bool: True if todo is overdue (has due_date < today and status is pending)
        """
        if not self.due_date or self.status == StatusEnum.COMPLETED:
            return False
        
        from datetime import date
        return self.due_date < date.today()
    
    def mark_completed(self):
        """Mark the todo as completed."""
        self.status = StatusEnum.COMPLETED
        self.updated_at = datetime.utcnow()
    
    def mark_pending(self):
        """Mark the todo as pending."""
        self.status = StatusEnum.PENDING
        self.updated_at = datetime.utcnow()