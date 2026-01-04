import React, { useState } from 'react';
import { Scissors, Layers } from 'lucide-react';

const TextSplitter = () => {
    const [text, setText] = useState(`The context window problem is one of the most significant challenges in working with Large Language Models (LLMs). A context window refers to the maximum number of tokens that a model can process in a single request. When you try to send more tokens than the model's context window allows, the request will fail or the model will truncate the input, potentially losing important information.

Different models have different context window sizes:
- GPT-3.5-turbo: 4,096 tokens
- GPT-4: 8,192 tokens
- GPT-4-turbo: 128,000 tokens
- Claude-3: 200,000 tokens

When working with large documents, you need strategies to handle this limitation:
1. Text Splitting: Break documents into smaller chunks
2. Summarization: Create summaries of chunks and process those
3. Retrieval-Augmented Generation (RAG): Store chunks in a vector database and retrieve only relevant ones for each query
4. Streaming: Process documents in streams rather than all at once`);
    const [chunkSize, setChunkSize] = useState(200);
    const [chunkOverlap, setChunkOverlap] = useState(20);
    const [chunks, setChunks] = useState([]);
    const [loading, setLoading] = useState(false);

    const handleSplit = async () => {
        setLoading(true);
        try {
            const response = await fetch('http://localhost:8000/api/split', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ text, chunk_size: parseInt(chunkSize), chunk_overlap: parseInt(chunkOverlap) }),
            });
            const data = await response.json();
            setChunks(data.chunks);
        } catch (error) {
            console.error('Error splitting text:', error);
        } finally {
            setLoading(false);
        }
    };

    return (
        <div className="card">
            <div className="section-title">
                <Scissors size={24} className="text-primary" />
                <h2>Text Splitter</h2>
            </div>

            <div className="input-group">
                <label>Source Text</label>
                <textarea
                    value={text}
                    onChange={(e) => setText(e.target.value)}
                    rows={6}
                />
            </div>

            <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: '1rem', marginBottom: '1.5rem' }}>
                <div>
                    <label>Chunk Size (chars)</label>
                    <input
                        type="number"
                        value={chunkSize}
                        onChange={(e) => setChunkSize(e.target.value)}
                    />
                </div>
                <div>
                    <label>Chunk Overlap (chars)</label>
                    <input
                        type="number"
                        value={chunkOverlap}
                        onChange={(e) => setChunkOverlap(e.target.value)}
                    />
                </div>
            </div>

            <button className="action-btn" onClick={handleSplit} disabled={loading}>
                {loading ? 'Splitting...' : 'Split Text'}
            </button>

            {chunks.length > 0 && (
                <div style={{ marginTop: '2rem' }}>
                    <div className="section-title">
                        <Layers size={20} />
                        <h3>Resulting Chunks ({chunks.length})</h3>
                    </div>
                    <div className="chunk-viz">
                        {chunks.map((chunk, idx) => (
                            <div key={idx} className="chunk">
                                <div style={{ marginBottom: '0.5rem', opacity: 0.5, fontSize: '0.7em' }}>CHUNK {idx + 1}</div>
                                {chunk}
                            </div>
                        ))}
                    </div>
                </div>
            )}
        </div>
    );
};

export default TextSplitter;
