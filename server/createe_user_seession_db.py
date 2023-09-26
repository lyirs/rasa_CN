import sqlite3
from sqlite3 import Error

def create_connection(db_file):
    conn = None
    try:
        conn = sqlite3.connect(db_file)
    except Error as e:
        print(e)

    if conn is not None:
        return conn

def create_user_sessions_table():
    conn = create_connection("user_sessions.db")
    with conn:
        cur = conn.cursor()
        cur.execute('''CREATE TABLE IF NOT EXISTS user_sessions (
                        user_id TEXT NOT NULL,
                        session_id TEXT NOT NULL
                       );''')

create_user_sessions_table()
