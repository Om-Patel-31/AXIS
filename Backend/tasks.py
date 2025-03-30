from datetime import datetime

class Task:
    def __init__(self, title, description=None, due_date=None, completed=False):
        self.id = datetime.now().strftime("%Y%m%d%H%M%S")
        self.title = title
        self.description = description
        self.due_date = due_date
        self.completed = completed
        self.created_at = datetime.now()

    def to_dict(self):
        return {
            'id': self.id,
            'title': self.title,
            'description': self.description,
            'due_date': self.due_date,
            'completed': self.completed,
            'created_at': self.created_at.isoformat()
        }

tasks = []

def add_task(title, description=None, due_date=None):
    task = Task(title, description, due_date)
    tasks.append(task)
    return task

def get_all_tasks():
    return [task.to_dict() for task in tasks]

def get_task_by_id(task_id):
    for task in tasks:
        if task.id == task_id:
            return task
    return None

def update_task(task_id, title=None, description=None, due_date=None, completed=None):
    task = get_task_by_id(task_id)
    if task:
        if title is not None:
            task.title = title
        if description is not None:
            task.description = description
        if due_date is not None:
            task.due_date = due_date
        if completed is not None:
            task.completed = completed
        return task
    return None

def delete_task(task_id):
    task = get_task_by_id(task_id)
    if task:
        tasks.remove(task)
        return True
    return False
