import sqlite3

DB_NAME = "news.db"

def get_connection():
    conn = sqlite3.connect(DB_NAME)
    conn.execute("PRAGMA journal_mode=WAL;")
    conn.execute("PRAGMA busy_timeout = 10000;") # timeout 1 min
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    conn = get_connection()
    cursor = conn.cursor()
    
    with open("app/db/schema.sql", "r") as f:
        cursor.executescript(f.read())
        
    conn.commit()
    conn.close()