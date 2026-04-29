#!/usr/bin/env python3
"""
MeetMind application launcher.
"""
import sys
from pathlib import Path

# Add the src directory to the Python path
ROOT_DIR = Path(__file__).resolve().parent
if str(ROOT_DIR) not in sys.path:
    sys.path.insert(0, str(ROOT_DIR))

# Import and run the Streamlit app
from meetmind.app import main

if __name__ == "__main__":
    main()