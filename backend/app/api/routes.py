from fastapi import APIRouter
from app.db.db import get_connection

router = APIRouter()

@router.get("/topics")
def get_topics():
    conn = get_connection()
    cursor = conn.cursor()
    
    cursor.execute("SELECT name FROM topics ORDER BY name ASC")
    rows = cursor.fetchall()
    conn.close()
    
    return [r[0] for r in rows]

@router.get("/news/summary-6h")
def get_lastest_6h_summary():
    conn = get_connection()
    cursor = conn.cursor()
    
    cursor.execute("""
                   SELECT summary 
                   FROM time_summaries
                   ORDER BY id DESC
                   LIMIT 1
                   """)
    row = cursor.fetchone()
    conn.close()
    
    if row:
        return {"summary": row[0]}
    return {"summary": "ยังไม่มีสรุป"}

@router.get("/news")
def get_news(topic: str = None):
    conn = get_connection()
    cursor = conn.cursor()
    
    base_query = """
        SELECT a.id, a.title, a.url, s.summary, a.published_at,
            src.name as source_name, s.model_used, s.sentiment,
            GROUP_CONCAT(t.name) as topics
        FROM articles a
        LEFT JOIN sources src ON a.source_id = src.id
        LEFT JOIN summaries s ON a.id = s.article_id
        LEFT JOIN article_topics at ON a.id = at.article_id
        LEFT JOIN topics t ON at.topic_id = t.id    
    """
    
    if topic and topic != "Latest":
        query = base_query + """ WHERE a.id IN (
                                SELECT article_id 
                                FROM article_topics at2 
                                JOIN topics t2 ON at2.topic_id = t2.id
                                WHERE t2.name = ?)
                                GROUP BY a.id
                                ORDER BY a.published_at DESC 
                                LIMIT 10
                                """
        cursor.execute(query, (topic,))
    else:
        query = base_query + """ GROUP BY a.id 
                                ORDER BY a.published_at DESC 
                                LIMIT 20
                                """
        cursor.execute(query)
    
    rows = cursor.fetchall()
    conn.close()
    
    news = []
    for r in rows:
        news.append({
            "id": r[0],
            "title": r[1],
            "url": r[2],
            "summary": r[3],
            "published_at": r[4],
            "source_name": r[5],
            "model_used": r[6],
            "sentiment": r[7],
            "topics": r[8].split(',') if r[8] else []
        })
        
    return news

@router.get("/news/{article_id}")
def get_news_detail(article_id: int):
    conn = get_connection()
    cursor = conn.cursor()
    
    cursor.execute("""
                   SELECT id, title, content, url, published_at
                   FROM articles
                   WHERE id = ?
                   """, (article_id,))
    
    row = cursor.fetchone()
    conn.close()
    
    if not row:
        return {"error": "Not found"}
    
    return {
        "id": row[0],
        "title": row[1],
        "content": row[2],
        "url": row[3],
        "published_at": row[4]
    }
    