from pydantic import BaseModel
from typing import Optional

class ArticleResponse(BaseModel):
    id: int
    title: Optional[str] = None
    url: Optional[str] = None
    summary: Optional[str] = None
    published_at: Optional[str] = None
    source_name: Optional[str] = None
    model_used: Optional[str] = None
    sentiment: Optional[str] = None
    topics: list[str] = []
    
class TimeSummaryResponse(BaseModel):
    summary: str
    created_at: Optional[str] = None
    model_used: Optional[str] = None