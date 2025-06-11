from flask import Flask, jsonify, request
from flask_cors import CORS
from models import db, Todo
import os

app = Flask(__name__)
CORS(app)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///todos.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)

with app.app_context():
    db.create_all()

@app.route('/')
def health_check():
    return {'message': 'Todo API is running'}

@app.route('/api/health')
def api_health():
    return {'status': 'healthy', 'service': 'todo-api'}

@app.route('/api/todos', methods=['GET'])
def get_todos():
    try:
        todos = Todo.query.all()
        return jsonify([todo.to_dict() for todo in todos])
    except Exception as e:
        return jsonify({'error': 'Failed to fetch todos'}), 500

@app.route('/api/todos', methods=['POST'])
def create_todo():
    try:
        data = request.get_json()
        
        if not data or 'text' not in data:
            return jsonify({'error': 'Text field is required'}), 400
        
        text = data['text'].strip()
        if not text:
            return jsonify({'error': 'Text cannot be empty'}), 400
        
        if len(text) > 200:
            return jsonify({'error': 'Text must be 200 characters or less'}), 400
        
        todo = Todo(text=text)
        db.session.add(todo)
        db.session.commit()
        
        return jsonify(todo.to_dict()), 201
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': 'Failed to create todo'}), 500

@app.route('/api/todos/<int:todo_id>', methods=['PUT'])
def update_todo(todo_id):
    try:
        todo = Todo.query.get(todo_id)
        if not todo:
            return jsonify({'error': 'Todo not found'}), 404
        
        data = request.get_json()
        if not data:
            return jsonify({'error': 'No data provided'}), 400
        
        # Update text if provided
        if 'text' in data:
            text = data['text'].strip()
            if not text:
                return jsonify({'error': 'Text cannot be empty'}), 400
            if len(text) > 200:
                return jsonify({'error': 'Text must be 200 characters or less'}), 400
            todo.text = text
        
        # Update completed status if provided
        if 'completed' in data:
            if not isinstance(data['completed'], bool):
                return jsonify({'error': 'Completed must be a boolean'}), 400
            todo.completed = data['completed']
        
        db.session.commit()
        return jsonify(todo.to_dict())
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': 'Failed to update todo'}), 500

@app.route('/api/todos/<int:todo_id>', methods=['DELETE'])
def delete_todo(todo_id):
    try:
        todo = Todo.query.get(todo_id)
        if not todo:
            return jsonify({'error': 'Todo not found'}), 404
        
        db.session.delete(todo)
        db.session.commit()
        
        return jsonify({'message': 'Todo deleted successfully'})
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': 'Failed to delete todo'}), 500

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=8080)