from datetime import datetime, timedelta
from app.db.db import get_connection
from app.services.ai_service import summarize_text, MODEL_NAME, summarize_6h_period
from email.utils import parsedate_to_datetime

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
            #format timedate to ISO
            raw_date = entry.get("published")
            try:
                date_time = parsedate_to_datetime(raw_date)
                published_at = date_time.strftime('%Y-%m-%d %H:%M:%S')
            except Exception:
                published_at = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            cursor.execute("""
                        INSERT OR IGNORE INTO articles
                        (title, content, url, published_at, created_at, source_id)
                        VALUES (?, ?, ?, ?, ?, ?)
                        """, (
                            entry.get("title"),
                            entry.get("summary", ""),
                            entry.get("link"),
                            published_at,
                            datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
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
                result, model_used= summarize_text(content)
                summary = result.get('summary')
                topics = result.get('topics', [])
                
                cursor.execute("""
                            INSERT INTO summaries (summary, model_used, created_at, article_id)
                            VALUES (?, ?, datetime('now'), ?)
                            """, (summary, model_used, article_id))
                
                for topic in topics:
                    cursor.execute("""
                                   INSERT OR IGNORE INTO topics (name) 
                                   VALUES (?)
                                   """, (topic.strip(),))
                    
                    cursor.execute("SELECT id FROM topics WHERE name = ?", (topic.strip(),))
                    topic_id = cursor.fetchone()[0]
                    
                    cursor.execute("""
                                   INSERT OR IGNORE INTO article_topics (article_id, topic_id)
                                   VALUES (?, ?)
                                   """, (article_id, topic_id))
                    
                conn.commit()
                print(f"Success: Article {article_id} classified in to {topics}")
                
            except Exception as e:
                conn.rollback()
                print(f"Error on article {article_id}: {e}")
                
def create_and_save_6h_summary():
    conn = get_connection()
    cursor = conn.cursor()
    
    end_time = datetime.now()
    start_time = end_time - timedelta(hours=6)
    
    cursor.execute("""
                   SELECT a.id, s.summary
                   FROM articles a
                   JOIN summaries s ON a.id = s.article_id
                   WHERE a.published_at >= ?
                   """, (start_time.strftime('%Y-%m-%d %H:%M:%S'),))
    
    rows = cursor.fetchall()
    if not rows:
        return "No news to summarize"
    
    article_ids = [r[0] for r in rows]
    summaries = [r[1] for r in rows]
    
    final_summary = summarize_6h_period(summaries)
    
    cursor.execute("""
                   INSERT INTO time_summaries (summary, start_time, end_time, created_at)
                   VALUES (?, ?, ?, datetime('now'))
                   """, (final_summary, start_time.strftime('%Y-%m-%d %H:%M:%S'), end_time.strftime('%Y-%m-%d %H:%M:%S')))
    
    time_summary_id = cursor.lastrowid
    
    for aid in article_ids:
        cursor.execute("""
                       INSERT INTO time_summary_articles (time_summary_id, article_id)
                       VALUES (?, ?)
                       """, (time_summary_id, aid))
        
    conn.commit()
    conn.close()
    return "Summary saved"