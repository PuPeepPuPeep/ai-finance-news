import sqlite3

DB_NAME = "news.db"

def get_connection():
    return sqlite3.connect(DB_NAME)

def init_db():
    conn = get_connection()
    cursor = conn.cursor()
    
    with open("app/db/schema.sql", "r") as f:
        cursor.executescript(f.read())
        
    conn.commit()
    conn.close()