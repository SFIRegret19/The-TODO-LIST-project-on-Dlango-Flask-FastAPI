from flask import Blueprint, render_template, request, redirect, url_for, jsonify
from models.task import Task
from backend.db_depends import get_db
from schemas import CreateTask, UpdateTask
from datetime import datetime, timezone
from slugify import slugify

task_router = Blueprint('task', __name__, url_prefix='/tasks')

# Создание задач
@task_router.route('/create', methods=['GET', 'POST'])
def create_task():

    # Создаем сессию через get_db
    db = next(get_db())

    if request.method == 'POST':
        task_data = request.form.to_dict()
        validated_data = CreateTask(**task_data)

        new_task = Task(
            title=validated_data.title,
            content=validated_data.content,
            priority=validated_data.priority,
            category=validated_data.category,
            progress=validated_data.progress,
            attachment=validated_data.attachment or None,
            user_id=1,  # Укажите текущего пользователя, либо замените реальной аутентификацией
            due_date=datetime.strptime(validated_data.due_date, '%Y-%m-%d'),
            created_at = datetime.now(timezone.utc),
            slug=slugify(validated_data.title)
        )

        db.add(new_task)
        db.commit()

        return redirect(url_for('view_tasks'))
    return render_template('add_task.html')  # Используется шаблон добавления задачи

# Изменение задач
@task_router.route('/edit/<int:task_id>', methods=['GET', 'POST'])
def edit_task(task_id):

    db = next(get_db())

    task = db.query(Task).filter_by(id=task_id).first()
    if not task:
        return jsonify({"error": "Task not found"}), 404

    if request.method == 'POST':
        task_data = request.form.to_dict()
        validated_data = UpdateTask(**task_data)

        # Преобразование due_date в формат datetime, если оно присутствует
        if validated_data.due_date:
            validated_data.due_date = datetime.strptime(validated_data.due_date, '%Y-%m-%d')


        for key, value in validated_data.model_dump(exclude_unset=True).items():
            if key == 'due_date' and value == '':
                value = task.due_date
            setattr(task, key, value)

        task.updated_at = datetime.now(timezone.utc)
        db.commit()

        return redirect(url_for('view_tasks'))
    return render_template('edit_task.html', task=task)

@task_router.route('/delete/<int:task_id>', methods=['POST'])
def delete_task(task_id):
    db = next(get_db())
    
    # Ищем задачу по ID
    task = db.query(Task).filter_by(id=task_id).first()
    if not task:
        return jsonify({"error": "Task not found"}), 404

    # Удаляем задачу из базы данных
    db.delete(task)
    db.commit()

    return redirect(url_for('view_tasks'))