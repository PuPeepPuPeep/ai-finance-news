from datetime import datetime, timedelta, timezone
from app.db.db import get_connection
from app.services.ai_service import summarize_text, MODEL_NAME, summarize_6h_period
from email.utils import parsedate_to_datetime
import time
import logging
import os

AI_REQUEST_DELAY = int(os.getenv("AI_REQUEST_DELAY", "10"))
AI_ERROR_DELAY = int(os.getenv("AI_ERROR_DELAY", "20"))

def insert_source(name, rss_url):
    with get_connection() as conn:
        cursor = conn.cursor()
        
        cursor.execute("""
                    INSERT INTO sources (name, rss_url)
                    VALUES (%s, %s)
                    ON CONFLICT (name) DO NOTHING
                    """, (name, rss_url))
        
        cursor.execute("SELECT id FROM sources WHERE name = %s", (name,))
        source_id = cursor.fetchone()["id"]
        
        return source_id

def save_articles(entries, source_id):
    news_count = 0
    
    with get_connection() as conn:
        cursor = conn.cursor()
        
        for entry in entries:
            #format timedate to ISO
            raw_date = entry.get("published")
            try:
                date_time = parsedate_to_datetime(raw_date)
                if date_time.tzinfo is None:
                    date_time = date_time.replace(tzinfo=timezone.utc)
                published_at = date_time.isoformat()
            except Exception:
                published_at = datetime.now(timezone.utc).isoformat()
            cursor.execute("""
                        INSERT INTO articles
                        (title, content, url, published_at, created_at, source_id)
                        VALUES (%s, %s, %s, %s, %s, %s)
                        ON CONFLICT (url) DO NOTHING
                        """, (
                            entry.get("title"),
                            entry.get("summary", ""),
                            entry.get("link"),
                            published_at,
                            datetime.now(timezone.utc).isoformat(),
                            source_id
                        ))
            
            if cursor.rowcount > 0:
                news_count += 1
            
    return news_count
    
def _get_or_create_topic_id(cursor, topic_name: str) -> int:
    cursor.execute("""
                   INSERT INTO topics (name) 
                   VALUES (%s) 
                   ON CONFLICT (name) DO NOTHING
                   RETURNING id
                   """, (topic_name,))
    row = cursor.fetchone()
    if row:
        return row["id"]
    cursor.execute("SELECT id FROM topics WHERE name = %s", (topic_name,))
    return cursor.fetchone()["id"]

def generate_summaries_for_articles():
    summary_count = 0
    
    with get_connection() as conn:
        cursor = conn.cursor()
        
        cursor.execute("""
                    SELECT id, content
                    FROM articles
                    WHERE id NOT IN (SELECT article_id FROM summaries)
                    """)
        
        rows = cursor.fetchall()
        
        for row in rows:
            article_id = row["id"]
            content = row["content"]
            try:
                result, model_used= summarize_text(content)
                summary = result.get('summary')
                sentiment = result.get('sentiment')
                topics = result.get('topics', [])
                
                cursor.execute("""
                            INSERT INTO summaries (summary, sentiment, model_used, created_at, article_id)
                            VALUES (%s, %s, %s, NOW(), %s)
                            """, (summary, sentiment, model_used, article_id))
                
                for topic in topics:
                    topic_id = _get_or_create_topic_id(cursor, topic.strip())
                    
                    cursor.execute("""
                                   INSERT INTO article_topics (article_id, topic_id)
                                   VALUES (%s, %s)
                                   ON CONFLICT DO NOTHING
                                   """, (article_id, topic_id))
                    
                conn.commit()
                summary_count += 1
                logging.info(f"Summary article {article_id} classified in to {topics}")
                time.sleep(AI_REQUEST_DELAY)
                
            except Exception as e:
                conn.rollback()
                logging.error(f"Error processing article {article_id} ({type(e).__name__}): {e}")
                time.sleep(AI_ERROR_DELAY)
    
    return summary_count
    
def create_and_save_6h_summary():
    with get_connection() as conn:
        cursor = conn.cursor()
        
        end_time = datetime.now(timezone.utc)
        start_time = end_time - timedelta(hours=6)
        
        cursor.execute("""
                    SELECT a.id, s.summary
                    FROM articles a
                    JOIN summaries s ON a.id = s.article_id
                    WHERE a.published_at >= %s
                    """, (start_time.isoformat(),))
        
        rows = cursor.fetchall()
        if not rows:
            return "No news to summarize"
        
        article_ids = [r["id"] for r in rows]
        summaries = [r["summary"] for r in rows]
        
        final_summary, model_used = summarize_6h_period(summaries)
        
        cursor.execute("""
                    INSERT INTO time_summaries (summary, model_used, start_time, end_time, created_at)
                    VALUES (%s, %s, %s, %s, %s)
                    RETURNING id
                    """, (final_summary, model_used, start_time.isoformat(), end_time.isoformat(), datetime.now(timezone.utc).isoformat()
                    ))
        
        time_summary_id = cursor.fetchone()["id"]
        
        for aid in article_ids:
            cursor.execute("""
                        INSERT INTO time_summary_articles (time_summary_id, article_id)
                        VALUES (%s, %s)
                        """, (time_summary_id, aid))
            
        conn.commit()
    return "Summary saved"