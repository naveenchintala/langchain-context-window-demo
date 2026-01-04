// Author: Naveen Chintala
import React, { useState } from 'react';
import { Cpu, Play, Loader2 } from 'lucide-react';

const ProcessingDemo = () => {
    const [apiKey, setApiKey] = useState('');
    const [status, setStatus] = useState('idle'); // idle, processing, complete
    const [output, setOutput] = useState(null);

    const handleProcess = async () => {
        setStatus('processing');
        try {
            // Simulate processing for demo since actual LLM calls are expensive/slow
            await new Promise(resolve => setTimeout(resolve, 2000));

            const response = await fetch('http://localhost:8000/api/process', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ text: "Demo text", api_key: apiKey }),
            });
            const data = await response.json();
            setOutput(data);
            setStatus('complete');
        } catch (error) {
            console.error(error);
            setStatus('idle');
        }
    };

    return (
        <div className="card">
            <div className="section-title">
                <Cpu size={24} className="text-primary" />
                <h2>LLM Processing Demo</h2>
            </div>

            <div className="input-group">
                <label>OpenAI API Key (Optional for Demo)</label>
                <input
                    type="password"
                    value={apiKey}
                    onChange={e => setApiKey(e.target.value)}
                    placeholder="sk-..."
                />
            </div>

            <button className="action-btn" onClick={handleProcess} disabled={status === 'processing'}>
                {status === 'processing' ? (
                    <span style={{ display: 'flex', alignItems: 'center', justifyContent: 'center', gap: '0.5rem' }}>
                        <Loader2 className="animate-spin" size={20} /> Processing...
                    </span>
                ) : (
                    <span style={{ display: 'flex', alignItems: 'center', justifyContent: 'center', gap: '0.5rem' }}>
                        <Play size={20} /> Start Processing
                    </span>
                )}
            </button>

            {output && (
                <div style={{ marginTop: '2rem', padding: '1rem', background: 'rgba(255,255,255,0.05)', borderRadius: '8px' }}>
                    <h3 style={{ marginBottom: '1rem' }}>Output</h3>
                    <p>{output.summary}</p>
                </div>
            )}
        </div>
    );
};

export default ProcessingDemo;
