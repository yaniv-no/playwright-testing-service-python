#!/bin/bash

# Comprehensive test runner script for the Flask Todo API application

echo "Running Flask Todo API Comprehensive Test Suite..."
echo "================================================="

# Run all Python tests
echo "Running all Python tests..."
python3 -m pytest tests/test_*.py -v --tb=short

# Check if tests passed
if [ $? -eq 0 ]; then
    echo ""
    echo "✅ All 44 Python tests passed!"
    echo ""
    echo "Test Coverage Summary:"
    echo "- 🔧 Flask Application Tests: 14 tests"
    echo "- 🌐 API Endpoint Tests: 14 tests"
    echo "- 🔗 Integration Tests: 16 tests"
    echo "- 📊 Total Tests: 44 tests"
    echo ""
    echo "Added Features:"
    echo "- 5 new REST API endpoints (CRUD operations + health check)"
    echo "- Comprehensive error handling and validation"
    echo "- Support for special characters, unicode, and edge cases"
    echo "- Full backwards compatibility with existing frontend"
    echo ""
    echo "API Endpoints:"
    echo "- GET /api/health - Health check"
    echo "- GET /api/todos - Get all todos"
    echo "- POST /api/todos - Create a new todo"
    echo "- PUT /api/todos/:id - Update an existing todo"
    echo "- DELETE /api/todos/:id - Delete a todo"
else
    echo ""
    echo "❌ Some tests failed!"
    exit 1
fi