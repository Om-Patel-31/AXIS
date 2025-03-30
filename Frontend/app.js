const API_BASE_URL = 'http://localhost:5000/api';

// DOM Elements
const taskForm = document.getElementById('task-form');
const tasksList = document.getElementById('tasks-list');
const notificationsPanel = document.getElementById('notifications-panel');
const notificationsList = document.getElementById('notifications-list');
const notificationToggle = document.getElementById('notification-toggle');
const notificationCount = document.getElementById('notification-count');
const voiceToggle = document.getElementById('voice-toggle');
const voiceIndicator = document.getElementById('voice-indicator');
const voiceOutput = document.getElementById('voice-output');
const memoryContent = document.getElementById('memory-content');
const organizeWorkForm = document.getElementById('organize-work-form');
const scheduleForm = document.getElementById('schedule-form');

// State
let isListening = false;

// Event Listeners
taskForm.addEventListener('submit', handleTaskSubmit);
notificationToggle.addEventListener('click', toggleNotifications);
voiceToggle.addEventListener('click', toggleVoiceInput);
organizeWorkForm.addEventListener('submit', handleOrganizeWork);
scheduleForm.addEventListener('submit', handleCreateSchedule);

// Initialize
document.addEventListener('DOMContentLoaded', () => {
    loadTasks();
    loadNotifications();
    loadMemory();
});

// Voice Input
async function toggleVoiceInput() {
    if (!isListening) {
        isListening = true;
        voiceIndicator.classList.add('active');
        voiceToggle.textContent = '⏹';
        
        try {
            const response = await fetch(`${API_BASE_URL}/ai/process-voice`, {
                method: 'POST'
            });
            const data = await response.json();
            
            voiceOutput.textContent = data.command;
            processVoiceCommand(data.intent);
        } catch (error) {
            console.error('Error processing voice input:', error);
            voiceOutput.textContent = 'Error processing voice input';
        } finally {
            isListening = false;
            voiceIndicator.classList.remove('active');
            voiceToggle.textContent = '🎤';
        }
    } else {
        isListening = false;
        voiceIndicator.classList.remove('active');
        voiceToggle.textContent = '🎤';
    }
}

async function processVoiceCommand(intent) {
    // Process the AI's understanding of the command
    console.log('Processing intent:', intent);
    // Add specific actions based on intent
}

// Memory Management
async function loadMemory() {
    try {
        const response = await fetch(`${API_BASE_URL}/ai/memory`);
        const memories = await response.json();
        renderMemory(memories);
    } catch (error) {
        console.error('Error loading memory:', error);
    }
}

function renderMemory(memories) {
    memoryContent.innerHTML = '';
    memories.forEach(memory => {
        const div = document.createElement('div');
        div.className = 'memory-item';
        div.innerHTML = `
            <div class="memory-content">${memory.content}</div>
            <div class="memory-meta">
                <span class="memory-category">${memory.category}</span>
                <span class="memory-date">${new Date(memory.created_at).toLocaleString()}</span>
            </div>
        `;
        memoryContent.appendChild(div);
    });
}

// Academic Tools
async function generateFlashcards() {
    const content = document.getElementById('flashcard-content').value;
    if (!content) return;

    try {
        const response = await fetch(`${API_BASE_URL}/ai/generate-flashcards`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ content }),
        });
        const flashcards = await response.json();
        renderFlashcards(flashcards);
    } catch (error) {
        console.error('Error generating flashcards:', error);
    }
}

function renderFlashcards(flashcards) {
    const container = document.getElementById('flashcards-container');
    container.innerHTML = '';
    
    flashcards.forEach(card => {
        const div = document.createElement('div');
        div.className = 'flashcard';
        div.innerHTML = `
            <div class="flashcard-question">${card.question}</div>
            <div class="flashcard-answer hidden">${card.answer}</div>
        `;
        div.addEventListener('click', () => {
            div.querySelector('.flashcard-answer').classList.toggle('hidden');
        });
        container.appendChild(div);
    });
}

async function summarizeContent() {
    const content = document.getElementById('summary-content').value;
    if (!content) return;

    try {
        const response = await fetch(`${API_BASE_URL}/ai/summarize`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ content }),
        });
        const data = await response.json();
        document.getElementById('summary-output').textContent = data.summary;
    } catch (error) {
        console.error('Error summarizing content:', error);
    }
}

// Automation
async function handleOrganizeWork(event) {
    event.preventDefault();
    
    const subject = document.getElementById('subject').value;
    const content = document.getElementById('content').value;

    try {
        const response = await fetch(`${API_BASE_URL}/automation/organize-work`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ subject, content }),
        });
        
        if (response.ok) {
            organizeWorkForm.reset();
            showNotification('Work organized successfully');
        }
    } catch (error) {
        console.error('Error organizing work:', error);
        showNotification('Error organizing work', 'error');
    }
}

async function handleCreateSchedule(event) {
    event.preventDefault();
    
    const subject = document.getElementById('exam-subject').value;
    const examDate = document.getElementById('exam-date').value;

    try {
        const response = await fetch(`${API_BASE_URL}/automation/create-schedule`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ subject, exam_date: examDate }),
        });
        
        if (response.ok) {
            scheduleForm.reset();
            showNotification('Study schedule created successfully');
        }
    } catch (error) {
        console.error('Error creating schedule:', error);
        showNotification('Error creating schedule', 'error');
    }
}

// Existing Task Management
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

function showNotification(message, type = 'success') {
    const notification = document.createElement('div');
    notification.className = `notification ${type}`;
    notification.textContent = message;
    
    document.body.appendChild(notification);
    
    setTimeout(() => {
        notification.remove();
    }, 3000);
}