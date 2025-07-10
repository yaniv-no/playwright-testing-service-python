# Flask Todo API Documentation

This document describes the REST API endpoints added to the Flask Todo application.

## API Endpoints

### Health Check
- **GET** `/api/health` - Check the health status of the API

**Response:**
```json
{
  "status": "healthy",
  "version": "1.0.0"
}
```

### Todos

#### Get All Todos
- **GET** `/api/todos` - Retrieve all todos

**Response:**
```json
{
  "todos": [
    {
      "id": 1,
      "title": "Sample Todo",
      "completed": false
    }
  ]
}
```

#### Create Todo
- **POST** `/api/todos` - Create a new todo

**Request Body:**
```json
{
  "title": "New Todo",
  "completed": false
}
```

**Response:**
```json
{
  "todo": {
    "id": 1,
    "title": "New Todo",
    "completed": false
  }
}
```

#### Update Todo
- **PUT** `/api/todos/:id` - Update an existing todo

**Request Body:**
```json
{
  "title": "Updated Todo",
  "completed": true
}
```

**Response:**
```json
{
  "todo": {
    "id": 1,
    "title": "Updated Todo",
    "completed": true
  }
}
```

#### Delete Todo
- **DELETE** `/api/todos/:id` - Delete a todo

**Response:**
```json
{
  "message": "Todo deleted successfully"
}
```

## Error Responses

All API endpoints return appropriate HTTP status codes:

- **200 OK** - Successful operation
- **201 Created** - Resource created successfully
- **400 Bad Request** - Invalid request data
- **404 Not Found** - Resource not found

Error responses include a descriptive error message:
```json
{
  "error": "Description of the error"
}
```

## Testing

The API includes comprehensive test coverage:

- **30 test cases** covering all endpoints
- **CRUD operations** testing
- **Edge cases** and error conditions
- **Integration tests** for complete workflows
- **Data validation** tests

Run the tests with:
```bash
python3 -m pytest tests/test_api.py tests/test_integration.py -v
```

Or use the test runner:
```bash
./run_tests.sh
```

## Examples

### Create a Todo
```bash
curl -X POST -H "Content-Type: application/json" \
  -d '{"title": "Learn API testing", "completed": false}' \
  http://localhost:5000/api/todos
```

### Get All Todos
```bash
curl -X GET http://localhost:5000/api/todos
```

### Update a Todo
```bash
curl -X PUT -H "Content-Type: application/json" \
  -d '{"title": "Learn API testing", "completed": true}' \
  http://localhost:5000/api/todos/1
```

### Delete a Todo
```bash
curl -X DELETE http://localhost:5000/api/todos/1
```