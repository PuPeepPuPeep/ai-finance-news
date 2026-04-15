from datetime import datetime
from app.db.db import get_connection

def insert_source(name, rss_url):
    conn = get_connection()
    cursor = conn.cursor()
    
    cursor.execute("""
                   INSERT OR IGNORE INTO sources (name, rss_url)
                   VALUES (?, ?)
                   """, (name, rss_url))
    
    conn.commit()
    
    cursor.execute("SELECT id FROM sources WHERE name = ?", (name,))
    source_id = cursor.fetchone()[0]
    
    conn.close()
    return source_id

def save_articles(entries, source_id):
    conn = get_connection()
    cursor = conn.cursor()
    
    for entry in entries:
        cursor.execute("""
                       INSERT OR IGNORE INTO articles
                       (title, content, url, published_at, created_at, source_id)
                       VALUES (?, ?, ?, ?, ?, ?)
                       """, (
                           entry.get("title"),
                           entry.get("summary", ""),
                           entry.get("link"),
                           entry.get("published", ""),
                           datetime.utcnow().isoformat(),
                           source_id
                       ))
        
    conn.commit()
    conn.close()