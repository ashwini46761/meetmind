#!/bin/bash

# MeetMind Streamlit Quick Start Script for macOS/Linux

echo ""
echo "========================================"
echo "   MeetMind - Quick Start Setup"
echo "========================================"
echo ""

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    echo "ERROR: Python 3 is not installed"
    echo "Please install Python 3.9+ from https://www.python.org"
    exit 1
fi

echo "[1/5] Creating virtual environment..."
if [ -d "venv" ]; then
    echo "Virtual environment already exists, skipping..."
else
    python3 -m venv venv
    if [ $? -ne 0 ]; then
        echo "ERROR: Failed to create virtual environment"
        exit 1
    fi
fi

echo "[2/5] Activating virtual environment..."
source venv/bin/activate
if [ $? -ne 0 ]; then
    echo "ERROR: Failed to activate virtual environment"
    exit 1
fi

echo "[3/5] Installing dependencies..."
pip install --upgrade pip setuptools wheel > /dev/null 2>&1
pip install -r requirements.txt
if [ $? -ne 0 ]; then
    echo "ERROR: Failed to install dependencies"
    echo "Try running: pip install -r requirements.txt"
    exit 1
fi

echo "[4/5] Checking configuration..."
if [ ! -f ".env" ]; then
    echo ""
    echo "WARNING: .env file not found!"
    echo "Creating .env from template..."
    cp .env.example .env
    echo ""
    echo "Please edit .env and add your API keys:"
    echo "  - ANTHROPIC_API_KEY"
    echo "  - TWILIO_ACCOUNT_SID"
    echo "  - TWILIO_AUTH_TOKEN"
    echo "  - TWILIO_FROM_NUMBER"
    echo ""
    read -p "Press Enter to continue..."
fi

echo "[5/5] Starting Streamlit app..."
echo ""
echo "App will open in your browser at: http://localhost:8501"
echo "Press Ctrl+C to stop the server"
echo ""
sleep 2

streamlit run src/meetmind/app.py

