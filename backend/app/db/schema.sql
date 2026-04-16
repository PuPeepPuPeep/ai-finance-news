CREATE TABLE IF NOT EXISTS sources (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT UNIQUE,
    rss_url TEXT
);

CREATE TABLE IF NOT EXISTS articles (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    title TEXT,
    content TEXT,
    url TEXT UNIQUE,
    published_at TEXT,
    created_at TEXT,
    source_id INTEGER,
    FOREIGN KEY (source_id) REFERENCES sources(id)
);

CREATE TABLE IF NOT EXISTS summaries (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    summary TEXT,
    model TEXT,
    created_at TEXT,
    article_id INTEGER,
    FOREIGN KEY (article_id) REFERENCES articles(id)
);