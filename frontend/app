import React, { useState, useEffect } from 'react';
import { ChevronDown, AlertCircle, BookOpen, Trophy, Radio, Zap, Search, Settings, RefreshCw, Filter } from 'lucide-react';

const UPSCAgent = () => {
  const [activeTab, setActiveTab] = useState('dashboard');
  const [selectedCategory, setSelectedCategory] = useState('all');
  const [newsData, setNewsData] = useState(null);
  const [loading, setLoading] = useState(false);
  const [expandedCard, setExpandedCard] = useState(null);
  const [filterType, setFilterType] = useState('all');
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
        summary: 'Cabinet reshuffle with 5 new ministers appointed across key portfolios including defense and finance.',
        content: 'The Prime Minister announced a major cabinet reshuffle today with the appointment of 5 new ministers. This is significant for Prelims as it tests knowledge of constitutional articles, ministerial qualifications, and cabinet hierarchy. Key articles: Article 75-78.',
      },
      {
        id: 2,
        title: 'RBI Announces New Monetary Policy',
        topic: 'Economics',
        source: 'RBI',
        date: '2025-05-14',
        relevance: 'high',
        summary: 'RBI maintains repo rate at 6.5% amid inflation concerns. New guidelines for digital banking.',
        content: 'The Reserve Bank of India announced its latest monetary policy stance. Key concepts: Repo rate, CRR, SLR, functions of RBI. Important for understanding economic policy frameworks.',
      },
      {
        id: 3,
        title: 'New Species of Endangered Tiger Found',
        topic: 'Environment',
        source: 'The Hindu',
        date: '2025-05-13',
        relevance: 'medium',
        summary: 'Researchers discover new subspecies in Western Ghats. Conservation efforts discussed.',
        content: 'A new tiger subspecies has been identified in the Western Ghats region. Relevant topics: Biodiversity hotspots, CITES, Wildlife Protection Act.',
      },
    ],
    mains: [
      {
        id: 4,
        title: 'Federal Structure and Centre-State Relations',
        topic: 'Government & Politics',
        source: 'The Hindu',
        date: '2025-05-15',
        relevance: 'high',
        summary: 'Analysis of recent Supreme Court judgment on GST distribution between Centre and States.',
        content: 'A comprehensive analysis of the federal structure in India and how recent GST judgment impacts centre-state relations. Relevant for Mains: Articles 246, 248, 249. Deep dive into concurrent list issues and fiscal federalism.',
        essay: 'Analyze the evolution of Centre-State relations in post-independent India with particular focus on fiscal arrangements and dispute resolution mechanisms.',
      },
      {
        id: 5,
        title: 'Environmental Justice and Development',
        topic: 'Environment & Social Issues',
        source: 'Indian Express',
        date: '2025-05-14',
        relevance: 'high',
        summary: 'Case study on balancing environmental protection with developmental needs in India.',
        content: 'Detailed analysis of environmental justice framework in India. Discusses Bhopal gas tragedy, Silent Valley project, and modern-day conflicts between development and environment preservation.',
        essay: 'Discuss the concept of environmental justice in the Indian context. How can we balance environmental protection with the developmental aspirations of India?',
      },
    ],
    interview: [
      {
        id: 6,
        title: 'How to Prepare for UPSC Interview on Current Affairs',
        topic: 'Interview Strategy',
        source: 'UPSC Analysis',
        date: '2025-05-15',
        relevance: 'high',
        summary: 'Tips on linking recent events to philosophical and governance frameworks.',
        content: 'Interview boards often ask candidates to relate current affairs to governance principles. Key strategies: Prepare 50-100 significant recent events with their implications for governance, public administration, and ethics.',
        questions: [
          'Recent RBI monetary policy - implications for financial inclusion?',
          'Cabinet reshuffle - what does it suggest about government priorities?',
          'Tiger conservation success - how does it reflect on India\'s environmental policy?',
        ],
      },
      {
        id: 7,
        title: 'Ethical Decision Making in Administration',
        topic: 'Ethics & Values',
        source: 'Interview Expert',
        date: '2025-05-14',
        relevance: 'high',
        summary: 'Real case studies for ethical dilemmas faced by administrators.',
        content: 'Collection of real-world ethical dilemmas. Helpful for interview preparation where boards assess your values and decision-making framework.',
        casestudies: [
          'Conflict between environmental protection and tribal rights',
          'Transparency vs national security concerns',
          'Equity vs efficiency in resource allocation',
        ],
      },
    ],
    'current-affairs': [
      {
        id: 8,
        title: 'Weekly Current Affairs Summary (May 9-15, 2025)',
        topic: 'Weekly Summary',
        source: 'Multiple Sources',
        date: '2025-05-15',
        relevance: 'high',
        summary: 'Comprehensive weekly summary of all major national and international events.',
        sections: {
          National: [
            'Cabinet reshuffle announced',
            'RBI monetary policy review',
            'New education policy implementation begins',
          ],
          International: [
            'UN Climate Summit in Vienna',
            'Trade negotiations between major economies',
            'Regional security developments in Asia',
          ],
          Sports: [
            'India wins cricket tournament',
            'Olympic qualification criteria released',
          ],
        },
      },
      {
        id: 9,
        title: 'PIB: Government Schemes Updates',
        topic: 'Government Initiatives',
        source: 'PIB',
        date: '2025-05-15',
        relevance: 'high',
        summary: 'Updates on major government schemes implementation status.',
        schemes: [
          { name: 'PM Gati Shakti', status: 'Infrastructure projects accelerating' },
          { name: 'Digital India', status: 'Rural broadband expansion ongoing' },
          { name: 'Swachh Bharat', status: '90% villages achieved ODF status' },
        ],
      },
    ],
  };

  const fetchNews = async () => {
    setLoading(true);
    // Simulate API call
    setTimeout(() => {
      setNewsData(mockNewsData);
      setLastUpdated(new Date());
      setLoading(false);
    }, 1500);
  };

  useEffect(() => {
    fetchNews();
  }, []);

  const getNewsForCategory = () => {
    if (selectedCategory === 'all') {
      return Object.values(mockNewsData).flat();
    }
    return mockNewsData[selectedCategory] || [];
  };

  const filteredNews = getNewsForCategory().filter((item) => {
    if (filterType === 'high') return item.relevance === 'high';
    if (filterType === 'medium') return item.relevance === 'medium';
    return true;
  });

  const renderTabContent = () => {
    if (activeTab === 'dashboard') {
      return (
        <div className="space-y-8">
          {/* Stats */}
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

          {/* Last Updated & Refresh */}
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

          {/* Quick Links to Sources */}
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
          {/* Category Filter */}
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

          {/* Relevance Filter */}
          <div className="flex gap-2">
            <Filter size={18} className="text-gray-600" />
            <button
              onClick={() => setFilterType('all')}
              className={`px-3 py-1 text-sm rounded ${
                filterType === 'all' ? 'bg-gray-800 text-white' : 'bg-gray-100'
              }`}
            >
              All Relevance
            </button>
            <button
              onClick={() => setFilterType('high')}
              className={`px-3 py-1 text-sm rounded ${
                filterType === 'high' ? 'bg-red-500 text-white' : 'bg-gray-100'
              }`}
            >
              ⭐ High Relevance Only
            </button>
          </div>

          {/* News Items */}
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

                      {item.essay && (
                        <div className="bg-white p-3 rounded border-l-4 border-purple-500">
                          <p className="text-xs font-semibold text-purple-700 mb-1">📝 ESSAY TOPIC</p>
                          <p className="text-sm text-gray-700">{item.essay}</p>
                        </div>
                      )}

                      {item.questions && (
                        <div className="bg-white p-3 rounded border-l-4 border-orange-500">
                          <p className="text-xs font-semibold text-orange-700 mb-2">🎤 INTERVIEW QUESTIONS</p>
                          <ul className="space-y-2">
                            {item.questions.map((q, i) => (
                              <li key={i} className="text-sm text-gray-700">• {q}</li>
                            ))}
                          </ul>
                        </div>
                      )}

                      {item.sections && (
                        <div className="bg-white p-3 rounded border-l-4 border-green-500">
                          <p className="text-xs font-semibold text-green-700 mb-2">📰 HIGHLIGHTS</p>
                          {Object.entries(item.sections).map(([section, items]) => (
                            <div key={section} className="mb-2">
                              <p className="text-xs font-semibold text-gray-600">{section}</p>
                              <ul className="ml-2 space-y-1">
                                {items.map((it, i) => (
                                  <li key={i} className="text-sm text-gray-700">• {it}</li>
                                ))}
                              </ul>
                            </div>
                          ))}
                        </div>
                      )}

                      {item.schemes && (
                        <div className="bg-white p-3 rounded border-l-4 border-blue-500">
                          <p className="text-xs font-semibold text-blue-700 mb-2">💼 SCHEMES</p>
                          <ul className="space-y-2">
                            {item.schemes.map((s, i) => (
                              <li key={i} className="text-sm text-gray-700">
                                <strong>{s.name}</strong>: {s.status}
                              </li>
                            ))}
                          </ul>
                        </div>
                      )}
                    </div>
                  )}
                </div>
              ))
            )}
          </div>
        </div>
      );
    }

    if (activeTab === 'resources') {
      return (
        <div className="space-y-6">
          <div className="bg-gradient-to-br from-blue-50 to-indigo-50 border border-blue-200 rounded-lg p-6">
            <h3 className="text-lg font-bold text-gray-800 mb-4">Study Strategy</h3>
            <div className="space-y-3">
              <div className="flex gap-3">
                <span className="text-2xl">📋</span>
                <div>
                  <p className="font-semibold">Prelims Strategy</p>
                  <p className="text-sm text-gray-600">Focus on factual accuracy. Use this agent to track all government appointments, economic data, and policy changes. Mock tests on related topics weekly.</p>
                </div>
              </div>
              <div className="flex gap-3">
                <span className="text-2xl">📚</span>
                <div>
                  <p className="font-semibold">Mains Strategy</p>
                  <p className="text-sm text-gray-600">Develop strong conceptual understanding. Link current affairs to governance frameworks. Practice essays connecting today's news to constitutional principles.</p>
                </div>
              </div>
              <div className="flex gap-3">
                <span className="text-2xl">🎤</span>
                <div>
                  <p className="font-semibold">Interview Strategy</p>
                  <p className="text-sm text-gray-600">Build a portfolio of recent events with their governance implications. Develop ethical frameworks for decision-making. Practice linking current affairs to administrative values.</p>
                </div>
              </div>
            </div>
          </div>

          <div className="bg-gradient-to-br from-green-50 to-emerald-50 border border-green-200 rounded-lg p-6">
            <h3 className="text-lg font-bold text-gray-800 mb-4">Official Sources to Follow</h3>
            <div className="space-y-2 text-sm">
              <p>🏛️ <strong>Government Sources</strong></p>
              <ul className="ml-6 space-y-1 text-gray-700">
                <li>• PIB (Press Information Bureau) - Government announcements</li>
                <li>• Ministry websites - Specific policy updates</li>
                <li>• PRS India - Legislative tracking</li>
                <li>• RBI/Finance Ministry - Economic data</li>
              </ul>
              <p className="mt-4">📰 <strong>Newspapers (Editorial & Analysis)</strong></p>
              <ul className="ml-6 space-y-1 text-gray-700">
                <li>• The Hindu - Quality analysis and editorials</li>
                <li>• Indian Express - In-depth reporting</li>
                <li>• Business Standard - Economics & policy</li>
                <li>• Livemint - Current affairs with governance angle</li>
              </ul>
            </div>
          </div>

          <div className="bg-gradient-to-br from-purple-50 to-pink-50 border border-purple-200 rounded-lg p-6">
            <h3 className="text-lg font-bold text-gray-800 mb-4">Daily Routine (30 mins)</h3>
            <ol className="space-y-2 text-sm text-gray-700">
              <li><strong>10 mins:</strong> Check this agent for high-relevance updates</li>
              <li><strong>10 mins:</strong> Read PIB and ministry websites directly</li>
              <li><strong>10 mins:</strong> Read newspaper editorials (The Hindu, Indian Express)</li>
              <li><strong>Daily:</strong> Link each news item to UPSC exam syllabus topics</li>
            </ol>
          </div>
        </div>
      );
    }
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-slate-900 via-slate-800 to-slate-900">
      <style>{`
        @import url('https://fonts.googleapis.com/css2?family=Outfit:wght@400;600;700;800&family=Playfair+Display:wght@700&display=swap');
        
        body {
          font-family: 'Outfit', sans-serif;
        }
        
        .hero-title {
          font-family: 'Playfair Display', serif;
          background: linear-gradient(135deg, #60a5fa 0%, #a78bfa 100%);
          -webkit-background-clip: text;
          -webkit-text-fill-color: transparent;
          background-clip: text;
        }
      `}</style>

      {/* Header */}
      <div className="bg-gradient-to-r from-slate-800 to-slate-900 border-b border-slate-700 sticky top-0 z-50">
        <div className="max-w-6xl mx-auto px-6 py-4">
          <div className="flex items-center justify-between">
            <div className="flex items-center gap-3">
              <div className="text-4xl">🎯</div>
              <div>
                <h1 className="hero-title text-2xl font-bold">UPSC AI Agent</h1>
                <p className="text-xs text-gray-400">Daily curated news for your exam prep</p>
              </div>
            </div>
            <button className="p-2 hover:bg-slate-700 rounded-lg transition">
              <Settings size={20} className="text-gray-400" />
            </button>
          </div>
        </div>
      </div>

      {/* Navigation */}
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

      {/* Main Content */}
      <div className="max-w-6xl mx-auto px-6 py-8">
        <div className="bg-slate-800 rounded-xl border border-slate-700 p-6">
          {renderTabContent()}
        </div>
      </div>

      {/* Footer */}
      <div className="max-w-6xl mx-auto px-6 py-8 text-center text-gray-500 text-sm">
        <p>🚀 This agent helps you prepare for UPSC by organizing news by exam stage. Always verify information from official sources.</p>
      </div>
    </div>
  );
};

export default UPSCAgent;
