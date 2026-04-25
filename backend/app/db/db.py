import psycopg2
import psycopg2.extras
import os

def get_connection():
    conn = psycopg2.connect(os.getenv("DATABASE_URL"))
    conn.cursor_factory = psycopg2.extras.RealDictCursor
    return conn

def init_db():
    with get_connection() as conn:
        cursor = conn.cursor()
        with open("app/db/schema.sql", "r", encoding="utf-8") as f:
            cursor.execute(f.read())
        conn.commit()
    conn.close()