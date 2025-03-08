# app.py
from flask import Flask, render_template, request, jsonify
import os
import datetime

app = Flask(__name__)

# Sample data - in a real app, this would likely come from a database
tasks = [
    {"id": 1, "title": "Learn Flask", "completed": True},
    {"id": 2, "title": "Deploy to Cloud Run", "completed": True},
    {"id": 3, "title": "Add dynamic features", "completed": False}
]

@app.route('/')
def home():
    current_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    return render_template('index.html', current_time=current_time, tasks=tasks)

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/api/tasks', methods=['GET'])
def get_tasks():
    return jsonify(tasks)

@app.route('/api/tasks', methods=['POST'])
def add_task():
    data = request.get_json()
    if 'title' in data:
        new_task = {
            "id": len(tasks) + 1,
            "title": data['title'],
            "completed": False
        }
        tasks.append(new_task)
        return jsonify(new_task), 201
    return jsonify({"error": "Title is required"}), 400

@app.route('/api/tasks/<int:task_id>', methods=['PUT'])
def update_task(task_id):
    data = request.get_json()
    for task in tasks:
        if task['id'] == task_id:
            task['completed'] = data.get('completed', task['completed'])
            task['title'] = data.get('title', task['title'])
            return jsonify(task)
    return jsonify({"error": "Task not found"}), 404

@app.route('/environment')
def environment():
    env_info = {
        "Cloud Run Service": os.environ.get('K_SERVICE', 'Unknown'),
        "Cloud Run Revision": os.environ.get('K_REVISION', 'Unknown'),
        "Cloud Run Configuration": os.environ.get('K_CONFIGURATION', 'Unknown'),
        "Project ID": os.environ.get('GOOGLE_CLOUD_PROJECT', 'Unknown')
    }
    return render_template('environment.html', env_info=env_info)

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 8080))
    app.run(host='0.0.0.0', port=port, debug=True)
