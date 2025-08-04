@echo off
echo 🎯 Investment Tracker Backend Startup
echo ========================================

REM Check if Python is installed
py --version >nul 2>&1
if errorlevel 1 (
    echo ❌ Python is not installed or not in PATH
    echo Please install Python 3.8+ from https://python.org
    pause
    exit /b 1
)

REM Check if backend directory exists
if not exist "backend" (
    echo ❌ Backend directory not found
    echo Please run this script from the project root directory
    pause
    exit /b 1
)

REM Change to backend directory
cd backend

REM Check if virtual environment exists
if not exist "venv" (
    echo 📝 Creating virtual environment...
    py -m venv venv
)

REM Activate virtual environment
echo 🔧 Activating virtual environment...
call venv\Scripts\activate.bat

REM Install dependencies
echo 📦 Installing dependencies...
pip install -r requirements.txt

REM Initialize database
echo 🗄️ Initializing database...
py database.py

REM Start server
echo 🚀 Starting Investment Tracker API server...
echo 📍 API will be available at: http://localhost:8000
echo 📖 API documentation at: http://localhost:8000/docs
echo 🛑 Press Ctrl+C to stop the server
echo ----------------------------------------

uvicorn app:app --host 0.0.0.0 --port 8000 --reload

pause 