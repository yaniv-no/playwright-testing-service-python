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

class TestHealthEndpoint:
    """Test the health check endpoint"""
    
    def test_health_check(self, client):
        """Test that the health check endpoint returns correct status"""
        response = client.get('/api/health')
        assert response.status_code == 200
        
        data = json.loads(response.data)
        assert data['status'] == 'healthy'
        assert data['version'] == '1.0.0'

class TestTodosAPI:
    """Test the todos API endpoints"""
    
    def test_get_empty_todos(self, client):
        """Test getting todos when there are none"""
        response = client.get('/api/todos')
        assert response.status_code == 200
        
        data = json.loads(response.data)
        assert 'todos' in data
        assert data['todos'] == []
    
    def test_create_todo(self, client):
        """Test creating a new todo"""
        todo_data = {
            'title': 'Test Todo',
            'completed': False
        }
        
        response = client.post('/api/todos', 
                              data=json.dumps(todo_data),
                              content_type='application/json')
        
        assert response.status_code == 201
        
        data = json.loads(response.data)
        assert 'todo' in data
        assert data['todo']['title'] == 'Test Todo'
        assert data['todo']['completed'] is False
        assert data['todo']['id'] == 1
    
    def test_create_todo_with_completed_true(self, client):
        """Test creating a todo that is already completed"""
        todo_data = {
            'title': 'Completed Todo',
            'completed': True
        }
        
        response = client.post('/api/todos', 
                              data=json.dumps(todo_data),
                              content_type='application/json')
        
        assert response.status_code == 201
        
        data = json.loads(response.data)
        assert data['todo']['title'] == 'Completed Todo'
        assert data['todo']['completed'] is True
    
    def test_create_todo_without_title(self, client):
        """Test creating a todo without a title should fail"""
        todo_data = {
            'completed': False
        }
        
        response = client.post('/api/todos', 
                              data=json.dumps(todo_data),
                              content_type='application/json')
        
        assert response.status_code == 400
        
        data = json.loads(response.data)
        assert 'error' in data
        assert data['error'] == 'Title is required'
    
    def test_create_todo_with_empty_title(self, client):
        """Test creating a todo with empty title should fail"""
        todo_data = {
            'title': '',
            'completed': False
        }
        
        response = client.post('/api/todos', 
                              data=json.dumps(todo_data),
                              content_type='application/json')
        
        assert response.status_code == 400
    
    def test_create_and_get_todos(self, client):
        """Test creating todos and then getting them"""
        # Create first todo
        todo1_data = {'title': 'First Todo', 'completed': False}
        response1 = client.post('/api/todos', 
                               data=json.dumps(todo1_data),
                               content_type='application/json')
        assert response1.status_code == 201
        
        # Create second todo
        todo2_data = {'title': 'Second Todo', 'completed': True}
        response2 = client.post('/api/todos', 
                               data=json.dumps(todo2_data),
                               content_type='application/json')
        assert response2.status_code == 201
        
        # Get all todos
        response = client.get('/api/todos')
        assert response.status_code == 200
        
        data = json.loads(response.data)
        assert len(data['todos']) == 2
        assert data['todos'][0]['title'] == 'First Todo'
        assert data['todos'][0]['completed'] is False
        assert data['todos'][1]['title'] == 'Second Todo'
        assert data['todos'][1]['completed'] is True
    
    def test_update_todo(self, client):
        """Test updating a todo"""
        # Create a todo first
        todo_data = {'title': 'Original Title', 'completed': False}
        response = client.post('/api/todos', 
                              data=json.dumps(todo_data),
                              content_type='application/json')
        assert response.status_code == 201
        
        created_todo = json.loads(response.data)['todo']
        todo_id = created_todo['id']
        
        # Update the todo
        update_data = {'title': 'Updated Title', 'completed': True}
        response = client.put(f'/api/todos/{todo_id}', 
                             data=json.dumps(update_data),
                             content_type='application/json')
        
        assert response.status_code == 200
        
        data = json.loads(response.data)
        assert data['todo']['title'] == 'Updated Title'
        assert data['todo']['completed'] is True
        assert data['todo']['id'] == todo_id
    
    def test_update_todo_partial(self, client):
        """Test updating only some fields of a todo"""
        # Create a todo first
        todo_data = {'title': 'Original Title', 'completed': False}
        response = client.post('/api/todos', 
                              data=json.dumps(todo_data),
                              content_type='application/json')
        assert response.status_code == 201
        
        created_todo = json.loads(response.data)['todo']
        todo_id = created_todo['id']
        
        # Update only the completed status
        update_data = {'completed': True}
        response = client.put(f'/api/todos/{todo_id}', 
                             data=json.dumps(update_data),
                             content_type='application/json')
        
        assert response.status_code == 200
        
        data = json.loads(response.data)
        assert data['todo']['title'] == 'Original Title'  # Should remain unchanged
        assert data['todo']['completed'] is True
    
    def test_update_nonexistent_todo(self, client):
        """Test updating a todo that doesn't exist"""
        update_data = {'title': 'Updated Title', 'completed': True}
        response = client.put('/api/todos/999', 
                             data=json.dumps(update_data),
                             content_type='application/json')
        
        assert response.status_code == 404
        
        data = json.loads(response.data)
        assert 'error' in data
        assert data['error'] == 'Todo not found'
    
    def test_delete_todo(self, client):
        """Test deleting a todo"""
        # Create a todo first
        todo_data = {'title': 'To be deleted', 'completed': False}
        response = client.post('/api/todos', 
                              data=json.dumps(todo_data),
                              content_type='application/json')
        assert response.status_code == 201
        
        created_todo = json.loads(response.data)['todo']
        todo_id = created_todo['id']
        
        # Delete the todo
        response = client.delete(f'/api/todos/{todo_id}')
        assert response.status_code == 200
        
        data = json.loads(response.data)
        assert data['message'] == 'Todo deleted successfully'
        
        # Verify the todo is deleted
        response = client.get('/api/todos')
        data = json.loads(response.data)
        assert len(data['todos']) == 0
    
    def test_delete_nonexistent_todo(self, client):
        """Test deleting a todo that doesn't exist"""
        response = client.delete('/api/todos/999')
        assert response.status_code == 404
        
        data = json.loads(response.data)
        assert 'error' in data
        assert data['error'] == 'Todo not found'

class TestStaticFilesStillWork:
    """Test that the existing static file serving still works"""
    
    def test_index_page(self, client):
        """Test that the index page still loads"""
        response = client.get('/')
        assert response.status_code == 200
        assert b'todos' in response.data
        assert b'TodoMVC' in response.data
    
    def test_static_js_file(self, client):
        """Test that static JavaScript files are served"""
        response = client.get('/static/todo-app.js')
        assert response.status_code == 200
        assert b'TodoMVC' in response.data or b'todo' in response.data