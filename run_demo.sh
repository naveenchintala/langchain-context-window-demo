#!/bin/bash

# Setup environment
echo "Setting up Python environment..."
python3 -m venv .venv
source .venv/bin/activate

# Install dependencies
echo "Installing dependencies..."
pip install -r requirements.txt

# Run server
echo "Starting server at http://localhost:8000"
echo "Press Ctrl+C to stop"
python3 server.py
