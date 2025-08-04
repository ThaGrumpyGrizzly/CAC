@echo off
echo 🚀 Starting Investment Tracker Application
echo ==========================================

echo.
echo 📋 Instructions:
echo 1. This will start the backend server
echo 2. Open a new PowerShell window and run: cd frontend && npm run dev
echo 3. Open your browser to: http://localhost:3000
echo.

echo 🔧 Starting Backend Server...
cd backend
call venv\Scripts\activate.bat
echo ✅ Backend environment activated
echo 🚀 Starting API server on http://localhost:8000
echo.
echo 📖 API Documentation: http://localhost:8000/docs
echo 🛑 Press Ctrl+C to stop the backend server
echo.

py app.py

pause 