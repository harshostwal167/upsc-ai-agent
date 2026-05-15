"""
UPSC AI Agent - LIVE NEWS VERSION
Fetches real news from RSS feeds - no API key needed
"""

from flask import Flask, jsonify, request
from flask_cors import CORS
import sqlite3
from datetime import datetime
import os
import logging
import feedparser
import threading
import time

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize Flask
app = Flask(__name__)
CORS(app)

# Configuration
DATABASE = os.environ.get('DATABASE_PATH', 'upsc_articles.db')

# ============================================================================
# RSS FEEDS (All free, no API key needed)
# ============================================================================

RSS_FEEDS = [
    # PIB
    { 'url': 'https://pib.gov.in/RssMain.aspx?ModId=6&Lang=1&Regid=3', 'source': 'PIB', 'category': 'current-affairs' },
    # The Hindu
    { 'url': 'https://www.thehindu.com/news/national/feeder/default.rss', 'source': 'The Hindu', 'category': 'current-affairs' },
    { 'url': 'https://www.thehindu.com/opinion/editorial/feeder/default.rss', 'source': 'The Hindu Editorial', 'category': 'mains' },
    # Indian Express
    { 'url': 'https://indianexpress.com/section/india/feed/', 'source': 'Indian Express', 'category': 'current-affairs' },
    { 'url': 'https://indianexpress.com/section/explained/feed/', 'source': 'IE Explained', 'category': 'mains' },
    # DD News
    { 'url': 'https://ddnews.gov.in/feed/', 'source': 'DD News', 'category': 'current-affairs' },
    # Economic Times
    { 'url': 'https://economictimes.indiatimes.com/news/economy/rssfeeds/1373380680.cms', 'source': 'Economic Times', 'category': 'prelims' },
]

# Keywords to classify articles
PRELIMS_KEYWORDS = [
    'rbi', 'repo rate', 'gdp', 'inflation', 'budget', 'scheme', 'act', 'bill', 'parliament',
    'constitution', 'supreme court', 'high court', 'election', 'commission', 'upsc', 'ias',
    'ministry', 'cabinet', 'president', 'governor', 'article', 'amendment', 'policy',
    'national park', 'wildlife', 'geography', 'river', 'dam', 'mission', 'award'
]

MAINS_KEYWORDS = [
    'analysis', 'explained', 'editorial', 'opinion', 'impact', 'reform', 'governance',
    'federal', 'centre state', 'development', 'inequality', 'poverty', 'education',
    'healthcare', 'environment', 'climate', 'foreign policy', 'diplomacy', 'economy',
    'social', 'culture', 'technology', 'agriculture', 'infrastructure', 'security'
]

INTERVIEW_KEYWORDS = [
    'interview', 'debate', 'controversy', 'challenge', 'crisis', 'international',
    'geopolitics', 'bilateral', 'multilateral', 'united nations', 'g20', 'brics',
    'india china', 'india pakistan', 'india us', 'global', 'world'
]

# ============================================================================
# DATABASE FUNCTIONS
# ============================================================================

def init_database():
    try:
        conn = sqlite3.connect(DATABASE)
        c = conn.cursor()
        c.execute('''CREATE TABLE IF NOT EXISTS articles (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            summary TEXT,
            url TEXT UNIQUE NOT NULL,
            source TEXT,
            published_date TEXT,
            fetched_date TEXT,
            category TEXT,
            relevance TEXT DEFAULT 'medium',
            created_at TEXT
        )''')
        conn.commit()
        conn.close()
        logger.info("✓ Database initialized")
    except Exception as e:
        logger.error(f"Database init error: {e}")

init_database()

# ============================================================================
# NEWS FETCHING
# ============================================================================

def classify_article(title, summary, source_category):
    """Classify article into UPSC categories based on keywords"""
    text = (title + ' ' + summary).lower()
    categories = set()

    # Always add source category
    categories.add(source_category)

    # Check keywords
    if any(kw in text for kw in PRELIMS_KEYWORDS):
        categories.add('prelims')
    if any(kw in text for kw in MAINS_KEYWORDS):
        categories.add('mains')
    if any(kw in text for kw in INTERVIEW_KEYWORDS):
        categories.add('interview')

    # Always add to current-affairs
    categories.add('current-affairs')

    return list(categories)

def get_relevance(title, summary):
    """Determine relevance score"""
    text = (title + ' ' + summary).lower()
    high_keywords = ['upsc', 'ias', 'policy', 'supreme court', 'parliament', 'rbi', 'budget', 'election', 'constitution', 'act', 'bill', 'ministry']
    if any(kw in text for kw in high_keywords):
        return 'high'
    return 'medium'

def fetch_and_store_news():
    """Fetch news from all RSS feeds and store in database"""
    logger.info("🔄 Fetching live news from RSS feeds...")
    total_saved = 0

    for feed_info in RSS_FEEDS:
        try:
            feed = feedparser.parse(feed_info['url'])
            conn = sqlite3.connect(DATABASE)
            c = conn.cursor()

            for entry in feed.entries[:10]:  # Max 10 per feed
                title = entry.get('title', '').strip()
                summary = entry.get('summary', entry.get('description', '')).strip()
                url = entry.get('link', '').strip()
                source = feed_info['source']

                # Parse date
                published = datetime.now().isoformat()
                if hasattr(entry, 'published_parsed') and entry.published_parsed:
                    try:
                        published = datetime(*entry.published_parsed[:6]).isoformat()
                    except Exception:
                        pass

                if not title or not url:
                    continue

                # Classify and get relevance
                categories = classify_article(title, summary, feed_info['category'])
                relevance = get_relevance(title, summary)

                # Store once per category
                for category in categories:
                    try:
                        c.execute('''INSERT OR IGNORE INTO articles
                            (title, summary, url, source, published_date, fetched_date, category, relevance, created_at)
                            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)''',
                            (title, summary[:500], url, source, published,
                             datetime.now().isoformat(), category, relevance,
                             datetime.now().isoformat()))
                        total_saved += c.rowcount
                    except Exception:
                        pass

            conn.commit()
            conn.close()
            logger.info(f"✓ Fetched from {feed_info['source']}")

        except Exception as e:
            logger.error(f"Error fetching {feed_info['source']}: {e}")

    logger.info(f"✅ Total new articles saved: {total_saved}")
    return total_saved

