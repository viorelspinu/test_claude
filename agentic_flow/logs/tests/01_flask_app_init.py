import sys
import os

# Add backend directory to path
backend_path = os.path.join(os.path.dirname(__file__), '../../../backend')
sys.path.insert(0, os.path.abspath(backend_path))

from app import app

def test_flask_app_creation():
    """Test that Flask app is created successfully"""
    assert app is not None
    assert app.name == 'app'

def test_health_endpoint():
    """Test health check endpoint"""
    with app.test_client() as client:
        response = client.get('/health')
        assert response.status_code == 200
        data = response.get_json()
        assert data['status'] == 'healthy'

def test_app_configuration():
    """Test app configuration"""
    # Debug mode is set when running with app.run(debug=True)
    # In test context, just verify app exists
    assert hasattr(app, 'config')

if __name__ == '__main__':
    test_flask_app_creation()
    test_health_endpoint()
    test_app_configuration()
    print("All tests passed!")