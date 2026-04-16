from datetime import datetime
from app.db.db import get_connection
from app.services.ai_service import summarize_text

def insert_source(name, rss_url):
    with get_connection() as conn:
        cursor = conn.cursor()
        
        cursor.execute("""
                    INSERT OR IGNORE INTO sources (name, rss_url)
                    VALUES (?, ?)
                    """, (name, rss_url))
        
        cursor.execute("SELECT id FROM sources WHERE name = ?", (name,))
        source_id = cursor.fetchone()[0]
        
        return source_id

def save_articles(entries, source_id):
    with get_connection() as conn:
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
    
def generate_summaries_for_articles(limit=5):
    with get_connection() as conn:
        cursor = conn.cursor()
        
        cursor.execute("""
                    SELECT id, content
                    FROM articles
                    WHERE id NOT IN (SELECT article_id FROM summaries)
                    LIMIT ?
                    """, (limit,))
        
        rows = cursor.fetchall()
        
        for article_id, content in rows:
            try:
                summary = summarize_text(content)
                
                cursor.execute("""
                            INSERT INTO summaries (summary, model, created_at, article_id)
                            VALUES (?, ?, datetime('now'), ?)
                            """, (summary, "gemini-3-flash-preview", article_id))
            except Exception as e:
                print(f"Error on article {article_id}: {e}")