def get_articles_from_db(category='all', limit=20):
    """Get articles from database"""
    try:
        conn = sqlite3.connect(DATABASE)
        c = conn.cursor()

        if category == 'all':
            c.execute('''SELECT id, title, summary, url, source, published_date, category, relevance
                        FROM articles ORDER BY published_date DESC LIMIT ?''', (limit,))
        else:
            c.execute('''SELECT id, title, summary, url, source, published_date, category, relevance
                        FROM articles WHERE category = ? ORDER BY published_date DESC LIMIT ?''',
                        (category, limit))

        rows = c.fetchall()
        conn.close()

        articles = []
        for row in rows:
            articles.append({
                'id': row[0],
                'title': row[1],
                'summary': row[2] or '',
                'url': row[3],
                'source': row[4],
                'date': row[5],
                'topic': row[6],
                'relevance': row[7],
                'content': row[2] or ''
            })
        return articles
    except Exception as e:
        logger.error(f"DB fetch error: {e}")
        return []

def background_refresh():
    """Refresh news every 6 hours in background"""
    while True:
        try:
            fetch_and_store_news()
        except Exception as e:
            logger.error(f"Background refresh error: {e}")
        time.sleep(6 * 60 * 60)  # 6 hours

# Fetch news on startup
fetch_and_store_news()

# Start background refresh thread
refresh_thread = threading.Thread(target=background_refresh, daemon=True)
refresh_thread.start()

# ============================================================================
# API ENDPOINTS
# ============================================================================

@app.route('/api/health', methods=['GET'])
def health():
    return jsonify({
        'status': 'healthy',
        'timestamp': datetime.now().isoformat(),
        'database': 'sqlite',
        'message': 'Backend is running with live news'
    }), 200

@app.route('/api/news', methods=['GET'])
def get_news():
    """Get news grouped by category - matches frontend format"""
    try:
        result = {}
        for category in ['prelims', 'mains', 'interview', 'current-affairs']:
            result[category] = get_articles_from_db(category, limit=10)

        # If database is empty, trigger a fetch
        total = sum(len(v) for v in result.values())
        if total == 0:
            fetch_and_store_news()
            for category in ['prelims', 'mains', 'interview', 'current-affairs']:
                result[category] = get_articles_from_db(category, limit=10)

        return jsonify(result), 200
    except Exception as e:
        logger.error(f"Error getting news: {e}")
        return jsonify({'error': str(e)}), 500

@app.route('/api/articles', methods=['GET'])
def get_articles():
    """Get articles with optional filtering"""
    try:
        category = request.args.get('category', 'all')
        limit = int(request.args.get('limit', 50))
        articles = get_articles_from_db(category, limit)
        return jsonify(articles), 200
    except Exception as e:
        logger.error(f"Error getting articles: {e}")
        return jsonify({'error': str(e)}), 500

@app.route('/api/stats', methods=['GET'])
def stats():
    try:
        conn = sqlite3.connect(DATABASE)
        c = conn.cursor()
        c.execute('SELECT category, COUNT(*) FROM articles GROUP BY category')
        rows = c.fetchall()
        conn.close()

        counts = {row[0]: row[1] for row in rows}
        return jsonify({
            'total_articles': sum(counts.values()),
            'prelims_items': counts.get('prelims', 0),
            'mains_items': counts.get('mains', 0),
            'interview_items': counts.get('interview', 0),
            'current_affairs_items': counts.get('current-affairs', 0),
            'last_update': datetime.now().isoformat(),
        }), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/refresh', methods=['POST'])
def refresh():
    """Manually trigger news refresh"""
    try:
        count = fetch_and_store_news()
        return jsonify({
            'status': 'success',
            'new_articles': count,
            'message': f'Fetched latest news successfully'
        }), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/search', methods=['POST'])
def search():
    try:
        query = request.json.get('query', '').lower()
        if not query:
            return jsonify([])

        conn = sqlite3.connect(DATABASE)
        c = conn.cursor()
        c.execute('''SELECT id, title, summary, url, source, published_date, category, relevance
                    FROM articles WHERE LOWER(title) LIKE ? OR LOWER(summary) LIKE ?
                    ORDER BY published_date DESC LIMIT 20''',
                    (f'%{query}%', f'%{query}%'))
        rows = c.fetchall()
        conn.close()

        results = [{'id': r[0], 'title': r[1], 'summary': r[2], 'url': r[3],
                    'source': r[4], 'date': r[5], 'topic': r[6], 'relevance': r[7]} for r in rows]
        return jsonify(results), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.errorhandler(404)
def not_found(error):
    return jsonify({'error': 'Endpoint not found'}), 404

@app.errorhandler(500)
def server_error(error):
    return jsonify({'error': 'Internal server error'}), 500

# ============================================================================
# MAIN
# ============================================================================

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    logger.info(f"Starting UPSC AI Agent - Live News Backend")
    logger.info(f"Port: {port}")
    app.run(debug=False, host='0.0.0.0', port=port)
