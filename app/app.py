import os
import time
from flask import Flask, request, render_template_string, redirect, url_for
import mysql.connector

app = Flask(__name__)

def get_db_connection():
    for i in range(15):
        try:
            conn = mysql.connector.connect(
                host=os.getenv('DB_HOST', 'db'),
                user=os.getenv('DB_USER', 'root'),
                password=os.getenv('DB_PASSWORD', 'password'),
                database=os.getenv('DB_NAME', 'tasks_db')
            )
            return conn
        except mysql.connector.Error:
            time.sleep(2)
    return None

conn = get_db_connection()
if conn:
    cursor = conn.cursor()
    cursor.execute("CREATE TABLE IF NOT EXISTS tasks (id INT AUTO_INCREMENT PRIMARY KEY, name VARCHAR(255) NOT NULL);")
    conn.commit()
    cursor.close()
    conn.close()

HTML_TEMPLATE = """
<!DOCTYPE html>
<html>
<head>
    <title>Docker Tasks App</title>
    <style>
        body { font-family: Arial, sans-serif; margin: 40px; }
        input[type="text"] { padding: 8px; width: 250px; }
        input[type="submit"] { padding: 8px 15px; background-color: #28a745; color: white; border: none; cursor: pointer; }
        li { padding: 10px; background: #f4f4f9; margin-bottom: 5px; }
    </style>
</head>
<body>
    <h1>Список задач</h1>
    <form action="/add" method="POST">
        <input type="text" name="task_name" placeholder="Введите задачу" required>
        <input type="submit" value="Добавить">
    </form>
    <ul>
        {% for task in tasks %}
            <li>ID: {{ task[0] }} — {{ task[1] }}</li>
        {% else %}
            <li>Задач пока нет</li>
        {% endfor %}
    </ul>
</body>
</html>
"""

@app.route('/')
def index():
    conn = get_db_connection()
    tasks = []
    if conn:
        cursor = conn.cursor()
        cursor.execute("SELECT id, name FROM tasks ORDER BY id DESC")
        tasks = cursor.fetchall()
        cursor.close()
        conn.close()
    return render_template_string(HTML_TEMPLATE, tasks=tasks)

@app.route('/add', methods=['POST'])
def add_task():
    task_name = request.form.get('task_name')
    if task_name:
        conn = get_db_connection()
        if conn:
            cursor = conn.cursor()
            cursor.execute("INSERT INTO tasks (name) VALUES (%s)", (task_name,))
            conn.commit()
            cursor.close()
            conn.close()
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
