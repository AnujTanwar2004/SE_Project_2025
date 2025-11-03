"""
Unauthorized Screen Capture Detection System for Windows
Detects malicious/unauthorized screen captures while allowing normal user screenshots
Main Entry Point
"""

import sys
import os
from pathlib import Path

# Add project root to path
sys.path.insert(0, str(Path(__file__).parent))

from gui.main_window import ScreenCaptureDetectorApp
from core.detector import ScreenCaptureDetector
from utils.logger import setup_logging

def main():
    """Main entry point for the application"""
    # Setup logging
    setup_logging()
    
    # Initialize and run the GUI application
    app = ScreenCaptureDetectorApp()
    app.run()

if __name__ == "__main__":
    main()
