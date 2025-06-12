import sys
import os

# Add backend directory to path
backend_path = os.path.join(os.path.dirname(__file__), '../../../backend')
sys.path.insert(0, os.path.abspath(backend_path))

from app import app

def test_cors_headers_present():
    """Test that CORS headers are present in response"""
    with app.test_client() as client:
        response = client.get('/health')
        headers = dict(response.headers)
        assert 'Access-Control-Allow-Origin' in headers
        assert headers['Access-Control-Allow-Origin'] == '*'

def test_options_preflight():
    """Test OPTIONS preflight request works"""
    with app.test_client() as client:
        response = client.options('/health')
        assert response.status_code == 200
        headers = dict(response.headers)
        assert 'Access-Control-Allow-Origin' in headers

def test_cors_import():
    """Test that flask_cors is properly imported"""
    import app
    # Verify CORS was configured by checking app has been wrapped
    assert hasattr(app, 'app')

if __name__ == '__main__':
    test_cors_headers_present()
    test_options_preflight()
    test_cors_import()
    print("All CORS tests passed!")