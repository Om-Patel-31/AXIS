# AI Assistant Task Manager

A modern task management application with AI-powered features and real-time notifications.

## Features

- Create, read, update, and delete tasks
- Set due dates and descriptions for tasks
- Real-time notifications for task updates
- Email notifications (optional)
- Modern and responsive UI
- RESTful API backend

## Prerequisites

- Python 3.8 or higher
- Node.js (for serving the frontend)
- Git

## Setup

### Backend Setup

1. Navigate to the backend directory:
   ```bash
   cd backend
   ```

2. Create a virtual environment:
   ```bash
   python -m venv venv
   ```

3. Activate the virtual environment:
   - Windows:
     ```bash
     .\venv\Scripts\activate
     ```
   - Unix/MacOS:
     ```bash
     source venv/bin/activate
     ```

4. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

5. Create a `.env` file in the root directory with the following variables:
   ```
   EMAIL_USER=your-email@example.com
   EMAIL_PASSWORD=your-email-password
   SMTP_SERVER=smtp.gmail.com
   SMTP_PORT=587
   ```

6. Run the backend server:
   ```bash
   python app.py
   ```

The backend will be available at `http://localhost:5000`.

### Frontend Setup

1. Navigate to the frontend directory:
   ```bash
   cd frontend
   ```

2. Open `index.html` in your web browser or serve it using a local server:
   ```bash
   python -m http.server 8000
   ```

The frontend will be available at `http://localhost:8000`.

## API Endpoints

### Tasks

- `GET /api/tasks` - Get all tasks
- `POST /api/tasks` - Create a new task
- `PUT /api/tasks/<task_id>` - Update a task
- `DELETE /api/tasks/<task_id>` - Delete a task

### Notifications

- `GET /api/notifications` - Get all notifications
- `GET /api/notifications/unread` - Get unread notifications
- `PUT /api/notifications/<notification_id>/read` - Mark a notification as read
- `DELETE /api/notifications/<notification_id>` - Delete a notification

## Contributing

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add some amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## License

This project is licensed under the MIT License - see the LICENSE file for details. 