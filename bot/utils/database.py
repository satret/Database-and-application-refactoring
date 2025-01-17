# bot/utils/database.py

import psycopg2
from psycopg2 import sql
from config.config import Config

def get_db_connection():
    """Возвращает соединение с базой данных."""
    return psycopg2.connect(**Config.DATABASE_CONFIG)

def execute_query(query, params=None, fetchone=False, fetchall=False):
    """Выполняет SQL-запрос и возвращает результат."""
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute(query, params)
    result = None
    if fetchone:
        result = cursor.fetchone()
    elif fetchall:
        result = cursor.fetchall()
    conn.commit()
    cursor.close()
    conn.close()
    return result