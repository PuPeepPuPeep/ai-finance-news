from app.db.db import init_db
from app.fetcher.cnbc import fetch_cnbc_news
from app.services.article_service import insert_source, save_articles, generate_summaries_for_articles

RSS_URL = "https://www.cnbc.com/id/100003114/device/rss/rss.html"

def main():
    init_db()
    
    source_id = insert_source("CNBC", RSS_URL)
    
    entries = fetch_cnbc_news()
    
    save_articles(entries, source_id)
    
    generate_summaries_for_articles(limit=3)
    
    print("Done fetch and save")
    
if __name__ == "__main__":
    main()