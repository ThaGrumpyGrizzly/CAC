<<<<<<< HEAD
@echo off
echo 🎨 Investment Tracker Frontend Startup
echo ========================================

REM Check if Node.js is installed
node --version >nul 2>&1
if errorlevel 1 (
    echo ❌ Node.js is not installed or not in PATH
    echo Please install Node.js 16+ from https://nodejs.org
    pause
    exit /b 1
)

REM Check if frontend directory exists
if not exist "frontend" (
    echo ❌ Frontend directory not found
    echo Please run this script from the project root directory
    pause
    exit /b 1
)

REM Change to frontend directory
cd frontend

REM Check if node_modules exists
if not exist "node_modules" (
    echo 📦 Installing dependencies...
    npm install
)

REM Start development server
echo 🚀 Starting Investment Tracker Frontend...
echo 📍 Frontend will be available at: http://localhost:3000
echo 🔗 Backend API should be running at: http://localhost:8000
echo 🛑 Press Ctrl+C to stop the server
echo ----------------------------------------

npm run dev

=======
@echo off
echo 🎨 Investment Tracker Frontend Startup
echo ========================================

REM Check if Node.js is installed
node --version >nul 2>&1
if errorlevel 1 (
    echo ❌ Node.js is not installed or not in PATH
    echo Please install Node.js 16+ from https://nodejs.org
    pause
    exit /b 1
)

REM Check if frontend directory exists
if not exist "frontend" (
    echo ❌ Frontend directory not found
    echo Please run this script from the project root directory
    pause
    exit /b 1
)

REM Change to frontend directory
cd frontend

REM Check if node_modules exists
if not exist "node_modules" (
    echo 📦 Installing dependencies...
    npm install
)

REM Start development server
echo 🚀 Starting Investment Tracker Frontend...
echo 📍 Frontend will be available at: http://localhost:3000
echo 🔗 Backend API should be running at: http://localhost:8000
echo 🛑 Press Ctrl+C to stop the server
echo ----------------------------------------

npm run dev

>>>>>>> 6217901f54d4a616e11e547dcf1f9cf5faa65607
pause 