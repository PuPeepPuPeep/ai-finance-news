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
    model_used TEXT,
    created_at TEXT,
    article_id INTEGER,
    FOREIGN KEY (article_id) REFERENCES articles(id)
);

CREATE TABLE IF NOT EXISTS topics (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT UNIQUE
);

CREATE TABLE IF NOT EXISTS article_topics (
    article_id INTEGER,
    topic_id INTEGER,
    PRIMARY KEY (article_id, topic_id),
    FOREIGN KEY (article_id) REFERENCES articles(id) ON DELETE CASCADE,
    FOREIGN KEY (topic_id) REFERENCES topics(id) ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS time_summaries (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    summary TEXT,
    model_used TEXT,
    start_time TEXT,
    end_time TEXT,
    created_at TEXT
);

CREATE TABLE IF NOT EXISTS time_summary_articles (
    time_summary_id INTEGER,
    article_id INTEGER,
    PRIMARY KEY (time_summary_id, article_id),
    FOREIGN KEY (time_summary_id) REFERENCES time_summaries(id) ON DELETE CASCADE,
    FOREIGN KEY (article_id) REFERENCES articles(id) ON DELETE CASCADE
);