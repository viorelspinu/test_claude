"""
Database models for the Todo application

Defines the Task model and related database schema.
"""

from datetime import datetime
from app import db


class Task(db.Model):
    """
    Task model representing a single todo item
    
    Attributes:
        id (int): Primary key
        title (str): Task title (required, max 200 chars)
        description (str): Optional task description
        priority (str): Priority level (High, Medium, Low)
        completed (bool): Completion status
        created_at (datetime): Creation timestamp
        updated_at (datetime): Last update timestamp
    """
    
    __tablename__ = 'tasks'
    
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text)
    priority = db.Column(db.String(10), default='Medium')  # High, Medium, Low
    completed = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    def __repr__(self):
        """String representation of Task object"""
        return f'<Task {self.id}: {self.title}>'
    
    def to_dict(self):
        """
        Convert Task object to dictionary for JSON serialization
        
        Returns:
            dict: Task data as dictionary
        """
        return {
            'id': self.id,
            'title': self.title,
            'description': self.description,
            'priority': self.priority,
            'completed': self.completed,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        }
    
    @classmethod
    def from_dict(cls, data):
        """
        Create Task object from dictionary data
        
        Args:
            data (dict): Task data dictionary
            
        Returns:
            Task: New Task instance
        """
        return cls(
            title=data.get('title'),
            description=data.get('description', ''),
            priority=data.get('priority', 'Medium'),
            completed=data.get('completed', False)
        )