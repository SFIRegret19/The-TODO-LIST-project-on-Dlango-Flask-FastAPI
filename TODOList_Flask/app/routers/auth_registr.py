from flask import Blueprint, render_template, request, redirect, url_for, flash
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_user, logout_user
from backend.db_depends import get_db
from models.user import User

auth_router = Blueprint('auth', __name__, url_prefix='/auth')

# Форма входа
@auth_router.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        db = next(get_db())
        username = request.form['username']
        password = request.form['password']

        # Проверка пользователя в базе данных
        user = db.query(User).filter_by(username=username).first()
        if user and check_password_hash(user.password_hash, password):
            login_user(user)  # Используем login_user для аутентификации
            flash(f'Добро пожаловать, {user.firstname}!', 'success')
            return redirect(url_for('task.view_tasks'))  # Перенаправление на список задач
        flash('Неверное имя пользователя или пароль', 'danger')

    return render_template('login.html')

# Форма регистрации
@auth_router.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        db = next(get_db())
        username = request.form['username']
        email = request.form['email']
        firstname = request.form['firstname']
        lastname = request.form['lastname']
        age = request.form['age']
        password = request.form['password']
        password_confirm = request.form['password_confirm']

        # Проверка совпадения паролей
        if password != password_confirm:
            flash('Пароли не совпадают', 'danger')
            return redirect(url_for('auth.register'))

        # Проверка существования пользователя
        if db.query(User).filter((User.username == username) | (User.email == email)).first():
            flash('Пользователь с таким именем или email уже существует', 'danger')
            return redirect(url_for('auth.register'))

        # Хэширование пароля и сохранение нового пользователя
        hashed_password = generate_password_hash(password, method='pbkdf2:sha256')
        new_user = User(
            username=username,
            email=email,
            firstname=firstname,
            lastname=lastname,
            age=age,
            password_hash=hashed_password
        )
        db.add(new_user)
        db.commit()

        flash('Регистрация успешна! Теперь вы можете войти.', 'success')
        return redirect(url_for('auth.login'))  # После регистрации перенаправляем на страницу входа

    return render_template('register.html')

# Маршрут для выхода
@auth_router.route('/log_out')
def logout():
    logout_user()  # Используем logout_user для выхода
    flash('Вы успешно вышли из системы.', 'success')
    return redirect(url_for('auth.login'))  # Перенаправляем на страницу входа