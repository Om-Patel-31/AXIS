from flask import Flask, request, jsonify
from tasks import add_task, get_all_tasks, get_task_by_id, update_task, delete_task
from notifications import add_notification, get_all_notifications, get_unread_notifications, mark_notification_as_read, delete_notification

app = Flask(__name__)

@app.route("/tasks", methods=['GET', 'POST'])
def handle_tasks():
    if request.method == 'POST':
        data = request.json
        task = add_task(
            title=data.get('title'),
            description=data.get('description'),
            due_date=data.get('due_date')
        )
        add_notification(f"New task created: {task.title}", task.id)
        return jsonify(task.to_dict()), 201
    return jsonify(get_all_tasks())

@app.route("/tasks/<task_id>", methods=['GET', 'PUT', 'DELETE'])
def handle_single_task(task_id):
    if request.method == 'GET':
        task = get_task_by_id(task_id)
        if task:
            return jsonify(task.to_dict())
        return jsonify({'error': 'Task not found'}), 404
    
    elif request.method == 'PUT':
        data = request.json
        task = update_task(
            task_id,
            title=data.get('title'),
            description=data.get('description'),
            due_date=data.get('due_date'),
            completed=data.get('completed')
        )
        if task:
            add_notification(f"Task updated: {task.title}", task.id)
            return jsonify(task.to_dict())
        return jsonify({'error': 'Task not found'}), 404
    
    elif request.method == 'DELETE':
        task = get_task_by_id(task_id)
        if task:
            delete_task(task_id)
            add_notification(f"Task deleted: {task.title}")
            return '', 204
        return jsonify({'error': 'Task not found'}), 404

@app.route("/notifications", methods=['GET'])
def handle_notifications():
    return jsonify(get_all_notifications())

@app.route("/notifications/unread", methods=['GET'])
def handle_unread_notifications():
    return jsonify(get_unread_notifications())

@app.route("/notifications/<notification_id>/read", methods=['PUT'])
def handle_mark_notification_read(notification_id):
    notification = mark_notification_as_read(notification_id)
    if notification:
        return jsonify(notification.to_dict())
    return jsonify({'error': 'Notification not found'}), 404

@app.route("/notifications/<notification_id>", methods=['DELETE'])
def handle_delete_notification(notification_id):
    if delete_notification(notification_id):
        return '', 204
    return jsonify({'error': 'Notification not found'}), 404

if __name__ == '__main__':
    app.run(debug=True)