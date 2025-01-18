# bot/utils/database.py

import psycopg2
from config.config import Config


def get_db_connection():
    return psycopg2.connect(**Config.DATABASE_CONFIG)


def execute_query(query, params=None, fetchone=False, fetchall=False):
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


def is_admin(user_id):
    result = execute_query(
        "SELECT role FROM users WHERE user_id = %s",
        (user_id,),
        fetchone=True
    )
    return result and result[0] == "admin"
