import pytest
import json
import sys
import os

# Add the parent directory to the path to import the Flask app
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from FlaskApp.flask_app import app

@pytest.fixture
def client():
    """Create a test client for the Flask app"""
    app.config['TESTING'] = True
    with app.test_client() as client:
        with app.app_context():
            # Clear todos before each test
            from FlaskApp.flask_app import todos
            todos.clear()
            # Reset the counter
            import FlaskApp.flask_app as flask_app
            flask_app.todo_id_counter = 1
            yield client

class TestAPIIntegration:
    """Integration tests for the API endpoints"""
    
    def test_full_crud_workflow(self, client):
        """Test a complete CRUD workflow"""
        # Create a todo
        create_data = {'title': 'Integration Test Todo', 'completed': False}
        response = client.post('/api/todos', 
                              data=json.dumps(create_data),
                              content_type='application/json')
        assert response.status_code == 201
        
        todo = json.loads(response.data)['todo']
        todo_id = todo['id']
        
        # Read the todo
        response = client.get('/api/todos')
        assert response.status_code == 200
        
        data = json.loads(response.data)
        assert len(data['todos']) == 1
        assert data['todos'][0]['title'] == 'Integration Test Todo'
        
        # Update the todo
        update_data = {'title': 'Updated Integration Test Todo', 'completed': True}
        response = client.put(f'/api/todos/{todo_id}', 
                             data=json.dumps(update_data),
                             content_type='application/json')
        assert response.status_code == 200
        
        updated_todo = json.loads(response.data)['todo']
        assert updated_todo['title'] == 'Updated Integration Test Todo'
        assert updated_todo['completed'] is True
        
        # Verify the update
        response = client.get('/api/todos')
        data = json.loads(response.data)
        assert data['todos'][0]['title'] == 'Updated Integration Test Todo'
        assert data['todos'][0]['completed'] is True
        
        # Delete the todo
        response = client.delete(f'/api/todos/{todo_id}')
        assert response.status_code == 200
        
        # Verify deletion
        response = client.get('/api/todos')
        data = json.loads(response.data)
        assert len(data['todos']) == 0
    
    def test_multiple_todos_operations(self, client):
        """Test operations with multiple todos"""
        # Create multiple todos
        todos_data = [
            {'title': 'Todo 1', 'completed': False},
            {'title': 'Todo 2', 'completed': True},
            {'title': 'Todo 3', 'completed': False}
        ]
        
        todo_ids = []
        for todo_data in todos_data:
            response = client.post('/api/todos', 
                                  data=json.dumps(todo_data),
                                  content_type='application/json')
            assert response.status_code == 201
            todo_ids.append(json.loads(response.data)['todo']['id'])
        
        # Get all todos
        response = client.get('/api/todos')
        assert response.status_code == 200
        
        data = json.loads(response.data)
        assert len(data['todos']) == 3
        
        # Update the second todo
        update_data = {'completed': False}
        response = client.put(f'/api/todos/{todo_ids[1]}', 
                             data=json.dumps(update_data),
                             content_type='application/json')
        assert response.status_code == 200
        
        # Delete the first todo
        response = client.delete(f'/api/todos/{todo_ids[0]}')
        assert response.status_code == 200
        
        # Verify final state
        response = client.get('/api/todos')
        data = json.loads(response.data)
        assert len(data['todos']) == 2
        assert data['todos'][0]['title'] == 'Todo 2'
        assert data['todos'][0]['completed'] is False
        assert data['todos'][1]['title'] == 'Todo 3'

