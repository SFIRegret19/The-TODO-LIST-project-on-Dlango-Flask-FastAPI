from flask import Blueprint, render_template, request, redirect, session, url_for, jsonify
from flask_login import current_user, login_required
from models.task import Task
from backend.db_depends import get_db
from schemas import CreateTask, UpdateTask
from datetime import datetime, timezone
from slugify import slugify
from enums.task_priority import Priority  # Импортируем Enum для приоритета

task_router = Blueprint('task', __name__, url_prefix='/tasks')

# Функция для преобразования строки в значение Enum
def map_priority_string_to_enum(priority_string: str) -> Priority:
    priority_map = {
        'Не важное_Не срочное': Priority.NOT_URGENT_NOT_IMPORTANT,
        'Важное_Не срочное': Priority.IMPORTANT_NOT_URGENT,
        'Не важное_Срочное': Priority.NOT_URGENT_URGENT,
        'Важное_Срочное': Priority.IMPORTANT_URGENT,
    }
    if priority_string not in priority_map:
        raise ValueError(f"Невалидное значение приоритета: {priority_string}")
    return priority_map[priority_string]

@login_required
@task_router.route('/view_all')
def view_tasks():
    with next(get_db()) as db:
        tasks = db.query(Task).order_by(Task.created_at.desc()).all()
    return render_template('tasks.html', tasks=tasks, user=current_user, username=current_user.username)

# Создание задач
@task_router.route('/create', methods=['GET', 'POST'])
def create_task():
    with next(get_db()) as db:
        if request.method == 'POST':
            task_data = request.form.to_dict()

            # Преобразуем форму в данные схемы CreateTask с помощью Pydantic
            validated_data = CreateTask(**task_data)

            # Преобразуем строковое значение priority в Enum
            priority = map_priority_string_to_enum(validated_data.priority)

            new_task = Task(
                title=validated_data.title,
                content=validated_data.content,
                priority=priority,
                category=validated_data.category,
                progress=validated_data.progress,
                attachment=validated_data.attachment or None,
                user_id=current_user.id,  # Используйте реального пользователя
                due_date=validated_data.due_date,
                created_at=datetime.now(timezone.utc),
                slug=slugify(validated_data.title)
            )

            db.add(new_task)
            db.commit()

            return redirect(url_for('task.view_tasks'))

    return render_template('add_task.html')  # Шаблон для добавления задачи

# Изменение задач
@task_router.route('/edit/<int:task_id>', methods=['GET', 'POST'])
def edit_task(task_id):
    with next(get_db()) as db:
        task = db.query(Task).filter_by(id=task_id).first()
        if not task:
            return jsonify({"error": "Task not found"}), 404

        if request.method == 'POST':
            task_data = request.form.to_dict()
            validated_data = UpdateTask(**task_data)

            # Преобразуем строковое значение priority в Enum, если оно задано
            if validated_data.priority:
                validated_data.priority = map_priority_string_to_enum(validated_data.priority)

            for key, value in validated_data.model_dump(exclude_unset=True).items():
                if key == 'due_date' and value == '':  # Проверяем, если due_date пустое, оставляем старое значение
                    value = task.due_date
                setattr(task, key, value)

            task.updated_at = datetime.now(timezone.utc)
            db.commit()

            # После сохранения изменений, редиректим на страницу задач
            return redirect(url_for('task.view_tasks'))

    # Передаем задачу в шаблон
    return render_template('edit_task.html', task=task, priority=task.priority.value)

# Удаление задачи
@task_router.route('/delete/<int:task_id>', methods=['POST'])
def delete_task(task_id):
    with next(get_db()) as db:
        task = db.query(Task).filter_by(id=task_id).first()
        if not task:
            return jsonify({"error": "Task not found"}), 404

        db.delete(task)
        db.commit()

    return redirect(url_for('task.view_tasks'))

# Пометить задачу как завершенную
@task_router.route('/mark_completed/<int:task_id>', methods=['POST'])
def mark_task_completed(task_id):
    with next(get_db()) as db:
        task = db.query(Task).filter_by(id=task_id).first()
        if not task:
            return jsonify({"error": "Task not found"}), 404

        task.mark_completed()
        db.commit()

    return redirect(url_for('task.view_tasks'))