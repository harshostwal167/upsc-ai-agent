"""
UPSC AI Agent - SIMPLIFIED VERSION
This version removes startup complexity
Use this if you're getting errors on Render
"""

from flask import Flask, jsonify, request
from flask_cors import CORS
import json
import sqlite3
from datetime import datetime
import os
import logging

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize Flask
app = Flask(__name__)
CORS(app)

# Configuration
DATABASE = os.environ.get('DATABASE_PATH', 'upsc_articles.db')

# ============================================================================
# DATABASE FUNCTIONS (Simple)
# ============================================================================

def init_database():
    """Initialize SQLite database"""
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
        logger.info("✓ Database initialized")
    except Exception as e:
        logger.error(f"Database init error: {e}")

# Initialize database on startup
init_database()

# ============================================================================
# MOCK DATA (for testing)
# ============================================================================

MOCK_DATA = {
    'prelims': [
        {
            'id': 1,
            'title': 'New Cabinet Ministers Appointed',
            'topic': 'Political Science',
            'source': 'PIB',
            'date': datetime.now().isoformat(),
            'relevance': 'high',
            'summary': 'Cabinet reshuffle with 5 new ministers appointed',
        },
        {
            'id': 2,
            'title': 'RBI Announces New Monetary Policy',
            'topic': 'Economics',
            'source': 'RBI',
            'date': datetime.now().isoformat(),
            'relevance': 'high',
            'summary': 'RBI maintains repo rate. New guidelines for digital banking.',
        },
    ],
    'mains': [
        {
            'id': 3,
            'title': 'Federal Structure and Centre-State Relations',
            'topic': 'Government & Politics',
            'source': 'The Hindu',
            'date': datetime.now().isoformat(),
            'relevance': 'high',
            'summary': 'Analysis of recent Supreme Court judgment on GST distribution',
        },
    ],
    'interview': [
        {
            'id': 4,
            'title': 'How to Prepare for UPSC Interview',
            'topic': 'Interview Strategy',
            'source': 'UPSC Analysis',
            'date': datetime.now().isoformat(),
            'relevance': 'high',
            'summary': 'Tips on linking recent events to governance frameworks',
        },
    ],
    'current-affairs': [
        {
            'id': 5,
            'title': 'Weekly Current Affairs Summary',
            'topic': 'Weekly Summary',
            'source': 'Multiple Sources',
            'date': datetime.now().isoformat(),
            'relevance': 'high',
            'summary': 'Comprehensive weekly summary of major national and international events',
        },
    ],
}

# ============================================================================
# API ENDPOINTS
# ============================================================================

@app.route('/api/health', methods=['GET'])
def health():
    """Health check endpoint"""
    return jsonify({
        'status': 'healthy',
        'timestamp': datetime.now().isoformat(),
        'database': 'sqlite',
        'message': 'Backend is running'
    }), 200

@app.route('/api/articles', methods=['GET'])
def get_articles():
    """Get articles with optional filtering"""
    try:
        category = request.args.get('category', 'all')
        limit = int(request.args.get('limit', 50))
        relevance = request.args.get('relevance', 'all')
        
        # Return mock data
        if category == 'all':
            all_articles = []
            for cat_articles in MOCK_DATA.values():
                all_articles.extend(cat_articles)
        else:
            all_articles = MOCK_DATA.get(category, [])
        
        # Filter by relevance
        if relevance == 'high':
            all_articles = [a for a in all_articles if a.get('relevance') == 'high']
        
        # Limit results
        all_articles = all_articles[:limit]
        
        return jsonify(all_articles), 200
    except Exception as e:
        logger.error(f"Error getting articles: {e}")
        return jsonify({'error': str(e)}), 500

@app.route('/api/stats', methods=['GET'])
def stats():
    """Get statistics"""
    try:
        return jsonify({
            'total_articles': sum(len(v) for v in MOCK_DATA.values()),
            'prelims_items': len(MOCK_DATA.get('prelims', [])),
            'mains_items': len(MOCK_DATA.get('mains', [])),
            'interview_items': len(MOCK_DATA.get('interview', [])),
            'current_affairs_items': len(MOCK_DATA.get('current-affairs', [])),
            'last_update': datetime.now().isoformat(),
            'note': 'Using mock data - real data comes after deployment succeeds'
        }), 200
    except Exception as e:
        logger.error(f"Error getting stats: {e}")
        return jsonify({'error': str(e)}), 500

@app.route('/api/articles/<category>', methods=['GET'])
def get_by_category(category):
    """Get articles by category"""
    try:
        articles = MOCK_DATA.get(category, [])
        return jsonify(articles), 200
    except Exception as e:
        logger.error(f"Error getting category: {e}")
        return jsonify({'error': str(e)}), 500

@app.route('/api/refresh', methods=['POST'])
def refresh():
    """Trigger manual refresh (not implemented in simple version)"""
    return jsonify({
        'status': 'success',
        'message': 'Using mock data. Real news fetching requires full version.',
        'note': 'Deploy successful! Now update to full backend.'
    }), 200

@app.route('/api/search', methods=['POST'])
def search():
    """Search articles"""
    try:
        query = request.json.get('query', '').lower()
        
        if not query:
            return jsonify([])
        
        results = []
        for articles in MOCK_DATA.values():
            for article in articles:
                if query in article.get('title', '').lower() or \
                   query in article.get('summary', '').lower():
                    results.append(article)
        
        return jsonify(results), 200
    except Exception as e:
        logger.error(f"Error searching: {e}")
        return jsonify({'error': str(e)}), 500

# ============================================================================
# ERROR HANDLERS
# ============================================================================

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
    logger.info(f"Starting UPSC AI Agent Backend (Simple Version)")
    logger.info(f"Server running on port {port}")
    logger.info(f"Health check: http://localhost:{port}/api/health")
    logger.info(f"Articles: http://localhost:{port}/api/articles")
    
    app.run(debug=False, host='0.0.0.0', port=port)