class TestAPIEdgeCases:
    """Test edge cases and error conditions"""
    
    def test_invalid_json_in_create(self, client):
        """Test creating a todo with invalid JSON"""
        response = client.post('/api/todos', 
                              data='invalid json',
                              content_type='application/json')
        assert response.status_code == 400
    
    def test_empty_request_body_in_create(self, client):
        """Test creating a todo with empty request body"""
        response = client.post('/api/todos', 
                              data='',
                              content_type='application/json')
        assert response.status_code == 400
    
    def test_invalid_json_in_update(self, client):
        """Test updating a todo with invalid JSON"""
        # Create a todo first
        todo_data = {'title': 'Test Todo', 'completed': False}
        response = client.post('/api/todos', 
                              data=json.dumps(todo_data),
                              content_type='application/json')
        assert response.status_code == 201
        
        todo_id = json.loads(response.data)['todo']['id']
        
        # Try to update with invalid JSON
        response = client.put(f'/api/todos/{todo_id}', 
                             data='invalid json',
                             content_type='application/json')
        assert response.status_code == 400
    
    def test_empty_request_body_in_update(self, client):
        """Test updating a todo with empty request body"""
        # Create a todo first
        todo_data = {'title': 'Test Todo', 'completed': False}
        response = client.post('/api/todos', 
                              data=json.dumps(todo_data),
                              content_type='application/json')
        assert response.status_code == 201
        
        todo_id = json.loads(response.data)['todo']['id']
        
        # Try to update with empty body
        response = client.put(f'/api/todos/{todo_id}', 
                             data='',
                             content_type='application/json')
        assert response.status_code == 400
    
    def test_special_characters_in_title(self, client):
        """Test creating todos with special characters in title"""
        special_titles = [
            'Todo with émojis 🚀',
            'Todo with "quotes" and \'apostrophes\'',
            'Todo with <html> tags',
            'Todo with newlines\nand\ttabs',
            'Todo with unicode: αβγδε'
        ]
        
        for title in special_titles:
            todo_data = {'title': title, 'completed': False}
            response = client.post('/api/todos', 
                                  data=json.dumps(todo_data),
                                  content_type='application/json')
            assert response.status_code == 201
            
            created_todo = json.loads(response.data)['todo']
            assert created_todo['title'] == title
    
    def test_very_long_title(self, client):
        """Test creating a todo with a very long title"""
        long_title = 'A' * 1000  # 1000 character title
        todo_data = {'title': long_title, 'completed': False}
        
        response = client.post('/api/todos', 
                              data=json.dumps(todo_data),
                              content_type='application/json')
        assert response.status_code == 201
        
        created_todo = json.loads(response.data)['todo']
        assert created_todo['title'] == long_title
    
    def test_non_string_title(self, client):
        """Test creating a todo with non-string title"""
        todo_data = {'title': 123, 'completed': False}
        
        response = client.post('/api/todos', 
                              data=json.dumps(todo_data),
                              content_type='application/json')
        # Should still work as the title gets converted to string
        assert response.status_code == 201
        
        created_todo = json.loads(response.data)['todo']
        assert created_todo['title'] == 123
    
    def test_non_boolean_completed(self, client):
        """Test creating a todo with non-boolean completed value"""
        todo_data = {'title': 'Test Todo', 'completed': 'true'}
        
        response = client.post('/api/todos', 
                              data=json.dumps(todo_data),
                              content_type='application/json')
        assert response.status_code == 201
        
        created_todo = json.loads(response.data)['todo']
        assert created_todo['completed'] == 'true'  # Should preserve the type

class TestAPIResponseHeaders:
    """Test API response headers and content types"""
    
    def test_health_check_content_type(self, client):
        """Test that health check returns correct content type"""
        response = client.get('/api/health')
        assert response.status_code == 200
        assert response.content_type == 'application/json'
    
    def test_todos_get_content_type(self, client):
        """Test that todos GET returns correct content type"""
        response = client.get('/api/todos')
        assert response.status_code == 200
        assert response.content_type == 'application/json'
    
    def test_todos_post_content_type(self, client):
        """Test that todos POST returns correct content type"""
        todo_data = {'title': 'Test Todo', 'completed': False}
        response = client.post('/api/todos', 
                              data=json.dumps(todo_data),
                              content_type='application/json')
        assert response.status_code == 201
        assert response.content_type == 'application/json'

class TestAPIConsistency:
    """Test API consistency and behavior"""
    
    def test_todo_id_incrementing(self, client):
        """Test that todo IDs increment correctly"""
        # Create multiple todos
        for i in range(3):
            todo_data = {'title': f'Todo {i+1}', 'completed': False}
            response = client.post('/api/todos', 
                                  data=json.dumps(todo_data),
                                  content_type='application/json')
            assert response.status_code == 201
            
            created_todo = json.loads(response.data)['todo']
            assert created_todo['id'] == i + 1
    
    def test_todo_id_persistence_after_delete(self, client):
        """Test that todo IDs don't reuse after deletion"""
        # Create and delete a todo
        todo_data = {'title': 'First Todo', 'completed': False}
        response = client.post('/api/todos', 
                              data=json.dumps(todo_data),
                              content_type='application/json')
        assert response.status_code == 201
        
        todo_id = json.loads(response.data)['todo']['id']
        
        response = client.delete(f'/api/todos/{todo_id}')
        assert response.status_code == 200
        
        # Create another todo - should get the next ID, not reuse the deleted one
        todo_data2 = {'title': 'Second Todo', 'completed': False}
        response = client.post('/api/todos', 
                              data=json.dumps(todo_data2),
                              content_type='application/json')
        assert response.status_code == 201
        
        new_todo = json.loads(response.data)['todo']
        assert new_todo['id'] == todo_id + 1
    
    def test_api_endpoints_exist(self, client):
        """Test that all expected API endpoints exist"""
        # Test that endpoints respond (not 404)
        endpoints = [
            ('GET', '/api/health'),
            ('GET', '/api/todos'),
        ]
        
        for method, endpoint in endpoints:
            response = client.open(endpoint, method=method)
            assert response.status_code != 404, f"Endpoint {method} {endpoint} should exist"