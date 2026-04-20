import logging
import time
from app.services.article_service import (
    insert_source, save_articles,
    generate_summaries_for_articles,
    create_and_save_6h_summary
)
from app.fetcher.cnbc import fetch_cnbc_news

#config Logging
logging.basicConfig(
    filemode='automation.log',
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

def run_workflow():
    logging.info("--- Starting News Workflow ---")
    
    try:
        # 1. Test Fetching
        source_id = insert_source("CNBC", "https://www.cnbc.com/id/100003114/device/rss/rss.html")
        entries = fetch_cnbc_news()
        
        if not entries:
            logging.warning("No news fetched. Source might be down or no new articles")
            return
        
        # 2. Test Saving
        new_count = save_articles(entries, source_id)
        logging.info(f"Success saved {new_count} new articles")
        
        # 3. Test AI Summary (Limit 5)
        summary_count = generate_summaries_for_articles(limit=5)
        logging.info(f"Generated {summary_count} summaries")
        
        # 4. Test 6h Summary
        result_message = create_and_save_6h_summary()
        if result_message == "Summary saved":
            logging.info(f"6h summary: {result_message}")
        elif result_message == "No news to summarize":
            logging.info(f"6h summary: {result_message}")
        else:
            logging.warning(f"6h summary: {result_message}")
            
    except Exception as e:
        logging.error(f"Workflow failed: {str(e)}")
        
if __name__ == "__main__":
    run_workflow()