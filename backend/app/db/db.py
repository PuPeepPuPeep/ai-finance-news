import psycopg2
import psycopg2.extras
import os
import time
import logging

logger = logging.getLogger(__name__)

def get_connection():
    conn = psycopg2.connect(os.getenv("DATABASE_URL"))
    conn.cursor_factory = psycopg2.extras.RealDictCursor
    return conn

def init_db():
    max_retries = 5
    for attempt in range(max_retries):
        try:
            with get_connection() as conn:
                cursor = conn.cursor()
                with open("app/db/schema.sql", "r", encoding="utf-8") as f:
                    cursor.execute(f.read())
                conn.commit()
            conn.close()
            logger.info("Database initialized successfully")
            return
        except psycopg2.OperationalError as e:
            if attempt < max_retries -1:
                logger.warning(f"Database not ready (attempt {attempt + 1}/{max_retries}), retrying in 5s... {e}")
                time.sleep(5)
            else:
                logger.error("Failed to initialize database after max retries")
                raise
    