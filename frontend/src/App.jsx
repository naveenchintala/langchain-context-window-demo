import React, { useState } from 'react';
import TokenCounter from './components/TokenCounter';
import TextSplitter from './components/TextSplitter';
import ProcessingDemo from './components/ProcessingDemo';
import { Layout } from 'lucide-react';

function App() {
  const [activeTab, setActiveTab] = useState('count');

  return (
    <div>
      <header>
        <h1>Context Window <span style={{ color: 'var(--primary)' }}>Demo</span></h1>
        <p className="subtitle">Advanced visualization of LLM context limits and chunking strategies</p>
      </header>

      <div className="tabs">
        <button
          className={`tab-btn ${activeTab === 'count' ? 'active' : ''}`}
          onClick={() => setActiveTab('count')}
        >
          Token Counting
        </button>
        <button
          className={`tab-btn ${activeTab === 'split' ? 'active' : ''}`}
          onClick={() => setActiveTab('split')}
        >
          Text Splitting
        </button>
        <button
          className={`tab-btn ${activeTab === 'process' ? 'active' : ''}`}
          onClick={() => setActiveTab('process')}
        >
          LLM Processing
        </button>
      </div>

      <main>
        {activeTab === 'count' && <TokenCounter />}
        {activeTab === 'split' && <TextSplitter />}
        {activeTab === 'process' && <ProcessingDemo />}
      </main>

      <footer style={{ textAlign: 'center', marginTop: '4rem', color: 'var(--text-muted)', fontSize: '0.9rem' }}>
        <p>Built with LangChain & FastAPI • <a href="#" style={{ color: 'var(--primary)' }}>View Source</a></p>
      </footer>
    </div>
  );
}

export default App;
