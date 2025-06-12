from flask import Blueprint, jsonify, request
from models import get_all_todos, add_todo, Todo, update_todo, get_todo_by_id, delete_todo

api = Blueprint('api', __name__, url_prefix='/api')

@api.route('/todos', methods=['GET'])
def get_todos():
    """Get all todos"""
    todos = get_all_todos()
    return jsonify([todo.to_dict() for todo in todos])

@api.route('/todos', methods=['POST'])
def create_todo():
    """Create a new todo"""
    data = request.get_json()
    
    # Validate required fields
    if not data or 'text' not in data:
        return jsonify({'error': 'Missing required field: text'}), 400
    
    text = data['text']
    if not text or not text.strip():
        return jsonify({'error': 'Text field cannot be empty'}), 400
    
    try:
        # Create and store new todo
        todo = Todo(text)
        add_todo(todo)
        return jsonify(todo.to_dict()), 201
    except ValueError as e:
        return jsonify({'error': str(e)}), 400

@api.route('/todos/<todo_id>', methods=['PUT'])
def update_todo_endpoint(todo_id):
    """Update an existing todo"""
    # Check if todo exists
    existing_todo = get_todo_by_id(todo_id)
    if not existing_todo:
        return jsonify({'error': 'Todo not found'}), 404
    
    data = request.get_json()
    if not data:
        return jsonify({'error': 'No data provided'}), 400
    
    # Extract optional fields
    text = data.get('text')
    completed = data.get('completed')
    
    # Validate text if provided
    if text is not None:
        if not text or not text.strip():
            return jsonify({'error': 'Text field cannot be empty'}), 400
    
    try:
        # Update todo
        updated_todo = update_todo(todo_id, text=text, completed=completed)
        if updated_todo:
            return jsonify(updated_todo.to_dict()), 200
        else:
            return jsonify({'error': 'Failed to update todo'}), 500
    except ValueError as e:
        return jsonify({'error': str(e)}), 400

@api.route('/todos/<todo_id>', methods=['DELETE'])
def delete_todo_endpoint(todo_id):
    """Delete an existing todo"""
    # Check if todo exists
    existing_todo = get_todo_by_id(todo_id)
    if not existing_todo:
        return jsonify({'error': 'Todo not found'}), 404
    
    # Delete todo
    deleted_todo = delete_todo(todo_id)
    if deleted_todo:
        return jsonify(deleted_todo.to_dict()), 200
    else:
        return jsonify({'error': 'Failed to delete todo'}), 500