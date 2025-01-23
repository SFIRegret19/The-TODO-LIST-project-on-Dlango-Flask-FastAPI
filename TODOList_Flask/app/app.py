from flask import Flask, render_template
from backend.db_depends import get_db
from models.task import Task
from routers.task import task_router

app = Flask(__name__)

# Регистрируем task_router
app.register_blueprint(task_router)

# Просмотр всех задач:
@app.route('/')
def view_tasks():
    db = next(get_db())
    tasks = db.query(Task).order_by(Task.created_at.desc()).all()
    return render_template('tasks.html', tasks=tasks)


if __name__ == '__main__':
    app.run(debug=True)