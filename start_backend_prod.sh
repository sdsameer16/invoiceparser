#!/bin/bash
# Backend startup script for production (Linux/Mac)
# This runs on Render servers

echo "Installing dependencies..."
pip install -r requirements.txt

echo "Starting backend server..."
# Production mode - this is what Render runs
uvicorn backend.app:app --host 0.0.0.0 --port $PORT
