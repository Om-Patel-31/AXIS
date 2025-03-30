from flask import Flask, request, jsonify
from flask_cors import CORS
from dotenv import load_dotenv
import os
from tasks import TaskManager
from notifications import NotificationManager
from ai_assistant import AIAssistant
from automation import AutomationManager
from datetime import datetime


# Load environment variables
load_dotenv()

app = Flask(__name__)
CORS(app)

# Initialize managers
task_manager = TaskManager()
notification_manager = NotificationManager()
ai_assistant = AIAssistant()
automation_manager = AutomationManager()

@app.route("/")
def home():
    return jsonify({
        "message": "Welcome to the AI Assistant API",
        "endpoints": {
            "tasks": {
                "GET /api/tasks": "List all tasks",
                "POST /api/tasks": "Create a new task",
                "GET /api/tasks/<task_id>": "Get a specific task",
                "PUT /api/tasks/<task_id>": "Update a task",
                "DELETE /api/tasks/<task_id>": "Delete a task"
            },
            "notifications": {
                "GET /api/notifications": "List all notifications",
                "GET /api/notifications/unread": "List unread notifications",
                "PUT /api/notifications/<notification_id>/read": "Mark a notification as read",
                "DELETE /api/notifications/<notification_id>": "Delete a notification"
            },
            "ai": {
                "POST /api/ai/process-voice": "Process voice command",
                "POST /api/ai/generate-flashcards": "Generate flashcards from content",
                "POST /api/ai/summarize": "Summarize content",
                "GET /api/ai/memory": "Retrieve AI memory"
            },
            "automation": {
                "POST /api/automation/organize-work": "Organize school work",
                "POST /api/automation/create-schedule": "Create study schedule",
                "GET /api/automation/email-summary": "Get email summary"
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

@app.route('/api/ai/process-voice', methods=['POST'])
def process_voice():
    try:
        command = ai_assistant.listen()
        intent = ai_assistant.process_command(command)
        return jsonify({
            'command': command,
            'intent': intent
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/ai/generate-flashcards', methods=['POST'])
def generate_flashcards():
    data = request.json
    content = data.get('content')
    if not content:
        return jsonify({'error': 'Content is required'}), 400
    
    flashcards = ai_assistant.generate_flashcards(content)
    return jsonify(flashcards)

@app.route('/api/ai/summarize', methods=['POST'])
def summarize_content():
    data = request.json
    content = data.get('content')
    if not content:
        return jsonify({'error': 'Content is required'}), 400
    
    summary = ai_assistant.summarize_content(content)
    return jsonify({'summary': summary})

@app.route('/api/ai/memory', methods=['GET'])
def get_memory():
    query = request.args.get('query', '')
    memories = ai_assistant.retrieve_memory(query)
    return jsonify(memories)

@app.route('/api/automation/organize-work', methods=['POST'])
def organize_work():
    data = request.json
    subject = data.get('subject')
    content = data.get('content')
    
    if not subject or not content:
        return jsonify({'error': 'Subject and content are required'}), 400
    
    automation_manager.organize_school_work(subject, content)
    return jsonify({'message': 'Work organized successfully'})

@app.route('/api/automation/create-schedule', methods=['POST'])
def create_schedule():
    data = request.json
    exam_date = data.get('exam_date')
    subject = data.get('subject')
    
    if not exam_date or not subject:
        return jsonify({'error': 'Exam date and subject are required'}), 400
    
    automation_manager.create_study_schedule(
        datetime.fromisoformat(exam_date),
        subject
    )
    return jsonify({'message': 'Schedule created successfully'})

@app.route('/api/automation/email-summary', methods=['GET'])
def get_email_summary():
    summaries = automation_manager.process_email_summary()
    return jsonify(summaries)

@app.route("/api/notifications", methods=['GET'])
def handle_notifications():
    return jsonify(notification_manager.get_all_notifications())

@app.route("/api/notifications/unread", methods=['GET'])
def handle_unread_notifications():
    return jsonify(notification_manager.get_unread_notifications())

@app.route("/api/notifications/<notification_id>/read", methods=['PUT'])
def handle_mark_notification_read(notification_id):
    notification = notification_manager.mark_notification_as_read(notification_id)
    if notification:
        return jsonify(notification)
    return jsonify({'error': 'Notification not found'}), 404

@app.route("/api/notifications/<notification_id>", methods=['DELETE'])
def handle_delete_notification(notification_id):
    if notification_manager.delete_notification(notification_id):
        return '', 204
    return jsonify({'error': 'Notification not found'}), 404

if __name__ == '__main__':
    app.run(debug=True, port=5000)