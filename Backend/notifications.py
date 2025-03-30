from datetime import datetime
import uuid
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import os
from dotenv import load_dotenv

load_dotenv()

class NotificationManager:
    def __init__(self):
        self.notifications = {}
        self.email = os.getenv('EMAIL_USER')
        self.password = os.getenv('EMAIL_PASSWORD')
        self.smtp_server = os.getenv('SMTP_SERVER', 'smtp.gmail.com')
        self.smtp_port = int(os.getenv('SMTP_PORT', '587'))

    def send_notification(self, message, task_id=None):
        notification_id = str(uuid.uuid4())
        notification = {
            'id': notification_id,
            'message': message,
            'task_id': task_id,
            'read': False,
            'created_at': datetime.utcnow().isoformat()
        }
        self.notifications[notification_id] = notification
        
        # Send email notification if credentials are configured
        if self.email and self.password:
            self._send_email_notification(message)
        
        return notification

    def get_all_notifications(self):
        return list(self.notifications.values())

    def get_unread_notifications(self):
        return [n for n in self.notifications.values() if not n['read']]

    def mark_notification_as_read(self, notification_id):
        if notification_id in self.notifications:
            self.notifications[notification_id]['read'] = True
            return self.notifications[notification_id]
        return None

    def delete_notification(self, notification_id):
        if notification_id in self.notifications:
            del self.notifications[notification_id]
            return True
        return False

    def _send_email_notification(self, message):
        try:
            msg = MIMEMultipart()
            msg['From'] = self.email
            msg['To'] = self.email
            msg['Subject'] = "AI Assistant Notification"
            
            msg.attach(MIMEText(message, 'plain'))
            
            server = smtplib.SMTP(self.smtp_server, self.smtp_port)
            server.starttls()
            server.login(self.email, self.password)
            server.send_message(msg)
            server.quit()
        except Exception as e:
            print(f"Failed to send email notification: {str(e)}")
