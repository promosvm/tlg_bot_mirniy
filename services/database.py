import sqlite3

from services.dto import UserData

DB_PATH = './base/telegram_bot_data.db'


def get_connection() -> sqlite3.Connection:
    """Открывает соединение с базой данных SQLite."""
    return sqlite3.connect(DB_PATH, check_same_thread=False)


def init_db(conn: sqlite3.Connection) -> None:
    """Создаёт таблицы, если их ещё нет."""
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            user_id INTEGER PRIMARY KEY,
            username TEXT,
            first_name TEXT,
            last_name TEXT,
            join_date DATETIME,
            join_count INTEGER
        )
    ''')
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS user_activity (
            user_id INTEGER PRIMARY KEY,
            activity_date TEXT,
            activity_count INTEGER
        )
    ''')
    conn.commit()


def get_user(conn: sqlite3.Connection, user_id: int):
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM users WHERE user_id = ?', (user_id,))
    return cursor.fetchone()


def add_user(conn: sqlite3.Connection, user: UserData, join_count: int = 1) -> bool:
    """Добавляет пользователя в базу, если его ещё нет."""
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM users WHERE user_id = ?', (user.user_id,))
    if cursor.fetchone() is not None:
        return False
    cursor.execute(
        '''INSERT INTO users (user_id, username, first_name, last_name, join_date, join_count)
           VALUES (?, ?, ?, ?, ?, ?)''',
        (
            user.user_id,
            user.username,
            user.first_name,
            user.last_name,
            user.join_date,
            join_count,
        ),
    )
    conn.commit()
    return True
