@echo off
REM Installation script for Screen Capture Detection System

echo ========================================
echo Screen Capture Detection System
echo Installation Script
echo ========================================
echo.

REM Check if Python is installed
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ERROR: Python is not installed or not in PATH
    echo Please install Python 3.8 or higher from https://www.python.org/
    pause
    exit /b 1
)

echo Python detected: 
python --version
echo.

REM Install required packages
echo Installing required packages...
echo.
pip install -r requirements.txt

if %errorlevel% neq 0 (
    echo.
    echo ERROR: Failed to install packages
    echo Please check your internet connection and try again
    pause
    exit /b 1
)

echo.
echo ========================================
echo Installation completed successfully!
echo ========================================
echo.
echo To run the application:
echo   python main.py
echo.
echo Or simply double-click run.bat
echo.
pause
