import argparse
import logging
from app.services.article_service import (
    insert_source, save_articles,
    generate_summaries_for_articles,
    create_and_save_6h_summary
)
from app.fetcher.cnbc import fetch_cnbc_news

#config Logging
logging.basicConfig(
    filename='automation.log',
    filemode='a',
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

def run_main_workflow():
    logging.info("--- Starting News Workflow ---")
    
    try:
        # 1. Fetching
        source_id = insert_source("CNBC", "https://www.cnbc.com/id/100003114/device/rss/rss.html")
        entries = fetch_cnbc_news()
        
        if not entries:
            logging.warning("No news fetched. Source might be down or no new articles")
            return
        
        # 2. Saving
        news_count = save_articles(entries, source_id)
        logging.info(f"Success saved {news_count} new articles")
        
        # 3. AI Summary
        summary_count = generate_summaries_for_articles()
        logging.info(f"Generated {summary_count} summaries")
        
        
            
    except Exception as e:
        logging.error(f"Workflow failed: {str(e)}")

def run_6h_summary():
    try:
        # 6h Summary
        result_message = create_and_save_6h_summary()
        if result_message == "Summary saved":
            logging.info(f"6h summary: {result_message}")
        elif result_message == "No news to summarize":
            logging.info(f"6h summary: {result_message}")
        else:
            logging.warning(f"6h summary: {result_message}")
            
    except Exception as e:
        logging.error(f"6h summary failed: {str(e)}")

if __name__ == "__main__":
    
    parser = argparse.ArgumentParser(description="Run news workflow tasks")
    
    parser.add_argument(
        "--task",
        choices=["main", "6h"],
        required=True,
        help="Specify the task to run: 'main' for workflow, '6h' for 6h summary" 
    )
    
    args = parser.parse_args()
    
    if args.task == "main":
        run_main_workflow()
    elif args.task == "6h":
        run_6h_summary()