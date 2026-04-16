from fastapi import APIRouter
from app.db.db import get_connection

router = APIRouter()

@router.get("/news")
def get_news():
    conn = get_connection()
    cursor = conn.cursor()
    
    cursor.execute("""
                   SELECT a.id, a.title, a.url, s.summary, a.published_at, s.created_at
                   FROM articles a
                   LEFT JOIN summaries s ON a.id = s.article_id
                   ORDER BY a.published_at DESC
                   LIMIT 20
                   """)
    
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
            "created_at": r[5]
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