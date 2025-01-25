from flask import Flask, redirect, url_for
from flask_login import LoginManager
from routers.task import task_router
from routers.auth_registr import auth_router
from routers.user import user_router
from models.user import User 
from backend.db_depends import get_db
import os

app = Flask(__name__)

# Инициализация Flask-Login
login_manager = LoginManager()
login_manager.login_view = 'auth.login'  # Указываем маршрут для страницы логина
login_manager.init_app(app)

app.secret_key = os.urandom(24)

@login_manager.user_loader
def load_user(user_id):
    db = next(get_db())  # Получаем текущую сессию из get_db
    return db.query(User).get(int(user_id))  # Доступ к данным через db напрямую

# Регистрируем роутеры
app.register_blueprint(task_router)
app.register_blueprint(auth_router)
app.register_blueprint(user_router)

@app.route('/')
def home():
    return redirect(url_for('auth.login'))

if __name__ == '__main__':
    app.run(debug=True)