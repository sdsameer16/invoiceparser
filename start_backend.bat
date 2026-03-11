@echo off
echo ======================================
echo    AI Invoice Data Extractor v2.0
echo      Powered by Gemini AI
echo ======================================
echo.

echo Checking Python installation...
python --version
if errorlevel 1 (
    echo Error: Python is not installed or not in PATH
    echo Please install Python 3.8+ from https://python.org
    pause
    exit /b 1
)

echo.
echo Checking required packages...
pip show fastapi uvicorn pdfplumber google-generativeai > nul 2>&1
if errorlevel 1 (
    echo Installing required packages (including Gemini AI)...
    pip install -r requirements.txt
    if errorlevel 1 (
        echo Error installing packages. Please check your internet connection.
        pause
        exit /b 1
    )
)

echo.
echo ======================================
echo     GEMINI AI SETUP (IMPORTANT!)
echo ======================================
echo.
echo To enable AI-powered extraction:
echo 1. Visit: https://makersuite.google.com/app/apikey
echo 2. Generate a Gemini API key
echo 3. Edit .env file and set: GEMINI_API_KEY=your_key_here
echo 4. Restart this server
echo.
echo Current Status: 
if exist .env (
    findstr /C:"GEMINI_API_KEY=your_gemini_api_key_here" .env > nul
    if errorlevel 1 (
        echo   🤖 Gemini API: Configured
    ) else (
        echo   ⚠️  Gemini API: Not configured - will use traditional parsing
    )
) else (
    echo   ⚠️  Gemini API: Not configured - will use traditional parsing
)
echo.
echo ======================================
echo.

echo Starting FastAPI server...
echo Server will be available at: http://127.0.0.1:8000
echo Frontend should be opened at: frontend/index.html
echo.
echo Supported formats: PDF, Word, Excel, Images (PNG, JPG, etc.)
echo.
echo Press Ctrl+C to stop the server
echo ======================================
echo.

cd backend
uvicorn app:app --reload --host 127.0.0.1 --port 8000