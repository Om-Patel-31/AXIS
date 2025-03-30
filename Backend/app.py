from flask import Flask, request, jsonify
from flask_cors import CORS
from dotenv import load_dotenv
import os
from tasks import TaskManager
from notifications import NotificationManager

# Load environment variables
load_dotenv()

app = Flask(__name__)
CORS(app)

# Initialize managers
task_manager = TaskManager()
notification_manager = NotificationManager()

@app.route("/")
def home():
    return jsonify({
        "message": "Welcome to the Task Management API",
        "endpoints": {
            "tasks": {
                "GET /tasks": "List all tasks",
                "POST /tasks": "Create a new task",
                "GET /tasks/<task_id>": "Get a specific task",
                "PUT /tasks/<task_id>": "Update a task",
                "DELETE /tasks/<task_id>": "Delete a task"
            },
            "notifications": {
                "GET /notifications": "List all notifications",
                "GET /notifications/unread": "List unread notifications",
                "PUT /notifications/<notification_id>/read": "Mark a notification as read",
                "DELETE /notifications/<notification_id>": "Delete a notification"
            }
        }
    })

@app.route('/api/tasks', methods=['GET'])
def get_tasks():
    return jsonify(task_manager.get_all_tasks())

@app.route('/api/tasks', methods=['POST'])
def create_task():
    data = request.json
    task = task_manager.create_task(
        title=data.get('title'),
        description=data.get('description'),
        due_date=data.get('due_date')
    )
    notification_manager.send_notification(f"New task created: {task['title']}")
    return jsonify(task), 201

@app.route('/api/tasks/<task_id>', methods=['PUT'])
def update_task(task_id):
    data = request.json
    task = task_manager.update_task(task_id, data)
    if task:
        notification_manager.send_notification(f"Task updated: {task['title']}")
        return jsonify(task)
    return jsonify({'error': 'Task not found'}), 404

@app.route('/api/tasks/<task_id>', methods=['DELETE'])
def delete_task(task_id):
    if task_manager.delete_task(task_id):
        notification_manager.send_notification(f"Task deleted: {task_id}")
        return '', 204
    return jsonify({'error': 'Task not found'}), 404

@app.route("/notifications", methods=['GET'])
def handle_notifications():
    return jsonify(notification_manager.get_all_notifications())

@app.route("/notifications/unread", methods=['GET'])
def handle_unread_notifications():
    return jsonify(notification_manager.get_unread_notifications())

@app.route("/notifications/<notification_id>/read", methods=['PUT'])
def handle_mark_notification_read(notification_id):
    notification = notification_manager.mark_notification_as_read(notification_id)
    if notification:
        return jsonify(notification.to_dict())
    return jsonify({'error': 'Notification not found'}), 404

@app.route("/notifications/<notification_id>", methods=['DELETE'])
def handle_delete_notification(notification_id):
    if notification_manager.delete_notification(notification_id):
        return '', 204
    return jsonify({'error': 'Notification not found'}), 404

if __name__ == '__main__':
    app.run(debug=True, port=5000)