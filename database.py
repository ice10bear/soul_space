import sqlite3
from datetime import datetime

DB_NAME = "soulspace.db"

def init_db():
    """Обновленная инициализация базы данных с новой таблицей истории"""
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    
    # Старая таблица настроек времени
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            user_id INTEGER PRIMARY KEY,
            delivery_mode TEXT DEFAULT 'manual',
            delivery_time TEXT DEFAULT NULL
        )
    ''')
    
    # НОВАЯ таблица для контекста и памяти ИИ
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS history (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER,
            date TEXT,
            sphere TEXT,
            user_mood TEXT,
            bot_response TEXT
        )
    ''')
    conn.commit()
    conn.close()

# ... (функции save_user_settings, get_user_settings и get_users_by_time остаются без изменений) ...

def save_session_to_history(user_id: int, sphere: str, user_mood: str, bot_response: str):
    """Сохраняет завершенную утреннюю сессию в историю"""
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    today_str = datetime.now().strftime("%Y-%m-%d")
    
    cursor.execute('''
        INSERT INTO history (user_id, date, sphere, user_mood, bot_response)
        VALUES (?, ?, ?, ?, ?)
    ''', (user_id, today_str, sphere, user_mood, bot_response))
    
    conn.commit()
    conn.close()

def get_recent_history(user_id: int, limit: int = 3):
    """Достает последние N записей из истории для контекста"""
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    
    cursor.execute('''
        SELECT date, sphere, user_mood, bot_response FROM history
        WHERE user_id = ?
        ORDER BY id DESC
        LIMIT ?
    ''', (user_id, limit))
    
    rows = cursor.fetchall()
    conn.close()
    
    # Разворачиваем историю, чтобы она шла в хронологическом порядке (от старых к новым)
    rows.reverse()
    
    history_text = ""
    for row in rows:
        history_text += f"--- Прошлая сессия ({row[0]}) ---\n"
        history_text += f"Выбранная сфера: {row[1]}\n"
        history_text += f"Что писал пользователь о состоянии: \"{row[2]}\"\n"
        history_text += f"Твой ответ наставника: \"{row[3]}\"\n\n"
        
    return history_text


def get_users_by_time(time_str: str):
    """Возвращает список пользователей, у которых запланирована отправка на это время"""
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute('SELECT user_id, delivery_mode FROM users WHERE delivery_time = ?', (time_str,))
    results = cursor.fetchall()
    conn.close()
    
    # Превращаем результат в удобный список словарей
    return [{"user_id": row[0], "mode": row[1]} for row in results]