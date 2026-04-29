@echo off
REM MeetMind Streamlit Quick Start Script for Windows

echo.
echo ========================================
echo   MeetMind - Quick Start Setup
echo ========================================
echo.

REM Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Python is not installed or not in PATH
    echo Please install Python 3.9+ from https://www.python.org
    pause
    exit /b 1
)

echo [1/5] Creating virtual environment...
if exist venv (
    echo Virtual environment already exists, skipping...
) else (
    python -m venv venv
    if errorlevel 1 (
        echo ERROR: Failed to create virtual environment
        pause
        exit /b 1
    )
)

echo [2/5] Activating virtual environment...
call venv\Scripts\activate.bat
if errorlevel 1 (
    echo ERROR: Failed to activate virtual environment
    pause
    exit /b 1
)

echo [3/5] Installing dependencies...
pip install --upgrade pip setuptools wheel >nul 2>&1
pip install -r requirements.txt
if errorlevel 1 (
    echo ERROR: Failed to install dependencies
    echo Try running: pip install -r requirements.txt
    pause
    exit /b 1
)

echo [4/5] Checking configuration...
if not exist .env (
    echo.
    echo WARNING: .env file not found!
    echo Creating .env from template...
    copy .env.example .env >nul
    echo.
    echo Please edit .env and add your API keys:
    echo   - ANTHROPIC_API_KEY
    echo   - TWILIO_ACCOUNT_SID
    echo   - TWILIO_AUTH_TOKEN
    echo   - TWILIO_FROM_NUMBER
    echo.
    pause
)

echo [5/5] Starting Streamlit app...
echo.
echo App will open in your browser at: http://localhost:8501
echo Press Ctrl+C to stop the server
echo.
timeout /t 2

streamlit run src\meetmind\app.py

pause
