# LangChain Context Window Demonstration

This repository contains Python programs that demonstrate the context window problem in Large Language Models (LLMs) and how to handle it using LangChain.

## Files

1. **`langchain_context_window_demo.py`** - Basic demonstration showing:
   - The context window limitation problem
   - How to split large documents using LangChain text splitters
   - Different splitting strategies
   - RAG approach overview

2. **`langchain_context_window_advanced.py`** - Advanced demonstration with:
   - Accurate token counting using tiktoken
   - Real LLM integration (requires API key)
   - Token usage tracking
   - Complete RAG workflow examples

## Installation

1. Install the required dependencies:
```bash
pip install -r requirements.txt
```

Or install individually:
```bash
pip install langchain openai tiktoken
```

2. (Optional) Set your OpenAI API key for the advanced demo:
```bash
export OPENAI_API_KEY='your-api-key-here'
```

## Usage

### Basic Demo (No API Key Required)

Run the basic demonstration:
```bash
python3 langchain_context_window_demo.py
```

This will show:
- Document statistics and token counts
- How documents exceed context windows
- Text splitting strategies
- RAG approach overview

### Advanced Demo (API Key Recommended)

Run the advanced demonstration:
```bash
python3 langchain_context_window_advanced.py
```

This includes:
- Accurate token counting
- Real LLM processing examples (if API key is set)
- Token usage tracking
- Complete RAG workflow code examples

## What is the Context Window Problem?

The context window is the maximum number of tokens (words/subwords) that an LLM can process in a single request. When a document exceeds this limit:

- **Problem**: The model cannot process the entire document at once
- **Consequences**: Requests fail or important information is lost
- **Solution**: Split documents into smaller chunks and process them strategically

### Common Context Window Limits

- GPT-3.5-turbo: 4,096 tokens
- GPT-4: 8,192 tokens
- GPT-4-turbo: 128,000 tokens
- Claude-3: 200,000 tokens

## Solutions Demonstrated

1. **Text Splitting**: Break large documents into smaller chunks
2. **Chunk Overlap**: Maintain context between chunks
3. **Retrieval-Augmented Generation (RAG)**: Store chunks in vector database and retrieve only relevant ones
4. **Token Monitoring**: Track token usage to stay within limits

## Key Concepts

- **Chunk Size**: Size of each document chunk (in characters or tokens)
- **Chunk Overlap**: Overlapping text between chunks to maintain context
- **Token Counting**: Accurately counting tokens before sending to LLM
- **RAG**: Retrieval-Augmented Generation for efficient document processing

## Example Output

The programs will demonstrate:
- Document statistics (characters, words, tokens)
- Comparison with model context window limits
- Text splitting results
- Processing strategies
- Code examples for RAG workflows

## Setting Up GitHub Repository

This repository is ready to be pushed to GitHub. You have several options:

### Option 1: Use the Helper Script (Recommended)

Run the Python helper script:
```bash
python3 create_github_repo.py
```

Or use the bash script:
```bash
./setup_github_repo.sh
```

### Option 2: Use GitHub CLI

If you have GitHub CLI installed:
```bash
gh repo create langchain-context-window-demo --public --description "Demonstration of context window problem in LLMs using LangChain" --source=. --remote=origin --push
```

### Option 3: Manual Setup

1. Go to [GitHub New Repository](https://github.com/new)
2. Repository name: `langchain-context-window-demo`
3. Description: "Demonstration of context window problem in LLMs using LangChain"
4. Choose public/private
5. **Don't** initialize with README (we already have one)
6. Click "Create repository"
7. Then run:
```bash
git remote add origin https://github.com/YOUR_USERNAME/langchain-context-window-demo.git
git branch -M main
git push -u origin main
```

## Notes

- The basic demo works without an API key
- The advanced demo shows code examples even without an API key
- Set `OPENAI_API_KEY` environment variable to run actual LLM calls
- Token counts are estimates; use `tiktoken` for accurate counts

