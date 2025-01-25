from flask import Blueprint, render_template, request, redirect, url_for, flash

auth_router = Blueprint('auth', __name__, url_prefix='/auth')

# Форма входа
@auth_router.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        # Здесь логика проверки пользователя
        if email == 'test@example.com' and password == 'password123':  # Пример
            flash('Вы успешно вошли!', 'success')
            return redirect(url_for('task.view_tasks'))
        flash('Неверные данные для входа', 'danger')
    return render_template('auth.html')

# Форма регистрации
@auth_router.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        password = request.form['password']
        password_confirm = request.form['password_confirm']
        
        # Проверка совпадения паролей
        if password != password_confirm:
            flash('Пароли не совпадают', 'danger')
            return redirect(url_for('auth.register'))

        # Логика добавления нового пользователя в базу данных
        flash('Регистрация успешна! Можете войти.', 'success')
        return redirect(url_for('auth.login'))
    return render_template('auth.html')
