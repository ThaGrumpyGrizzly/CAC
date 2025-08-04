# 🚀 Investment Tracker - Windows Setup Guide

## Prerequisites ✅
- ✅ Python 3.13.5 (using `py` command)
- ✅ Node.js v22.14.0
- ✅ Windows PowerShell

## Quick Start (Windows)

### Option 1: Using Batch Files (Recommended)

1. **Start the Backend:**
   ```cmd
   start_backend.bat
   ```
   This will:
   - Create a virtual environment
   - Install Python dependencies
   - Initialize the database
   - Start the API server

2. **Start the Frontend (in a new terminal):**
   ```cmd
   start_frontend.bat
   ```
   This will:
   - Install Node.js dependencies
   - Start the development server

### Option 2: Manual Setup

#### Backend Setup
```cmd
cd backend
py -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
py database.py
py app.py
```

#### Frontend Setup
```cmd
cd frontend
npm install
npm run dev
```

## Access the Application

- **Frontend:** http://localhost:3000
- **Backend API:** http://localhost:8000
- **API Documentation:** http://localhost:8000/docs

## Test the Setup

Run the test script to verify everything is working:
```cmd
py test_backend.py
```

## Troubleshooting

### Python Command Issues
- Use `py` instead of `python` on Windows
- If `py` doesn't work, try `python3`

### Port Already in Use
- Backend: Change port in `backend/app.py` or kill process on port 8000
- Frontend: Change port in `frontend/vite.config.js` or kill process on port 3000

### Database Issues
- The app uses SQLite by default (no setup required)
- For PostgreSQL, edit `.env` file with your database URL

## Features to Try

1. **Add an Investment:**
   - Go to "Add Investment"
   - Try ticker: `AAPL` (Apple), `MSFT` (Microsoft), `ASML.AS` (ASML Amsterdam)

2. **View Portfolio:**
   - Dashboard shows all investments
   - Real-time prices from Yahoo Finance
   - Profit/loss calculations

3. **API Testing:**
   - Visit http://localhost:8000/docs for interactive API documentation
   - Test endpoints directly in the browser

## Development

### Backend Development
```cmd
cd backend
venv\Scripts\activate
py -m uvicorn app:app --reload --host 0.0.0.0 --port 8000
```

### Frontend Development
```cmd
cd frontend
npm run dev
```

## File Structure
```
Coffee/
├── backend/           # FastAPI backend
├── frontend/          # React frontend
├── start_backend.bat  # Windows backend starter
├── start_frontend.bat # Windows frontend starter
├── test_backend.py    # API test script
└── README.md         # Full documentation
``` 