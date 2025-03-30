from datetime import datetime
import uuid

class TaskManager:
    def __init__(self):
        self.tasks = {}

    def create_task(self, title, description, due_date=None):
        task_id = str(uuid.uuid4())
        task = {
            'id': task_id,
            'title': title,
            'description': description,
            'due_date': due_date,
            'completed': False,
            'created_at': datetime.utcnow().isoformat()
        }
        self.tasks[task_id] = task
        return task

    def get_all_tasks(self):
        return list(self.tasks.values())

    def get_task_by_id(self, task_id):
        return self.tasks.get(task_id)

    def update_task(self, task_id, data):
        if task_id not in self.tasks:
            return None
        
        task = self.tasks[task_id]
        task.update({
            'title': data.get('title', task['title']),
            'description': data.get('description', task['description']),
            'due_date': data.get('due_date', task['due_date']),
            'completed': data.get('completed', task['completed'])
        })
        return task

    def delete_task(self, task_id):
        if task_id in self.tasks:
            del self.tasks[task_id]
            return True
        return False
