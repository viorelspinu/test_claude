from flask import jsonify, request
from .models import Todo
from . import db

def register_routes(app):
    @app.route('/api/todos', methods=['GET'])
    def get_todos():
        todos = Todo.query.all()
        return jsonify([todo.to_dict() for todo in todos])
    
    @app.route('/api/todos', methods=['POST'])
    def create_todo():
        data = request.get_json()
        
        if not data or 'text' not in data:
            return jsonify({'error': 'Text field is required'}), 400
        
        todo = Todo(text=data['text'])
        db.session.add(todo)
        db.session.commit()
        
        return jsonify(todo.to_dict()), 201
    
    @app.route('/api/todos/<int:todo_id>', methods=['PUT'])
    def update_todo(todo_id):
        todo = Todo.query.get(todo_id)
        
        if not todo:
            return jsonify({'error': 'Todo not found'}), 404
        
        data = request.get_json()
        if not data:
            return jsonify({'error': 'No data provided'}), 400
        
        if 'text' in data:
            todo.text = data['text']
        if 'completed' in data:
            todo.completed = data['completed']
        
        db.session.commit()
        
        return jsonify(todo.to_dict())
    
    @app.route('/api/todos/<int:todo_id>', methods=['DELETE'])
    def delete_todo(todo_id):
        todo = Todo.query.get(todo_id)
        
        if not todo:
            return jsonify({'error': 'Todo not found'}), 404
        
        db.session.delete(todo)
        db.session.commit()
        
        return '', 204