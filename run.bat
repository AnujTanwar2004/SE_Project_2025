@echo off
REM Run script for Screen Capture Detection System

title Screen Capture Detection System

echo ========================================
echo Screen Capture Detection System
echo Starting application...
echo ========================================
echo.

REM Check if Python is installed
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ERROR: Python is not installed or not in PATH
    echo Please run install.bat first
    pause
    exit /b 1
)

REM Run the application
python main.py

if %errorlevel% neq 0 (
    echo.
    echo ERROR: Application crashed or encountered an error
    echo Check the logs folder for details
    pause
)
