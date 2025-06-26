from flask import Flask, send_from_directory
import os

app = Flask(__name__, static_folder=os.path.join(os.path.dirname(__file__), 'static'))

@app.route("/")
def index():
    return send_from_directory(app.static_folder, "index.html")

@app.route("/static/<path:filename>")
def static_files(filename):
    return send_from_directory(app.static_folder, filename)

if __name__ == "__main__":
    app.run()