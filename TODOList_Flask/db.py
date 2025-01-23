import sqlite3


def init_db():
    conn = get_db_connection()
    # Создание таблицы для задач
    conn.execute('''
        CREATE TABLE IF NOT EXISTS tasks (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user TEXT NOT NULL,
            title TEXT NOT NULL,
            description TEXT,
            priority TEXT DEFAULT 'Normal',
            is_completed BOOLEAN DEFAULT 0,
            created_at TEXT DEFAULT CURRENT_TIMESTAMP,
            due_date TEXT,
            updated_at TEXT,
            category TEXT,
            progress INTEGER DEFAULT 0,
            attachment TEXT,
            completed_at TEXT
        )
    ''')
    conn.close()

def get_db_connection():
    conn = sqlite3.connect('database.db')
    conn.row_factory = sqlite3.Row  # Получение строк как словарей
    return conn

def close_db_connection(conn):
    conn.close()