from flask import Flask, render_template, request, redirect, url_for
from backend.db import *

app = Flask(__name__)

# Инициализация базы данных при первом запросе
with app.app_context():
    init_db()

@app.route('/')
def welcome_page():
    conn = get_db_connection()
    tasks = conn.execute('SELECT * FROM tasks ORDER BY created_at DESC').fetchall()
    conn.close()
    return render_template('index.html', tasks=tasks)

@app.route('/add', methods=['POST'])
def add_task():
    if request.method == 'POST':
        title = request.form['title']
        description = request.form.get('description', default='')
        user = request.form.get('user', default='Anonymous')
        priority = request.form.get('priority', default='Normal')
        category = request.form.get('category', default='Uncategorized')
        due_date = request.form.get('due_date', default=None)

        conn = get_db_connection()
        conn.execute(
            'INSERT INTO tasks (user, title, description, priority, category, due_date) VALUES (?, ?, ?, ?, ?, ?)',
            (user, title, description, priority, category, due_date)
        )
        conn.commit()
        conn.close()
        return redirect(url_for('welcome_page'))
    return render_template('add_task.html')

@app.route('/delete/<int:task_id>')
def delete_task(task_id):
    conn = get_db_connection()
    conn.execute('DELETE FROM tasks WHERE id = ?', (task_id,))
    conn.commit()
    conn.close()
    return redirect(url_for('welcome_page'))

if __name__ == "__main__":
    app.run(debug=True)