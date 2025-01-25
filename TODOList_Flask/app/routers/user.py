from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import current_user, login_required
from models.user import User
from backend.db_depends import get_db

user_router = Blueprint('user', __name__, url_prefix='/user')

@login_required
@user_router.route('/edit_profile', methods=['GET', 'POST'])
def edit_profile():
    db = next(get_db())  # Получаем сессию базы данных из get_db()

    # Проверка, что текущий пользователь авторизован
    if not current_user.is_authenticated:
        flash('Пожалуйста, войдите в систему', 'danger')
        return redirect(url_for('auth.login'))  # Перенаправляем на страницу логина

    if request.method == 'POST':
        # Получаем новые данные из формы
        username = request.form.get('username')
        email = request.form.get('email')

        # Проверка, если имя пользователя изменилось, выполняем проверку на уникальность
        if username != current_user.username:
            user_exists = db.query(User).filter_by(username=username).first()
            if user_exists:
                flash('Имя пользователя уже занято', 'danger')
                return redirect(url_for('user.edit_profile'))
        
        # Проверка, если email изменился, выполняем проверку на уникальность
        if email != current_user.email:
            email_exists = db.query(User).filter_by(email=email).first()
            if email_exists:
                flash('Этот email уже используется', 'danger')
                return redirect(url_for('user.edit_profile'))

        # Обновляем данные пользователя
        current_user.username = username
        current_user.email = email

        # Сохраняем изменения в базе данных
        db.merge(current_user)  # Обновляем объект в базе данных
        db.commit()  # Применяем изменения в базе данных

        flash('Ваш профиль был успешно обновлен!', 'success')
        return redirect(url_for('task.view_tasks'))  # Перенаправляем обратно на страницу задач

    return render_template('user.html', user=current_user)  # Передаем текущего пользователя