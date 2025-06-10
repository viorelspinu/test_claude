#!/usr/bin/env python3
"""
Development helper scripts for the Flask Todo application
"""

import os
import sys
import requests
import json
from datetime import datetime

# Add the backend directory to the path so we can import our app
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

from app import create_app, db
from app.models import Task


def init_database():
    """Initialize the database with tables"""
    app = create_app()
    with app.app_context():
        db.create_all()
        print("✅ Database initialized successfully!")


def reset_database():
    """Reset the database (drop and recreate all tables)"""
    app = create_app()
    with app.app_context():
        db.drop_all()
        db.create_all()
        print("✅ Database reset successfully!")


def seed_database():
    """Seed the database with sample data"""
    app = create_app()
    with app.app_context():
        # Clear existing data
        Task.query.delete()
        
        # Sample tasks
        sample_tasks = [
            {
                'title': 'Complete project documentation',
                'description': 'Write comprehensive documentation for the todo application',
                'priority': 'High',
                'completed': False
            },
            {
                'title': 'Set up CI/CD pipeline',
                'description': 'Configure continuous integration and deployment',
                'priority': 'Medium',
                'completed': False
            },
            {
                'title': 'Design user interface mockups',
                'description': 'Create wireframes and mockups for the frontend',
                'priority': 'Low',
                'completed': True
            },
            {
                'title': 'Implement user authentication',
                'description': 'Add login and registration functionality',
                'priority': 'High',
                'completed': False
            },
            {
                'title': 'Write unit tests',
                'description': 'Create comprehensive test coverage for the application',
                'priority': 'Medium',
                'completed': False
            }
        ]
        
        for task_data in sample_tasks:
            task = Task.from_dict(task_data)
            if task_data['completed']:
                task.completed_at = datetime.utcnow()
            db.session.add(task)
        
        db.session.commit()
        print(f"✅ Database seeded with {len(sample_tasks)} sample tasks!")


def check_api_health():
    """Check if the API is running and healthy"""
    try:
        response = requests.get('http://localhost:5001/api/health', timeout=5)
        if response.status_code == 200:
            data = response.json()
            print("✅ API is healthy!")
            print(f"   Status: {data.get('status')}")
            print(f"   Message: {data.get('message')}")
            print(f"   Timestamp: {data.get('timestamp')}")
            return True
        else:
            print(f"❌ API returned status code: {response.status_code}")
            return False
    except requests.RequestException as e:
        print(f"❌ API is not reachable: {e}")
        return False


def test_api_endpoints():
    """Test all API endpoints"""
    base_url = 'http://localhost:5001/api'
    
    print("🧪 Testing API endpoints...")
    
    # Test health endpoint
    try:
        response = requests.get(f'{base_url}/health')
        print(f"GET /health: {response.status_code} ✅" if response.ok else f"GET /health: {response.status_code} ❌")
    except Exception as e:
        print(f"GET /health: Error - {e} ❌")
    
    # Test get tasks
    try:
        response = requests.get(f'{base_url}/tasks')
        print(f"GET /tasks: {response.status_code} ✅" if response.ok else f"GET /tasks: {response.status_code} ❌")
    except Exception as e:
        print(f"GET /tasks: Error - {e} ❌")
    
    # Test create task
    try:
        test_task = {
            'title': 'Test Task',
            'description': 'This is a test task',
            'priority': 'Medium'
        }
        response = requests.post(f'{base_url}/tasks', json=test_task)
        print(f"POST /tasks: {response.status_code} ✅" if response.status_code == 201 else f"POST /tasks: {response.status_code} ❌")
        
        if response.status_code == 201:
            task_id = response.json()['task']['id']
            
            # Test get specific task
            response = requests.get(f'{base_url}/tasks/{task_id}')
            print(f"GET /tasks/{task_id}: {response.status_code} ✅" if response.ok else f"GET /tasks/{task_id}: {response.status_code} ❌")
            
            # Test update task
            update_data = {'completed': True}
            response = requests.put(f'{base_url}/tasks/{task_id}', json=update_data)
            print(f"PUT /tasks/{task_id}: {response.status_code} ✅" if response.ok else f"PUT /tasks/{task_id}: {response.status_code} ❌")
            
            # Test delete task
            response = requests.delete(f'{base_url}/tasks/{task_id}')
            print(f"DELETE /tasks/{task_id}: {response.status_code} ✅" if response.status_code == 204 else f"DELETE /tasks/{task_id}: {response.status_code} ❌")
            
    except Exception as e:
        print(f"Task CRUD operations: Error - {e} ❌")
    
    # Test stats endpoint
    try:
        response = requests.get(f'{base_url}/tasks/stats')
        print(f"GET /tasks/stats: {response.status_code} ✅" if response.ok else f"GET /tasks/stats: {response.status_code} ❌")
    except Exception as e:
        print(f"GET /tasks/stats: Error - {e} ❌")


def show_database_stats():
    """Show database statistics"""
    app = create_app()
    with app.app_context():
        total_tasks = Task.query.count()
        completed_tasks = Task.query.filter(Task.completed == True).count()
        pending_tasks = total_tasks - completed_tasks
        
        print(f"📊 Database Statistics:")
        print(f"   Total tasks: {total_tasks}")
        print(f"   Completed: {completed_tasks}")
        print(f"   Pending: {pending_tasks}")
        
        if total_tasks > 0:
            completion_rate = (completed_tasks / total_tasks) * 100
            print(f"   Completion rate: {completion_rate:.1f}%")
            
            # Priority breakdown
            high_priority = Task.query.filter(Task.priority == 'High').count()
            medium_priority = Task.query.filter(Task.priority == 'Medium').count()
            low_priority = Task.query.filter(Task.priority == 'Low').count()
            
            print(f"   Priority breakdown:")
            print(f"     High: {high_priority}")
            print(f"     Medium: {medium_priority}")
            print(f"     Low: {low_priority}")


def run_development_server():
    """Run the development server with debug mode"""
    os.environ['FLASK_ENV'] = 'development'
    app = create_app()
    
    # Initialize database if it doesn't exist
    with app.app_context():
        db.create_all()
    
    print("🚀 Starting Flask development server...")
    print("   - Debug mode: ON")
    print("   - Host: 0.0.0.0")
    print("   - Port: 5001")
    print("   - CORS origins: http://localhost:3000, http://127.0.0.1:3000")
    
    app.run(host='0.0.0.0', port=5001, debug=True)


if __name__ == '__main__':
    import argparse
    
    parser = argparse.ArgumentParser(description='Flask Todo App Development Helpers')
    parser.add_argument('command', choices=[
        'init-db', 'reset-db', 'seed-db', 'health', 'test-api', 
        'stats', 'dev-server', 'full-setup'
    ], help='Command to run')
    
    args = parser.parse_args()
    
    if args.command == 'init-db':
        init_database()
    elif args.command == 'reset-db':
        reset_database()
    elif args.command == 'seed-db':
        seed_database()
    elif args.command == 'health':
        check_api_health()
    elif args.command == 'test-api':
        test_api_endpoints()
    elif args.command == 'stats':
        show_database_stats()
    elif args.command == 'dev-server':
        run_development_server()
    elif args.command == 'full-setup':
        print("🔧 Setting up development environment...")
        init_database()
        seed_database()
        show_database_stats()
        print("✅ Full setup complete!")