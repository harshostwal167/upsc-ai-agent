import React, { useState, useEffect, useCallback } from 'react';
import { ChevronDown, AlertCircle, Radio, RefreshCw } from 'lucide-react';

const UPSCAgent = () => {
  const [activeTab, setActiveTab] = useState('dashboard');
  const [selectedCategory, setSelectedCategory] = useState('all');
  const [loading, setLoading] = useState(false);
  const [expandedCard, setExpandedCard] = useState(null);
  const [lastUpdated, setLastUpdated] = useState(new Date());

  const categories = [
    { id: 'prelims', label: 'Prelims', icon: '📋', color: 'from-blue-500 to-blue-600' },
    { id: 'mains', label: 'Mains', icon: '📚', color: 'from-purple-500 to-purple-600' },
    { id: 'interview', label: 'Interview', icon: '🎤', color: 'from-orange-500 to-orange-600' },
    { id: 'current-affairs', label: 'Current Affairs', icon: '📰', color: 'from-green-500 to-green-600' },
  ];

  const sources = [
    { id: 'pib', name: 'PIB (Press Information Bureau)', url: 'https://pib.gov.in' },
    { id: 'thehindu', name: 'The Hindu', url: 'https://thehindu.com' },
    { id: 'icc', name: 'Indian Express', url: 'https://indianexpress.com' },
    { id: 'bbc', name: 'BBC India', url: 'https://bbc.com/news/world/india' },
    { id: 'prs', name: 'PRS India', url: 'https://prsindia.org' },
  ];

  const mockNewsData = {
    prelims: [
      {
        id: 1,
        title: 'New Cabinet Ministers Appointed',
        topic: 'Political Science',
        source: 'PIB',
        date: '2025-05-15',
        relevance: 'high',
        summary: 'Cabinet reshuffle with 5 new ministers appointed across key portfolios.',
        content: 'The Prime Minister announced a major cabinet reshuffle. Key articles: Article 75-78.',
      },
      {
        id: 2,
        title: 'RBI Announces New Monetary Policy',
        topic: 'Economics',
        source: 'RBI',
        date: '2025-05-14',
        relevance: 'high',
        summary: 'RBI maintains repo rate at 6.5% amid inflation concerns.',
        content: 'The Reserve Bank of India announced its latest monetary policy stance.',
      },
    ],
    mains: [
      {
        id: 3,
        title: 'Federal Structure and Centre-State Relations',
        topic: 'Government & Politics',
        source: 'The Hindu',
        date: '2025-05-15',
        relevance: 'high',
        summary: 'Analysis of recent Supreme Court judgment on GST distribution.',
        content: 'Comprehensive analysis of the federal structure in India.',
        essay: 'Analyze the evolution of Centre-State relations in post-independent India.',
      },
    ],
    interview: [
      {
        id: 4,
        title: 'How to Prepare for UPSC Interview',
        topic: 'Interview Strategy',
        source: 'UPSC Analysis',
        date: '2025-05-15',
        relevance: 'high',
        summary: 'Tips on linking recent events to governance frameworks.',
        content: 'Interview boards often ask candidates to relate current affairs to governance.',
        questions: [
          'Recent RBI monetary policy - implications for financial inclusion?',
          'Cabinet reshuffle - what does it suggest about government priorities?',
        ],
      },
    ],
    'current-affairs': [
      {
        id: 5,
        title: 'Weekly Current Affairs Summary',
        topic: 'Weekly Summary',
        source: 'Multiple Sources',
        date: '2025-05-15',
        relevance: 'high',
        summary: 'Comprehensive weekly summary of major events.',
        sections: {
          National: ['Cabinet reshuffle announced', 'RBI monetary policy review'],
          International: ['UN Climate Summit', 'Trade negotiations'],
        },
      },
    ],
  };

  const fetchNews = useCallback(() => {
    setLoading(true);
    setTimeout(() => {
      setLastUpdated(new Date());
      setLoading(false);
    }, 1500);
  }, []);

  useEffect(() => {
    fetchNews();
  }, [fetchNews]);

  const getNewsForCategory = () => {
    if (selectedCategory === 'all') {
      return Object.values(mockNewsData).flat();
    }
    return mockNewsData[selectedCategory] || [];
  };

  const filteredNews = getNewsForCategory();

  const renderTabContent = () => {
    if (activeTab === 'dashboard') {
      return (
        <div className="space-y-8">
          <div className="grid grid-cols-1 md:grid-cols-4 gap-4">
            {[
              { label: 'Prelims Items', count: mockNewsData.prelims?.length || 0, color: 'bg-blue-50 border-blue-200' },
              { label: 'Mains Items', count: mockNewsData.mains?.length || 0, color: 'bg-purple-50 border-purple-200' },
              { label: 'Interview Tips', count: mockNewsData.interview?.length || 0, color: 'bg-orange-50 border-orange-200' },
              { label: 'CA Updates', count: mockNewsData['current-affairs']?.length || 0, color: 'bg-green-50 border-green-200' },
            ].map((stat, i) => (
              <div key={i} className={`${stat.color} border rounded-lg p-4 text-center`}>
                <div className="text-3xl font-bold">{stat.count}</div>
                <p className="text-sm text-gray-600 mt-1">{stat.label}</p>
              </div>
            ))}
          </div>

          <div className="flex items-center justify-between bg-gradient-to-r from-slate-50 to-slate-100 border border-slate-200 rounded-lg p-4">
            <div>
              <p className="text-sm text-gray-600">Last Updated</p>
              <p className="font-semibold text-gray-800">{lastUpdated.toLocaleString()}</p>
            </div>
            <button
              onClick={fetchNews}
              disabled={loading}
              className="flex items-center gap-2 px-4 py-2 bg-gradient-to-r from-blue-500 to-blue-600 text-white rounded-lg hover:from-blue-600 hover:to-blue-700 transition disabled:opacity-50"
            >
              <RefreshCw size={18} className={loading ? 'animate-spin' : ''} />
              {loading ? 'Updating...' : 'Fetch Latest'}
            </button>
          </div>

          <div>
            <h3 className="text-lg font-bold mb-3 flex items-center gap-2">
              <Radio size={20} /> Official Sources
            </h3>
            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-3">
              {sources.map((source) => (
                <a
                  key={source.id}
                  href={source.url}
                  target="_blank"
                  rel="noopener noreferrer"
                  className="p-3 border border-gray-200 rounded-lg hover:border-blue-400 hover:bg-blue-50 transition"
                >
                  <p className="font-semibold text-sm text-gray-800">{source.name}</p>
                  <p className="text-xs text-gray-500 mt-1">Direct link ↗</p>
                </a>
              ))}
            </div>
          </div>
        </div>
      );
    }

    if (activeTab === 'news') {
      return (
        <div className="space-y-4">
          <div className="flex gap-2 flex-wrap">
            <button
              onClick={() => setSelectedCategory('all')}
              className={`px-4 py-2 rounded-lg transition ${
                selectedCategory === 'all'
                  ? 'bg-slate-800 text-white'
                  : 'bg-gray-100 text-gray-700 hover:bg-gray-200'
              }`}
            >
              All News
            </button>
            {categories.map((cat) => (
              <button
                key={cat.id}
                onClick={() => setSelectedCategory(cat.id)}
                className={`px-4 py-2 rounded-lg transition ${
                  selectedCategory === cat.id
                    ? `bg-gradient-to-r ${cat.color} text-white`
                    : 'bg-gray-100 text-gray-700 hover:bg-gray-200'
                }`}
              >
                {cat.icon} {cat.label}
              </button>
            ))}
          </div>

          <div className="space-y-4">
            {filteredNews.length === 0 ? (
              <div className="text-center py-12 text-gray-500">
                <AlertCircle className="mx-auto mb-2" />
                No items found in this category
              </div>
            ) : (
              filteredNews.map((item) => (
                <div
                  key={item.id}
                  className="border border-gray-200 rounded-lg overflow-hidden hover:shadow-lg transition"
                >
                  <button
                    onClick={() =>
                      setExpandedCard(expandedCard === item.id ? null : item.id)
                    }
                    className="w-full p-4 text-left hover:bg-gray-50 transition"
                  >
                    <div className="flex items-start justify-between">
                      <div className="flex-1">
                        <div className="flex items-center gap-2 mb-2">
                          <span className="text-xs font-semibold px-2 py-1 bg-blue-100 text-blue-700 rounded">
                            {item.source}
                          </span>
                          <span className={`text-xs font-semibold px-2 py-1 rounded ${
                            item.relevance === 'high'
                              ? 'bg-red-100 text-red-700'
                              : 'bg-yellow-100 text-yellow-700'
                          }`}>
                            {item.relevance === 'high' ? '⭐ High' : '⭐ Medium'} Relevance
                          </span>
                        </div>
                        <h3 className="text-lg font-bold text-gray-800">{item.title}</h3>
                        <p className="text-sm text-gray-600 mt-1">
                          📌 {item.topic} • {new Date(item.date).toLocaleDateString()}
                        </p>
                        <p className="text-sm text-gray-700 mt-2">{item.summary}</p>
                      </div>
                      <ChevronDown
                        size={20}
                        className={`text-gray-400 transition ${
                          expandedCard === item.id ? 'rotate-180' : ''
                        }`}
                      />
                    </div>
                  </button>

                  {expandedCard === item.id && (
                    <div className="border-t border-gray-200 bg-gray-50 p-4 space-y-3">
                      <div>
                        <h4 className="font-semibold text-sm text-gray-700 mb-2">Detailed Content:</h4>
                        <p className="text-sm text-gray-700 leading-relaxed">{item.content}</p>
                      </div>
                    </div>
                  )}
                </div>
              ))
            )}
          </div>
        </div>
      );
    }

    return (
      <div className="space-y-6">
        <div className="bg-gradient-to-br from-blue-50 to-indigo-50 border border-blue-200 rounded-lg p-6">
          <h3 className="text-lg font-bold text-gray-800 mb-4">Study Strategy</h3>
          <div className="space-y-3 text-sm text-gray-700">
            <p>Review daily news updates related to your UPSC exam preparation.</p>
            <p>Use the filters to focus on Prelims, Mains, or Interview relevant content.</p>
            <p>Share with your study group using the dashboard link.</p>
          </div>
        </div>
      </div>
    );
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-slate-900 via-slate-800 to-slate-900">
      <style>{`
        @import url('https://fonts.googleapis.com/css2?family=Outfit:wght@400;600;700;800&display=swap');
        body { font-family: 'Outfit', sans-serif; }
      `}</style>

      <div className="bg-gradient-to-r from-slate-800 to-slate-900 border-b border-slate-700 sticky top-0 z-50">
        <div className="max-w-6xl mx-auto px-6 py-4">
          <div className="flex items-center justify-between">
            <div className="flex items-center gap-3">
              <div className="text-4xl">🎯</div>
              <div>
                <h1 className="text-2xl font-bold text-blue-400">UPSC AI Agent</h1>
                <p className="text-xs text-gray-400">Daily curated news for your exam prep</p>
              </div>
            </div>
          </div>
        </div>
      </div>

      <div className="max-w-6xl mx-auto px-6 py-4">
        <div className="flex gap-2 border-b border-slate-700">
          {[
            { id: 'dashboard', label: 'Dashboard', icon: '📊' },
            { id: 'news', label: 'News Feed', icon: '📰' },
            { id: 'resources', label: 'Resources', icon: '📚' },
          ].map((tab) => (
            <button
              key={tab.id}
              onClick={() => setActiveTab(tab.id)}
              className={`px-4 py-3 font-semibold transition flex items-center gap-2 ${
                activeTab === tab.id
                  ? 'text-blue-400 border-b-2 border-blue-400'
                  : 'text-gray-400 hover:text-gray-300'
              }`}
            >
              <span>{tab.icon}</span>
              {tab.label}
            </button>
          ))}
        </div>
      </div>

      <div className="max-w-6xl mx-auto px-6 py-8">
        <div className="bg-slate-800 rounded-xl border border-slate-700 p-6">
          {renderTabContent()}
        </div>
      </div>

      <div className="max-w-6xl mx-auto px-6 py-8 text-center text-gray-500 text-sm">
        <p>🚀 UPSC AI Agent - Your Personal News Curator</p>
      </div>
    </div>
  );
};

export default UPSCAgent;
