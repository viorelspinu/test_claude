from flask import Flask, request, jsonify
from flask_cors import CORS
from database import (
    init_database, get_all_todos, create_todo, 
    update_todo, delete_todo, get_todo_by_id
)

app = Flask(__name__)
CORS(app)

# Initialize database on startup
init_database()

@app.route('/')
def hello_world():
    return {'message': 'Todo API Server Running!'}

@app.route('/api/health')
def health_check():
    return {'status': 'healthy'}

@app.route('/api/todos', methods=['GET'])
def get_todos():
    """Get all todos."""
    try:
        todos = get_all_todos()
        return jsonify(todos), 200
    except Exception as e:
        return jsonify({'error': 'Failed to retrieve todos'}), 500

@app.route('/api/todos', methods=['POST'])
def create_new_todo():
    """Create a new todo."""
    try:
        data = request.get_json()
        
        if not data or 'text' not in data:
            return jsonify({'error': 'Missing required field: text'}), 400
        
        text = data['text'].strip()
        if not text:
            return jsonify({'error': 'Todo text cannot be empty'}), 400
        
        todo = create_todo(text)
        return jsonify(todo), 201
    
    except Exception as e:
        return jsonify({'error': 'Failed to create todo'}), 500

@app.route('/api/todos/<int:todo_id>', methods=['PUT'])
def update_existing_todo(todo_id):
    """Update a todo's completion status."""
    try:
        data = request.get_json()
        
        if not data or 'completed' not in data:
            return jsonify({'error': 'Missing required field: completed'}), 400
        
        completed = bool(data['completed'])
        
        todo = update_todo(todo_id, completed)
        if todo is None:
            return jsonify({'error': 'Todo not found'}), 404
        
        return jsonify(todo), 200
    
    except Exception as e:
        return jsonify({'error': 'Failed to update todo'}), 500

@app.route('/api/todos/<int:todo_id>', methods=['DELETE'])
def delete_existing_todo(todo_id):
    """Delete a todo."""
    try:
        deleted = delete_todo(todo_id)
        
        if not deleted:
            return jsonify({'error': 'Todo not found'}), 404
        
        return jsonify({'message': 'Todo deleted successfully'}), 200
    
    except Exception as e:
        return jsonify({'error': 'Failed to delete todo'}), 500

if __name__ == '__main__':
    app.run(debug=True, port=8080)