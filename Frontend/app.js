const API_BASE_URL = 'http://localhost:5000/api';

// DOM Elements
const taskForm = document.getElementById('task-form');
const tasksList = document.getElementById('tasks-list');
const notificationsPanel = document.getElementById('notifications-panel');
const notificationsList = document.getElementById('notifications-list');
const notificationToggle = document.getElementById('notification-toggle');
const notificationCount = document.getElementById('notification-count');

// Event Listeners
taskForm.addEventListener('submit', handleTaskSubmit);
notificationToggle.addEventListener('click', toggleNotifications);

// Initialize
document.addEventListener('DOMContentLoaded', () => {
    loadTasks();
    loadNotifications();
});

// Task Management
async function loadTasks() {
    try {
        const response = await fetch(`${API_BASE_URL}/tasks`);
        const tasks = await response.json();
        renderTasks(tasks);
    } catch (error) {
        console.error('Error loading tasks:', error);
    }
}

function renderTasks(tasks) {
    tasksList.innerHTML = '';
    tasks.forEach(task => {
        const taskElement = createTaskElement(task);
        tasksList.appendChild(taskElement);
    });
}

function createTaskElement(task) {
    const div = document.createElement('div');
    div.className = 'task-item';
    div.innerHTML = `
        <div class="task-content">
            <div class="task-title">${task.title}</div>
            <div class="task-description">${task.description || ''}</div>
            ${task.due_date ? `<div class="task-due-date">Due: ${new Date(task.due_date).toLocaleString()}</div>` : ''}
        </div>
        <div class="task-actions">
            <button onclick="updateTask('${task.id}')">Edit</button>
            <button class="delete-btn" onclick="deleteTask('${task.id}')">Delete</button>
        </div>
    `;
    return div;
}

async function handleTaskSubmit(event) {
    event.preventDefault();
    
    const title = document.getElementById('title').value;
    const description = document.getElementById('description').value;
    const dueDate = document.getElementById('due-date').value;

    try {
        const response = await fetch(`${API_BASE_URL}/tasks`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ title, description, due_date: dueDate }),
        });

        if (response.ok) {
            taskForm.reset();
            loadTasks();
            loadNotifications();
        }
    } catch (error) {
        console.error('Error creating task:', error);
    }
}

async function updateTask(taskId) {
    // Implement task update functionality
    console.log('Update task:', taskId);
}

async function deleteTask(taskId) {
    try {
        const response = await fetch(`${API_BASE_URL}/tasks/${taskId}`, {
            method: 'DELETE',
        });

        if (response.ok) {
            loadTasks();
            loadNotifications();
        }
    } catch (error) {
        console.error('Error deleting task:', error);
    }
}

// Notification Management
async function loadNotifications() {
    try {
        const response = await fetch(`${API_BASE_URL}/notifications`);
        const notifications = await response.json();
        renderNotifications(notifications);
        updateNotificationCount(notifications);
    } catch (error) {
        console.error('Error loading notifications:', error);
    }
}

function renderNotifications(notifications) {
    notificationsList.innerHTML = '';
    notifications.forEach(notification => {
        const notificationElement = createNotificationElement(notification);
        notificationsList.appendChild(notificationElement);
    });
}

function createNotificationElement(notification) {
    const div = document.createElement('div');
    div.className = `notification-item ${notification.read ? '' : 'unread'}`;
    div.innerHTML = `
        <div class="notification-message">${notification.message}</div>
        <div class="notification-time">${new Date(notification.created_at).toLocaleString()}</div>
    `;
    
    if (!notification.read) {
        div.addEventListener('click', () => markNotificationAsRead(notification.id));
    }
    
    return div;
}

async function markNotificationAsRead(notificationId) {
    try {
        const response = await fetch(`${API_BASE_URL}/notifications/${notificationId}/read`, {
            method: 'PUT',
        });

        if (response.ok) {
            loadNotifications();
        }
    } catch (error) {
        console.error('Error marking notification as read:', error);
    }
}

function updateNotificationCount(notifications) {
    const unreadCount = notifications.filter(n => !n.read).length;
    notificationCount.textContent = unreadCount;
}

function toggleNotifications() {
    notificationsPanel.classList.toggle('hidden');
}