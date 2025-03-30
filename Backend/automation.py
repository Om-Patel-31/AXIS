import os
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload
from datetime import datetime, timedelta
import json
from typing import List, Dict
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from dotenv import load_dotenv

load_dotenv()

class AutomationManager:
    def __init__(self):
        self.SCOPES = [
            'https://www.googleapis.com/auth/drive',
            'https://www.googleapis.com/auth/calendar',
            'https://www.googleapis.com/auth/gmail.readonly'
        ]
        self.creds = None
        self.setup_credentials()
        
    def setup_credentials(self):
        """Setup Google API credentials"""
        if os.path.exists('token.json'):
            self.creds = Credentials.from_authorized_user_file('token.json', self.SCOPES)
        
        if not self.creds or not self.creds.valid:
            if self.creds and self.creds.expired and self.creds.refresh_token:
                self.creds.refresh(Request())
            else:
                flow = InstalledAppFlow.from_client_secrets_file('credentials.json', self.SCOPES)
                self.creds = flow.run_local_server(port=0)
            with open('token.json', 'w') as token:
                token.write(self.creds.to_json())

    def create_drive_folder(self, folder_name: str, parent_id: str = None) -> str:
        """Create a folder in Google Drive"""
        service = build('drive', 'v3', credentials=self.creds)
        
        file_metadata = {
            'name': folder_name,
            'mimeType': 'application/vnd.google-apps.folder',
            'parents': [parent_id] if parent_id else []
        }
        
        file = service.files().create(body=file_metadata, fields='id').execute()
        return file.get('id')

    def organize_school_work(self, subject: str, content: str):
        """Organize school work in Google Drive"""
        # Create subject folder if it doesn't exist
        subject_folder_id = self.create_drive_folder(subject)
        
        # Create timestamped folder for the content
        timestamp = datetime.now().strftime('%Y-%m-%d_%H-%M')
        content_folder_id = self.create_drive_folder(timestamp, subject_folder_id)
        
        # Create and upload content file
        service = build('drive', 'v3', credentials=self.creds)
        file_metadata = {
            'name': f'{subject}_content_{timestamp}.txt',
            'parents': [content_folder_id]
        }
        
        media = MediaFileUpload(
            content,
            mimetype='text/plain',
            resumable=True
        )
        
        service.files().create(
            body=file_metadata,
            media_body=media,
            fields='id'
        ).execute()

    def create_calendar_event(self, summary: str, description: str, start_time: datetime, duration: int):
        """Create a calendar event"""
        service = build('calendar', 'v3', credentials=self.creds)
        
        event = {
            'summary': summary,
            'description': description,
            'start': {
                'dateTime': start_time.isoformat(),
                'timeZone': 'UTC',
            },
            'end': {
                'dateTime': (start_time + timedelta(minutes=duration)).isoformat(),
                'timeZone': 'UTC',
            },
        }
        
        service.events().insert(calendarId='primary', body=event).execute()

    def create_study_schedule(self, exam_date: datetime, subject: str):
        """Create a study schedule for exams"""
        # Calculate days until exam
        days_until_exam = (exam_date - datetime.now()).days
        
        # Create study sessions
        study_sessions = self._generate_study_sessions(days_until_exam, subject)
        
        # Add sessions to calendar
        for session in study_sessions:
            self.create_calendar_event(
                summary=f"Study Session - {subject}",
                description=session['description'],
                start_time=session['start_time'],
                duration=session['duration']
            )

    def _generate_study_sessions(self, days_until_exam: int, subject: str) -> List[Dict]:
        """Generate study sessions based on spaced repetition"""
        sessions = []
        current_date = datetime.now()
        
        # Implement spaced repetition algorithm
        intervals = [1, 3, 7, 14, 30]  # Days between reviews
        
        for interval in intervals:
            if interval <= days_until_exam:
                session_date = current_date + timedelta(days=interval)
                sessions.append({
                    'start_time': session_date,
                    'duration': 60,  # 1 hour sessions
                    'description': f"Review {subject} - Spaced repetition session {interval} days"
                })
        
        return sessions

    def send_notification(self, message: str, email: str = None):
        """Send notification via email"""
        if email is None:
            email = os.getenv('NOTIFICATION_EMAIL')
            
        msg = MIMEMultipart()
        msg['From'] = os.getenv('EMAIL_USER')
        msg['To'] = email
        msg['Subject'] = "AI Assistant Notification"
        
        msg.attach(MIMEText(message, 'plain'))
        
        with smtplib.SMTP(os.getenv('SMTP_SERVER'), int(os.getenv('SMTP_PORT'))) as server:
            server.starttls()
            server.login(os.getenv('EMAIL_USER'), os.getenv('EMAIL_PASSWORD'))
            server.send_message(msg)

    def process_email_summary(self):
        """Process and summarize emails"""
        service = build('gmail', 'v1', credentials=self.creds)
        
        # Get recent emails
        results = service.users().messages().list(
            userId='me',
            maxResults=10
        ).execute()
        
        messages = results.get('messages', [])
        
        summaries = []
        for message in messages:
            msg = service.users().messages().get(
                userId='me',
                id=message['id']
            ).execute()
            
            # Extract email content and create summary
            # This is a simplified version - you'd want to properly parse email content
            subject = next(
                header['value'] for header in msg['payload']['headers']
                if header['name'] == 'Subject'
            )
            
            summaries.append({
                'subject': subject,
                'summary': f"Email from {subject}"  # Replace with actual summary
            })
        
        return summaries 