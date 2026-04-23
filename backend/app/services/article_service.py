from datetime import datetime, timedelta, timezone
from app.db.db import get_connection
from app.services.ai_service import summarize_text, MODEL_NAME, summarize_6h_period
from email.utils import parsedate_to_datetime
import time
import logging

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
                        INSERT OR IGNORE INTO articles
                        (title, content, url, published_at, created_at, source_id)
                        VALUES (?, ?, ?, ?, ?, ?)
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
        
        for article_id, content in rows:
            try:
                result, model_used= summarize_text(content)
                summary = result.get('summary')
                sentiment = result.get('sentiment')
                topics = result.get('topics', [])
                
                cursor.execute("""
                            INSERT INTO summaries (summary, sentiment, model_used, created_at, article_id)
                            VALUES (?, ?, ?, datetime('now'), ?)
                            """, (summary, sentiment, model_used, article_id))
                
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
                summary_count += 1
                logging.info(f"Summary article {article_id} classified in to {topics}")
                time.sleep(10)
                
            except Exception as e:
                conn.rollback()
                logging.error(f"Error on article {article_id}: {str(e)}")
                time.sleep(20)
    
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
                    WHERE a.published_at >= ?
                    """, (start_time.isoformat(),))
        
        rows = cursor.fetchall()
        if not rows:
            return "No news to summarize"
        
        article_ids = [r[0] for r in rows]
        summaries = [r[1] for r in rows]
        
        final_summary, model_used = summarize_6h_period(summaries)
        
        cursor.execute("""
                    INSERT INTO time_summaries (summary, model_used, start_time, end_time, created_at)
                    VALUES (?, ?, ?, ?, ?)
                    """, (final_summary, model_used, start_time.isoformat(), end_time.isoformat(), datetime.now(timezone.utc).isoformat()
                    ))
        
        time_summary_id = cursor.lastrowid
        
        for aid in article_ids:
            cursor.execute("""
                        INSERT INTO time_summary_articles (time_summary_id, article_id)
                        VALUES (?, ?)
                        """, (time_summary_id, aid))
            
        conn.commit()
    return "Summary saved"