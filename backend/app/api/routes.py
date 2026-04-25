from fastapi import APIRouter, HTTPException
from app.db.db import get_connection
from app.api.schemas import ArticleResponse, TimeSummaryResponse
import psycopg2
import logging

router = APIRouter()
logger = logging.getLogger(__name__)

@router.get("/topics", response_model=list[str])
def get_topics():
    try:
        with get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT name FROM topics ORDER BY name ASC")
            rows = cursor.fetchall()
        conn.close()
        return [row["name"] for row in rows]
    except psycopg2.Error as e:
        logger.error(f"Database error in get_topics: {e}")
        raise HTTPException(status_code=500, detail="Failed to fetch topics")

@router.get("/news/summary-6h", response_model=TimeSummaryResponse)
def get_latest_6h_summary():
    try:
        with get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                        SELECT summary, created_at, model_used
                        FROM time_summaries
                        ORDER BY id DESC
                        LIMIT 1
                        """)
            row = cursor.fetchone()
        conn.close()    
        if row:
            return TimeSummaryResponse(
                summary=row["summary"],
                created_at=row["created_at"],
                model_used=row["model_used"]
            )
        return TimeSummaryResponse(summary="ยังไม่มีสรุป")
    except psycopg2.Error as e:
        logger.error(f"Database error in get_latest_6h_summary: {e}")
        raise HTTPException(status_code=500, detail="Failed to fetch summary")

@router.get("/news", response_model=list[ArticleResponse])
def get_news(topic: str = None):
    try:
        with get_connection() as conn:
            cursor = conn.cursor()
            
            base_query = """
                SELECT a.id, a.title, a.url, s.summary, a.published_at,
                    src.name as source_name, s.model_used, s.sentiment,
                    STRING_AGG(t.name, ',') as topics
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
                                        WHERE t2.name = %s)
                                        GROUP BY a.id, a.title, a.url, a.published_at, src.name, s.summary, s.model_used, s.sentiment
                                        ORDER BY a.published_at DESC 
                                        LIMIT 10
                                        """
                cursor.execute(query, (topic,))
            else:
                query = base_query + """ GROUP BY a.id, a.title, a.url, a.published_at, src.name, s.summary, s.model_used, s.sentiment 
                                        ORDER BY a.published_at DESC 
                                        LIMIT 20
                                        """
                cursor.execute(query)
    
            rows = cursor.fetchall()
        conn.close()
        
        return [
            ArticleResponse(
                id=row["id"],
                title=row["title"],
                url=row["url"],
                summary=row["summary"],
                published_at=row["published_at"],
                source_name=row["source_name"],
                model_used=row["model_used"],
                sentiment=row["sentiment"],
                topics=row["topics"].split(",") if row["topics"] else []
            )
            for row in rows
        ]
    except psycopg2.Error as e:
        logger.error(f"Database error in get_news: {e}")
        raise HTTPException(status_code=500, detail="Failed to fetch news")