from flask import Flask, request, jsonify

app = Flask(__name__)

tasks = []  # This will hold tasks in memory

@app.route('/tasks', methods=['GET', 'POST'])
def handle_tasks():
    if request.method == 'POST':
        task = request.json.get('task')
        tasks.append(task)
        return jsonify({'message': 'Task added successfully!'}), 201
    return jsonify(tasks)

if __name__ == '__main__':
    app.run(debug=True)