"""
UPSC AI Agent - Production Backend
Handles news fetching, categorization, and serving to frontend
"""

from flask import Flask, jsonify, request
from flask_cors import CORS
from anthropic import Anthropic
import feedparser
import json
import sqlite3
from datetime import datetime, timedelta
from apscheduler.schedulers.background import BackgroundScheduler
import logging
import os
from dotenv import load_dotenv

load_dotenv()

# Configuration
app = Flask(__name__)
CORS(app)
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize Anthropic client
anthropic_client = Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY", ""))

# Database initialization
DATABASE = "upsc_articles.db"

def init_database():
    """Initialize SQLite database"""
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
        content TEXT,
        
        prelims_relevant INTEGER,
        mains_relevant INTEGER,
        interview_relevant INTEGER,
        current_affairs_relevant INTEGER,
        relevance_score INTEGER,
        
        prelims_topics TEXT,
        mains_topics TEXT,
        interview_angles TEXT,
        study_notes TEXT,
        
        created_at TEXT,
        updated_at TEXT
    )''')
    
    conn.commit()
    conn.close()

init_database()

# ============================================================================
# NEWS FETCHING
# ============================================================================

class NewsAggregator:
    """Fetch news from multiple sources"""
    
    def __init__(self):
        self.feeds = {
            'pib': 'https://pib.gov.in/allreleasessfeed.xml',
            'the_hindu': 'https://feeds.thehindu.com/news/national/',
            'indian_express': 'https://feeds.indianexpress.com/news/india/',
            'business_standard': 'https://www.business-standard.com/rss/rssfeed.php?section=economy',
        }
    
    def fetch_all_feeds(self):
        """Fetch from all configured feeds"""
        all_articles = []
        
        for source_name, feed_url in self.feeds.items():
            try:
                logger.info(f"Fetching from {source_name}...")
                feed = feedparser.parse(feed_url)
                
                for entry in feed.entries[:15]:  # Get last 15 entries per source
                    article = {
                        'title': entry.get('title', 'No title'),
                        'summary': entry.get('summary', '')[:500],  # Truncate
                        'url': entry.get('link', ''),
                        'published': entry.get('published', datetime.now().isoformat()),
                        'source': source_name.replace('_', ' ').title(),
                        'source_id': source_name,
                    }
                    
                    # Avoid duplicates
                    if not any(a['url'] == article['url'] for a in all_articles):
                        all_articles.append(article)
                        
            except Exception as e:
                logger.error(f"Error fetching {source_name}: {str(e)}")
        
        logger.info(f"Total articles fetched: {len(all_articles)}")
        return all_articles

# ============================================================================
# AI CATEGORIZATION
# ============================================================================

class NewsCategorizerUPSC:
    """Categorize news for UPSC preparation using Claude"""
    
    def __init__(self):
        self.client = anthropic_client
    
    def categorize_article(self, article):
        """Use Claude to categorize article for UPSC"""
        
        try:
            prompt = f"""Analyze this news article for UPSC IAS exam preparation:

Title: {article['title']}
Summary: {article['summary']}
Source: {article['source']}

Provide ONLY a JSON response with:
{{
    "prelims": {{"relevant": true/false, "topics": ["topic1", "topic2"], "explanation": "brief explanation"}},
    "mains": {{"relevant": true/false, "essay_topics": ["essay1"], "explanation": "brief explanation"}},
    "interview": {{"relevant": true/false, "angles": ["angle1"], "explanation": "brief explanation"}},
    "current_affairs": {{"score": 1-10, "keywords": ["keyword1", "keyword2"]}},
    "overall_relevance": "high/medium/low"
}}

Be strict and accurate. Only mark relevant if truly useful for UPSC.
Return ONLY the JSON, no other text, no markdown backticks."""

            message = self.client.messages.create(
                model="claude-opus-4-6",
                max_tokens=500,
                messages=[
                    {"role": "user", "content": prompt}
                ]
            )
            
            response_text = message.content[0].text.strip()
            # Remove any markdown code blocks if present
            response_text = response_text.replace('```json', '').replace('```', '').strip()
            
            result = json.loads(response_text)
            return result
            
        except Exception as e:
            logger.error(f"Error categorizing article: {str(e)}")
            return {
                "prelims": {"relevant": False},
                "mains": {"relevant": False},
                "interview": {"relevant": False},
                "current_affairs": {"score": 0},
                "overall_relevance": "low"
            }
    
    def generate_study_notes(self, article, categories):
        """Generate concise study notes"""
        
        try:
            if categories['overall_relevance'] == 'low':
                return ""
            
            prompt = f"""Create brief UPSC study notes from this news (max 200 words):

Title: {article['title']}
Summary: {article['summary']}

Include:
1. Key Facts (3-4 bullets)
2. UPSC Relevance
3. Possible Question
4. Related Topic

Keep it concise and focused."""

            message = self.client.messages.create(
                model="claude-opus-4-6",
                max_tokens=300,
                messages=[
                    {"role": "user", "content": prompt}
                ]
            )
            
            return message.content[0].text
            
        except Exception as e:
            logger.error(f"Error generating notes: {str(e)}")
            return ""

# ============================================================================
# DATABASE OPERATIONS
# ============================================================================

def article_exists(url):
    """Check if article already in database"""
    conn = sqlite3.connect(DATABASE)
    c = conn.cursor()
    c.execute('SELECT id FROM articles WHERE url = ?', (url,))
    result = c.fetchone()
    conn.close()
    return result is not None

def save_article(article_data):
    """Save article to database"""
    conn = sqlite3.connect(DATABASE)
    c = conn.cursor()
    
    now = datetime.now().isoformat()
    
    try:
        c.execute('''INSERT INTO articles (
            title, summary, url, source, published_date, fetched_date,
            prelims_relevant, mains_relevant, interview_relevant,
            current_affairs_relevant, relevance_score,
            prelims_topics, mains_topics, interview_angles,
            study_notes, created_at, updated_at
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)''', (
            article_data.get('title'),
            article_data.get('summary'),
            article_data.get('url'),
            article_data.get('source'),
            article_data.get('published'),
            now,
            1 if article_data.get('categories', {}).get('prelims', {}).get('relevant') else 0,
            1 if article_data.get('categories', {}).get('mains', {}).get('relevant') else 0,
            1 if article_data.get('categories', {}).get('interview', {}).get('relevant') else 0,
            1 if article_data.get('categories', {}).get('current_affairs', {}).get('score', 0) >= 5 else 0,
            article_data.get('categories', {}).get('current_affairs', {}).get('score', 0),
            json.dumps(article_data.get('categories', {}).get('prelims', {}).get('topics', [])),
            json.dumps(article_data.get('categories', {}).get('mains', {}).get('essay_topics', [])),
            json.dumps(article_data.get('categories', {}).get('interview', {}).get('angles', [])),
            article_data.get('study_notes', ''),
            now,
            now
        ))
        conn.commit()
        logger.info(f"✓ Saved: {article_data['title'][:60]}")
    except sqlite3.IntegrityError:
        logger.info(f"⊘ Duplicate URL: {article_data['title'][:60]}")
    except Exception as e:
        logger.error(f"Error saving article: {str(e)}")
    finally:
        conn.close()

def get_articles(category=None, limit=50, relevance_filter='all'):
    """Retrieve articles from database"""
    conn = sqlite3.connect(DATABASE)
    c = conn.cursor()
    
    query = 'SELECT * FROM articles WHERE 1=1'
    params = []
    
    if category and category != 'all':
        column = f'{category}_relevant'
        query += f' AND {column} = 1'
    
    if relevance_filter == 'high':
        query += ' AND relevance_score >= 7'
    
    query += ' ORDER BY fetched_date DESC LIMIT ?'
    params.append(limit)
    
    c.execute(query, params)
    columns = [description[0] for description in c.description]
    articles = [dict(zip(columns, row)) for row in c.fetchall()]
    
    conn.close()
    return articles

def get_stats():
    """Get database statistics"""
    conn = sqlite3.connect(DATABASE)
    c = conn.cursor()
    
    c.execute('SELECT COUNT(*) FROM articles')
    total = c.fetchone()[0]
    
    c.execute('SELECT COUNT(*) FROM articles WHERE prelims_relevant = 1')
    prelims = c.fetchone()[0]
    
    c.execute('SELECT COUNT(*) FROM articles WHERE mains_relevant = 1')
    mains = c.fetchone()[0]
    
    c.execute('SELECT COUNT(*) FROM articles WHERE interview_relevant = 1')
    interview = c.fetchone()[0]
    
    c.execute('SELECT COUNT(*) FROM articles WHERE current_affairs_relevant = 1')
    ca = c.fetchone()[0]
    
    c.execute('SELECT MAX(fetched_date) FROM articles')
    last_update = c.fetchone()[0]
    
    conn.close()
    
    return {
        'total_articles': total,
        'prelims_items': prelims,
        'mains_items': mains,
        'interview_items': interview,
        'current_affairs_items': ca,
        'last_update': last_update
    }

# ============================================================================
# DAILY PROCESSING PIPELINE
# ============================================================================

class UpscAgentPipeline:
    """Main pipeline for daily news processing"""
    
    def __init__(self):
        self.aggregator = NewsAggregator()
        self.categorizer = NewsCategorizerUPSC()
    
    def run(self):
        """Execute the full pipeline"""
        logger.info(f"\n{'='*60}")
        logger.info(f"[{datetime.now()}] Starting UPSC News Pipeline...")
        logger.info(f"{'='*60}")
        
        try:
            # Step 1: Fetch news
            articles = self.aggregator.fetch_all_feeds()
            
            if not articles:
                logger.warning("No articles fetched!")
                return
            
            # Step 2: Process each article
            processed = 0
            for article in articles:
                if not article_exists(article['url']):
                    logger.info(f"\nProcessing: {article['title'][:60]}")
                    
                    # Categorize
                    categories = self.categorizer.categorize_article(article)
                    
                    # Generate notes if relevant
                    study_notes = ""
                    if categories.get('overall_relevance') != 'low':
                        study_notes = self.categorizer.generate_study_notes(article, categories)
                    
                    # Save to DB
                    save_article({
                        **article,
                        'categories': categories,
                        'study_notes': study_notes
                    })
                    processed += 1
            
            logger.info(f"\n{'='*60}")
            logger.info(f"✓ Pipeline completed! Processed {processed} new articles")
            logger.info(f"{'='*60}\n")
            
        except Exception as e:
            logger.error(f"Pipeline error: {str(e)}")

# ============================================================================
# FLASK API ENDPOINTS
# ============================================================================

@app.route('/api/articles', methods=['GET'])
def get_articles_endpoint():
    """Get articles with optional filtering"""
    category = request.args.get('category', 'all')
    limit = int(request.args.get('limit', 50))
    relevance = request.args.get('relevance', 'all')
    
    articles = get_articles(category, limit, relevance)
    
    # Parse JSON fields
    for article in articles:
        try:
            article['prelims_topics'] = json.loads(article['prelims_topics'] or '[]')
            article['mains_topics'] = json.loads(article['mains_topics'] or '[]')
            article['interview_angles'] = json.loads(article['interview_angles'] or '[]')
        except:
            pass
    
    return jsonify(articles)

@app.route('/api/stats', methods=['GET'])
def stats_endpoint():
    """Get statistics"""
    return jsonify(get_stats())

@app.route('/api/refresh', methods=['POST'])
def refresh_endpoint():
    """Manually trigger pipeline"""
    try:
        pipeline = UpscAgentPipeline()
        pipeline.run()
        return jsonify({'status': 'success', 'message': 'Pipeline executed'}), 200
    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)}), 500

@app.route('/api/health', methods=['GET'])
def health_endpoint():
    """Health check"""
    return jsonify({
        'status': 'healthy',
        'timestamp': datetime.now().isoformat(),
        'database': 'sqlite'
    })

@app.route('/api/search', methods=['POST'])
def search_endpoint():
    """Search articles"""
    query = request.json.get('query', '')
    
    if not query:
        return jsonify([])
    
    conn = sqlite3.connect(DATABASE)
    c = conn.cursor()
    
    search_pattern = f"%{query}%"
    c.execute('''SELECT * FROM articles 
                 WHERE title LIKE ? OR summary LIKE ? 
                 ORDER BY fetched_date DESC LIMIT 20''',
              (search_pattern, search_pattern))
    
    columns = [description[0] for description in c.description]
    articles = [dict(zip(columns, row)) for row in c.fetchall()]
    
    conn.close()
    return jsonify(articles)

# ============================================================================
# SCHEDULING
# ============================================================================

def schedule_daily_job():
    """Schedule the pipeline to run daily"""
    scheduler = BackgroundScheduler()
    
    def job():
        pipeline = UpscAgentPipeline()
        pipeline.run()
    
    # Run at 6 AM IST every day
    scheduler.add_job(job, 'cron', hour=6, minute=0)
    
    try:
        scheduler.start()
        logger.info("✓ Daily scheduler started (6 AM IST)")
    except Exception as e:
        logger.error(f"Scheduler error: {str(e)}")

# ============================================================================
# INITIALIZATION
# ============================================================================

if __name__ == '__main__':
    # Run initial pipeline on startup
    logger.info("Starting UPSC AI Agent Backend...")
    pipeline = UpscAgentPipeline()
    pipeline.run()
    
    # Schedule daily jobs
    schedule_daily_job()
    
    # Start Flask app
    logger.info("Starting Flask server on http://localhost:5000")
    app.run(debug=False, host='0.0.0.0', port=5000)
