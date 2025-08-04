# Investment Tracker

A modern web application for tracking your investment portfolio with real-time stock prices and profit/loss calculations.

## Features

- 📊 **Portfolio Dashboard** - Overview of all investments with current values
- 💰 **Real-time Prices** - Live stock prices from Yahoo Finance API
- 📈 **Profit/Loss Tracking** - Automatic calculation of gains and losses
- ➕ **Add Investments** - Easy form to add new positions
- 🗑️ **Delete Investments** - Remove positions from your portfolio
- 📱 **Responsive Design** - Works on desktop and mobile devices
- 🎨 **Modern UI** - Clean interface built with React and Tailwind CSS

## Tech Stack

### Backend
- **FastAPI** - Modern Python web framework
- **SQLAlchemy** - Database ORM
- **PostgreSQL/SQLite** - Database options
- **Yahoo Finance API** - Real-time stock data

### Frontend
- **React 18** - Modern React with hooks
- **Tailwind CSS** - Utility-first CSS framework
- **Vite** - Fast build tool
- **Axios** - HTTP client
- **React Router** - Client-side routing

## Quick Start

### Prerequisites
- Python 3.8+
- Node.js 16+
- npm or yarn

### Backend Setup

1. **Navigate to backend directory:**
   ```bash
   cd backend
   ```

2. **Create virtual environment:**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Set up environment variables:**
   ```bash
   cp ../env.example .env
   # Edit .env file with your database settings
   ```

5. **Initialize database:**
   ```bash
   python database.py
   ```

6. **Start the backend server:**
   ```bash
   python app.py
   ```
   
   The API will be available at `http://localhost:8000`

### Frontend Setup

1. **Navigate to frontend directory:**
   ```bash
   cd frontend
   ```

2. **Install dependencies:**
   ```bash
   npm install
   ```

3. **Start the development server:**
   ```bash
   npm run dev
   ```
   
   The frontend will be available at `http://localhost:3000`

## Database Configuration

### Option 1: SQLite (Development)
Set `USE_SQLITE=true` in your `.env` file. This creates a local SQLite database file.

### Option 2: PostgreSQL (Production)
1. Install PostgreSQL
2. Create a database
3. Set database connection string in `.env` file

## API Documentation

Once the backend is running, visit `http://localhost:8000/docs` for interactive API documentation.

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Submit a pull request

## License

This project is licensed under the MIT License. 