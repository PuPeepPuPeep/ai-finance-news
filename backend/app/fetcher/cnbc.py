import feedparser

RSS_URL = "https://www.cnbc.com/id/100003114/device/rss/rss.html"

def fetch_cnbc_news():
    feed = feedparser.parse(RSS_URL)
    return feed.entries