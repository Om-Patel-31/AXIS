from datetime import datetime

class Notification:
    def __init__(self, message, task_id=None, notification_type="info"):
        self.id = datetime.now().strftime("%Y%m%d%H%M%S")
        self.message = message
        self.task_id = task_id
        self.type = notification_type
        self.created_at = datetime.now()
        self.read = False

    def to_dict(self):
        return {
            'id': self.id,
            'message': self.message,
            'task_id': self.task_id,
            'type': self.type,
            'created_at': self.created_at.isoformat(),
            'read': self.read
        }

notifications = []

def add_notification(message, task_id=None, notification_type="info"):
    notification = Notification(message, task_id, notification_type)
    notifications.append(notification)
    return notification

def get_all_notifications():
    return [notification.to_dict() for notification in notifications]

def get_unread_notifications():
    return [notification.to_dict() for notification in notifications if not notification.read]

def mark_notification_as_read(notification_id):
    for notification in notifications:
        if notification.id == notification_id:
            notification.read = True
            return notification
    return None

def delete_notification(notification_id):
    notification = next((n for n in notifications if n.id == notification_id), None)
    if notification:
        notifications.remove(notification)
        return True
    return False
