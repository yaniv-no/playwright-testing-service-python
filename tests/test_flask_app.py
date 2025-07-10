import pytest
import sys
import os

# Add the parent directory to the path to import the Flask app
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from FlaskApp.flask_app import app

class TestFlaskAppConfiguration:
    """Test Flask app configuration and setup"""
    
    def test_app_exists(self):
        """Test that the Flask app exists and can be imported"""
        assert app is not None
        assert app.name == 'FlaskApp.flask_app'
    
    def test_app_is_testing_mode(self):
        """Test that the app can be configured for testing"""
        app.config['TESTING'] = True
        assert app.config['TESTING'] is True
    
    def test_static_folder_configured(self):
        """Test that the static folder is configured correctly"""
        assert app.static_folder is not None
        assert 'static' in app.static_folder

class TestFlaskAppRoutes:
    """Test Flask app routes and basic functionality"""
    
    def test_app_has_routes(self):
        """Test that the app has the expected routes"""
        with app.test_client() as client:
            # Test that basic routes exist
            response = client.get('/')
            assert response.status_code == 200
            
            # Test that static routes work
            response = client.get('/static/todo-app.js')
            assert response.status_code == 200
            
            # Test that API routes exist
            response = client.get('/api/health')
            assert response.status_code == 200
            
            response = client.get('/api/todos')
            assert response.status_code == 200

class TestFlaskAppMemoryStorage:
    """Test the in-memory storage functionality"""
    
    def test_todos_list_exists(self):
        """Test that the todos list exists in the module"""
        from FlaskApp.flask_app import todos
        assert todos is not None
        assert isinstance(todos, list)
    
    def test_todo_counter_exists(self):
        """Test that the todo counter exists in the module"""
        from FlaskApp.flask_app import todo_id_counter
        assert todo_id_counter is not None
        assert isinstance(todo_id_counter, int)
        assert todo_id_counter >= 1

class TestFlaskAppUtilities:
    """Test utility functions and helper methods"""
    
    def test_app_can_handle_json_requests(self):
        """Test that the app can handle JSON requests"""
        with app.test_client() as client:
            # Test that the app can handle JSON content type
            response = client.post('/api/todos', 
                                  data='{"title": "Test"}',
                                  content_type='application/json')
            # Should either succeed or fail with a specific error, not crash
            assert response.status_code in [200, 201, 400]
    
    def test_app_handles_missing_routes(self):
        """Test that the app handles missing routes gracefully"""
        with app.test_client() as client:
            response = client.get('/nonexistent-route')
            assert response.status_code == 404

class TestFlaskAppImports:
    """Test that all required imports work"""
    
    def test_flask_imports(self):
        """Test that Flask imports work correctly"""
        try:
            from flask import Flask, send_from_directory, jsonify, request
            assert True
        except ImportError:
            pytest.fail("Flask imports failed")
    
    def test_os_imports(self):
        """Test that OS imports work correctly"""
        try:
            import os
            assert True
        except ImportError:
            pytest.fail("OS imports failed")

class TestFlaskAppInitialization:
    """Test Flask app initialization"""
    
    def test_app_initialization(self):
        """Test that the app initializes correctly"""
        # Test that we can create a test client
        with app.test_client() as client:
            assert client is not None
    
    def test_app_context(self):
        """Test that the app context works correctly"""
        with app.app_context():
            assert app is not None
            # We should be able to access the app within the context
            from flask import current_app
            assert current_app is not None

class TestFlaskAppErrorHandling:
    """Test error handling in the Flask app"""
    
    def test_invalid_content_type(self):
        """Test handling of invalid content types"""
        with app.test_client() as client:
            response = client.post('/api/todos', 
                                  data='{"title": "Test"}',
                                  content_type='text/plain')
            # Should handle gracefully - either process or return error
            assert response.status_code in [200, 201, 400, 415]
    
    def test_malformed_json(self):
        """Test handling of malformed JSON"""
        with app.test_client() as client:
            response = client.post('/api/todos', 
                                  data='invalid json',
                                  content_type='application/json')
            # Should return 400 Bad Request
            assert response.status_code == 400