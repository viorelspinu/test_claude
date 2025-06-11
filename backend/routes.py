from flask import Blueprint, jsonify, request

api = Blueprint('api', __name__)

# Sample data for testing
sample_todos = [
    {"id": 1, "title": "Learn Flask", "description": "Build todo API", "completed": False, "created_at": "2025-01-06T10:00:00"},
    {"id": 2, "title": "Setup React", "description": "Create frontend", "completed": False, "created_at": "2025-01-06T10:30:00"},
    {"id": 3, "title": "Connect Frontend to Backend", "description": "Integrate API calls", "completed": False, "created_at": "2025-01-06T11:00:00"}
]

@api.route('/todos', methods=['GET'])
def get_todos():
    """Get all todos"""
    return jsonify({
        'success': True,
        'data': sample_todos,
        'message': 'Todos retrieved successfully'
    }), 200

@api.route('/todos', methods=['POST'])
def create_todo():
    """Create a new todo"""
    try:
        data = request.get_json()
        
        if not data or 'title' not in data:
            return jsonify({
                'success': False,
                'message': 'Title is required'
            }), 400
        
        # Generate new ID
        new_id = max([todo['id'] for todo in sample_todos]) + 1 if sample_todos else 1
        
        new_todo = {
            'id': new_id,
            'title': data['title'],
            'description': data.get('description', ''),
            'completed': data.get('completed', False),
            'created_at': '2025-01-06T12:00:00'
        }
        
        sample_todos.append(new_todo)
        
        return jsonify({
            'success': True,
            'data': new_todo,
            'message': 'Todo created successfully'
        }), 201
        
    except Exception as e:
        return jsonify({
            'success': False,
            'message': f'Error creating todo: {str(e)}'
        }), 500

@api.route('/todos/<int:todo_id>', methods=['PUT'])
def update_todo(todo_id):
    """Update an existing todo"""
    try:
        data = request.get_json()
        
        # Find todo by ID
        todo = next((t for t in sample_todos if t['id'] == todo_id), None)
        
        if not todo:
            return jsonify({
                'success': False,
                'message': 'Todo not found'
            }), 404
        
        # Update todo fields
        if 'title' in data:
            todo['title'] = data['title']
        if 'description' in data:
            todo['description'] = data['description']
        if 'completed' in data:
            todo['completed'] = data['completed']
        
        return jsonify({
            'success': True,
            'data': todo,
            'message': 'Todo updated successfully'
        }), 200
        
    except Exception as e:
        return jsonify({
            'success': False,
            'message': f'Error updating todo: {str(e)}'
        }), 500

@api.route('/todos/<int:todo_id>', methods=['DELETE'])
def delete_todo(todo_id):
    """Delete a todo"""
    try:
        # Find todo by ID
        todo = next((t for t in sample_todos if t['id'] == todo_id), None)
        
        if not todo:
            return jsonify({
                'success': False,
                'message': 'Todo not found'
            }), 404
        
        sample_todos.remove(todo)
        
        return jsonify({
            'success': True,
            'message': 'Todo deleted successfully'
        }), 200
        
    except Exception as e:
        return jsonify({
            'success': False,
            'message': f'Error deleting todo: {str(e)}'
        }), 500