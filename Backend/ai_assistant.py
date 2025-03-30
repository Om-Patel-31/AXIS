import speech_recognition as sr
import pyttsx3
import json
import os
from datetime import datetime, timedelta
import sqlite3
from typing import Dict, List, Optional
import openai
from dotenv import load_dotenv

load_dotenv()

class AIAssistant:
    def __init__(self):
        self.engine = pyttsx3.init()
        self.recognizer = sr.Recognizer()
        self.memory_db = "memory.db"
        self.setup_database()
        self.openai_client = openai.OpenAI(api_key=os.getenv('OPENAI_API_KEY'))
        
    def setup_database(self):
        """Initialize SQLite database for memory storage"""
        conn = sqlite3.connect(self.memory_db)
        c = conn.cursor()
        
        # Long-term memory table
        c.execute('''CREATE TABLE IF NOT EXISTS long_term_memory
                    (id INTEGER PRIMARY KEY, content TEXT, category TEXT, 
                     created_at TIMESTAMP, last_accessed TIMESTAMP)''')
        
        # Short-term memory table (60 days)
        c.execute('''CREATE TABLE IF NOT EXISTS short_term_memory
                    (id INTEGER PRIMARY KEY, content TEXT, category TEXT, 
                     created_at TIMESTAMP, expires_at TIMESTAMP)''')
        
        # Academic information table
        c.execute('''CREATE TABLE IF NOT EXISTS academic_info
                    (id INTEGER PRIMARY KEY, subject TEXT, content TEXT, 
                     type TEXT, created_at TIMESTAMP)''')
        
        conn.commit()
        conn.close()

    def listen(self) -> str:
        """Listen for voice input and convert to text"""
        with sr.Microphone() as source:
            print("Listening...")
            audio = self.recognizer.listen(source)
            try:
                text = self.recognizer.recognize_google(audio)
                return text
            except sr.UnknownValueError:
                return "Could not understand audio"
            except sr.RequestError:
                return "Could not request results"

    def speak(self, text: str):
        """Convert text to speech"""
        self.engine.say(text)
        self.engine.runAndWait()

    def store_long_term_memory(self, content: str, category: str):
        """Store information in long-term memory"""
        conn = sqlite3.connect(self.memory_db)
        c = conn.cursor()
        c.execute('''INSERT INTO long_term_memory (content, category, created_at, last_accessed)
                    VALUES (?, ?, ?, ?)''', (content, category, datetime.now(), datetime.now()))
        conn.commit()
        conn.close()

    def store_short_term_memory(self, content: str, category: str):
        """Store information in short-term memory (60 days)"""
        conn = sqlite3.connect(self.memory_db)
        c = conn.cursor()
        expires_at = datetime.now() + timedelta(days=60)
        c.execute('''INSERT INTO short_term_memory (content, category, created_at, expires_at)
                    VALUES (?, ?, ?, ?)''', (content, category, datetime.now(), expires_at))
        conn.commit()
        conn.close()

    def retrieve_memory(self, query: str) -> List[Dict]:
        """Retrieve relevant memories based on query"""
        conn = sqlite3.connect(self.memory_db)
        c = conn.cursor()
        
        # Search in both long-term and short-term memory
        c.execute('''SELECT content, category, created_at FROM long_term_memory
                    WHERE content LIKE ? ORDER BY last_accessed DESC''', (f'%{query}%',))
        long_term_results = c.fetchall()
        
        c.execute('''SELECT content, category, created_at FROM short_term_memory
                    WHERE content LIKE ? AND expires_at > ? ORDER BY created_at DESC''',
                 (f'%{query}%', datetime.now()))
        short_term_results = c.fetchall()
        
        conn.close()
        
        return [
            {'content': r[0], 'category': r[1], 'created_at': r[2], 'type': 'long_term'}
            for r in long_term_results
        ] + [
            {'content': r[0], 'category': r[1], 'created_at': r[2], 'type': 'short_term'}
            for r in short_term_results
        ]

    def process_academic_content(self, content: str, subject: str, content_type: str):
        """Process and store academic content"""
        conn = sqlite3.connect(self.memory_db)
        c = conn.cursor()
        c.execute('''INSERT INTO academic_info (subject, content, type, created_at)
                    VALUES (?, ?, ?, ?)''', (subject, content, content_type, datetime.now()))
        conn.commit()
        conn.close()

    def generate_flashcards(self, content: str) -> List[Dict]:
        """Generate flashcards from content using OpenAI"""
        response = self.openai_client.chat.completions.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": "Generate flashcards from the following content. Format as JSON with 'question' and 'answer' fields."},
                {"role": "user", "content": content}
            ]
        )
        return json.loads(response.choices[0].message.content)

    def summarize_content(self, content: str) -> str:
        """Generate a summary of content using OpenAI"""
        response = self.openai_client.chat.completions.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": "Provide a concise summary of the following content."},
                {"role": "user", "content": content}
            ]
        )
        return response.choices[0].message.content

    def process_command(self, command: str):
        """Process voice commands and execute appropriate actions"""
        # Store command in short-term memory
        self.store_short_term_memory(command, "command")
        
        # Process command using OpenAI for intent recognition
        response = self.openai_client.chat.completions.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": "Analyze the command and determine the intent and required actions."},
                {"role": "user", "content": command}
            ]
        )
        
        # Execute appropriate actions based on intent
        intent = response.choices[0].message.content
        # Add specific action handlers here based on intent
        
        return intent 