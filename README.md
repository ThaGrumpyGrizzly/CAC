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
- 🔐 **Authentication** - Secure login with JWT tokens
- 👑 **Admin Dashboard** - Stock analytics and user management

## Tech Stack

### Backend
- **FastAPI** - Modern Python web framework
- **SQLAlchemy** - Database ORM
- **SQLite** - Local database for development
- **Yahoo Finance API** - Real-time stock data
- **JWT** - Authentication tokens

### Frontend
- **React 18** - Modern React with hooks
- **Tailwind CSS** - Utility-first CSS framework
- **Vite** - Fast build tool
- **Axios** - HTTP client
- **React Router** - Client-side routing
- **Firebase** - Authentication and hosting
- **Supabase** - Database and backend services

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

2. **Install dependencies:**
   ```bash
   pip install fastapi uvicorn requests pydantic sqlalchemy python-dotenv python-multipart passlib python-jose PyJWT
   ```

3. **Start the backend server:**
   ```bash
   py start.py
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
   
   The frontend will be available at `http://localhost:5173`

## API Documentation

Once the backend is running, visit `http://localhost:8000/docs` for interactive API documentation.

## Admin Access

To access the admin dashboard:
1. Log in to your account
2. Click "Make Me Admin" button on the admin page
3. Refresh the page to see admin features

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Submit a pull request

## License

This project is licensed under the MIT License. 