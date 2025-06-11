from flask import Flask, jsonify
from flask_cors import CORS
from routes import api

app = Flask(__name__)
CORS(app)

# Register API blueprint
app.register_blueprint(api, url_prefix='/api')

@app.route('/')
def hello():
    return jsonify({
        'message': 'Todo App Backend',
        'status': 'running',
        'version': '1.0.0'
    })

@app.route('/api/status')
def status():
    return jsonify({
        'success': True,
        'message': 'API is running',
        'endpoints': [
            'GET /api/todos',
            'POST /api/todos',
            'PUT /api/todos/{id}',
            'DELETE /api/todos/{id}'
        ]
    })

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=8080)