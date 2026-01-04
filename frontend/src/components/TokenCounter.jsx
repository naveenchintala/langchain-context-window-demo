// Author: Naveen Chintala
import React, { useState, useEffect } from 'react';
import { Calculator, CheckCircle, AlertTriangle } from 'lucide-react';

const TokenCounter = () => {
    const [text, setText] = useState('The context window problem is one of the most significant challenges in working with Large Language Models (LLMs).');
    const [stats, setStats] = useState({ count: 0, compatible_models: [] });
    const [loading, setLoading] = useState(false);

    useEffect(() => {
        const fetchTokens = async () => {
            setLoading(true);
            try {
                const response = await fetch('http://localhost:8000/api/tokenize', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({ text, model: 'gpt-3.5-turbo' }),
                });
                const data = await response.json();
                setStats(data);
            } catch (error) {
                console.error('Error fetching token count:', error);
            } finally {
                setLoading(false);
            }
        };

        const debounce = setTimeout(fetchTokens, 500);
        return () => clearTimeout(debounce);
    }, [text]);

    return (
        <div className="card">
            <div className="section-title">
                <Calculator size={24} className="text-primary" />
                <h2>Token Counter</h2>
            </div>

            <div className="input-group">
                <label>Input Text</label>
                <textarea
                    value={text}
                    onChange={(e) => setText(e.target.value)}
                    rows={6}
                    placeholder="Type or paste text here to count tokens..."
                />
            </div>

            <div className="stats-grid">
                <div className="stat-item">
                    <div className="stat-value">{text.length.toLocaleString()}</div>
                    <div className="stat-label">Characters</div>
                </div>
                <div className="stat-item">
                    <div className="stat-value">{text.split(/\s+/).filter(w => w.length > 0).length.toLocaleString()}</div>
                    <div className="stat-label">Words</div>
                </div>
                <div className="stat-item">
                    <div className="stat-value" style={{ color: stats.count > 4096 ? 'var(--error)' : 'var(--primary)' }}>
                        {stats.count.toLocaleString()}
                    </div>
                    <div className="stat-label">Estimated Tokens</div>
                </div>
            </div>

            <div style={{ marginTop: '2rem' }}>
                <label>Model Compatibility</label>
                <div className="chunk-viz">
                    {['gpt-3.5-turbo', 'gpt-4', 'gpt-4-turbo', 'claude-3-opus'].map(model => {
                        const isCompatible = stats.compatible_models.includes(model);
                        return (
                            <div key={model} className={`model-pill ${isCompatible ? 'compatible' : 'incompatible'}`}>
                                {isCompatible ? <CheckCircle size={14} /> : <AlertTriangle size={14} />}
                                <span style={{ marginLeft: '0.5rem' }}>{model}</span>
                            </div>
                        );
                    })}
                </div>
            </div>
        </div>
    );
};

export default TokenCounter;
