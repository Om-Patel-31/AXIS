// Fetch tasks from the backend
function fetchTasks() {
    fetch('http://127.0.0.1:5000/tasks')
        .then(response => response.json())
        .then(data => {
            const taskList = document.getElementById('taskList');
            taskList.innerHTML = '';
            data.forEach(task => {
                const li = document.createElement('li');
                li.textContent = task;
                taskList.appendChild(li);
            });
        });
}

// Add a new task
function addTask() {
    const taskInput = document.getElementById('taskInput');
    const task = taskInput.value;
    if (task) {
        fetch('http://127.0.0.1:5000/tasks', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ task })
        })
        .then(() => {
            taskInput.value = ''; // Clear the input field
            fetchTasks(); // Refresh the task list
        });
    }
}

// Initial fetch
fetchTasks();