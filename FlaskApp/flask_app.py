from flask import Flask, send_from_directory, jsonify, request
import os

app = Flask(__name__, static_folder=os.path.join(os.path.dirname(__file__), 'static'))

# In-memory storage for todos (in a real app, this would be a database)
todos = []
todo_id_counter = 1

@app.route("/")
def index():
    return send_from_directory(app.static_folder, "index.html")

@app.route("/static/<path:filename>")
def static_files(filename):
    return send_from_directory(app.static_folder, filename)

# API endpoints for todos
@app.route("/api/todos", methods=["GET"])
def get_todos():
    """Get all todos"""
    return jsonify({"todos": todos})

@app.route("/api/todos", methods=["POST"])
def create_todo():
    """Create a new todo"""
    global todo_id_counter
    data = request.get_json()
    
    if not data or not data.get('title'):
        return jsonify({"error": "Title is required"}), 400
    
    todo = {
        "id": todo_id_counter,
        "title": data["title"],
        "completed": data.get("completed", False)
    }
    
    todos.append(todo)
    todo_id_counter += 1
    
    return jsonify({"todo": todo}), 201

@app.route("/api/todos/<int:todo_id>", methods=["PUT"])
def update_todo(todo_id):
    """Update a todo"""
    data = request.get_json()
    
    if not data:
        return jsonify({"error": "No data provided"}), 400
    
    todo = next((t for t in todos if t["id"] == todo_id), None)
    if not todo:
        return jsonify({"error": "Todo not found"}), 404
    
    todo["title"] = data.get("title", todo["title"])
    todo["completed"] = data.get("completed", todo["completed"])
    
    return jsonify({"todo": todo})

@app.route("/api/todos/<int:todo_id>", methods=["DELETE"])
def delete_todo(todo_id):
    """Delete a todo"""
    global todos
    
    todo = next((t for t in todos if t["id"] == todo_id), None)
    if not todo:
        return jsonify({"error": "Todo not found"}), 404
    
    todos = [t for t in todos if t["id"] != todo_id]
    
    return jsonify({"message": "Todo deleted successfully"})

@app.route("/api/health", methods=["GET"])
def health_check():
    """Health check endpoint"""
    return jsonify({"status": "healthy", "version": "1.0.0"})

if __name__ == "__main__":
    app.run()