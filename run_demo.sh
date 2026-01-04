#!/bin/bash

# Setup environment
echo "Setting up Python environment..."
python3 -m venv .venv
source .venv/bin/activate

# Install dependencies
echo "Installing dependencies..."
pip install -r requirements.txt

# Check for .env file
if [ ! -f .env ]; then
    echo ""
    echo "⚠️  No .env file found!"
    echo "   Creating one from .env.example..."
    cp .env.example .env
    echo "   Please edit .env and add your OPENAI_API_KEY to use real LLM features."
    echo ""
fi

# Run server
echo "Starting server at http://localhost:8000"
echo "Press Ctrl+C to stop"
python3 server.py
