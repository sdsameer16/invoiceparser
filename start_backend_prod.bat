@echo off
REM Backend startup script for Windows
REM This is what Render will run in production

echo Installing dependencies...
pip install -r requirements.txt

echo Starting backend server...
REM For local development with auto-reload
REM uvicorn backend.app:app --reload

REM For production
uvicorn backend.app:app --host 0.0.0.0 --port 8000
