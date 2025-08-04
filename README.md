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
3. Set `DATABASE_URL` in your `.env` file:
   ```
   DATABASE_URL=postgresql://username:password@localhost/database_name
   ```

## API Endpoints

- `GET /` - API status
- `GET /investments` - Get all investments
- `POST /investment` - Add new investment
- `DELETE /investment/{id}` - Delete investment

## Usage

1. **Add Investments:**
   - Click "Add Investment" in the navigation
   - Enter stock ticker (e.g., AAPL, ASML.AS, MSFT)
   - Fill in purchase details (shares, price, date, costs)
   - Submit to add to your portfolio

2. **View Portfolio:**
   - Dashboard shows overview of all investments
   - Each investment card displays current value and profit/loss
   - Portfolio summary shows total metrics

3. **Manage Investments:**
   - Delete investments using the trash icon
   - Refresh prices using the refresh button

## Stock Ticker Examples

- **US Stocks:** AAPL, MSFT, GOOGL, TSLA
- **European Stocks:** ASML.AS (Amsterdam), SAP.DE (Frankfurt), LVMH.PA (Paris)
- **Other:** Add exchange suffix for international stocks

## Development

### Backend Development
```bash
cd backend
uvicorn app:app --reload --host 0.0.0.0 --port 8000
```

### Frontend Development
```bash
cd frontend
npm run dev
```

### Building for Production
```bash
# Frontend
cd frontend
npm run build

# Backend
cd backend
pip install -r requirements.txt
python app.py
```

## Project Structure

```
investment-tracker/
├── backend/
│   ├── app.py               # FastAPI application
│   ├── models.py            # Pydantic models
│   ├── database.py          # Database configuration
│   ├── requirements.txt     # Python dependencies
│   └── services/
│       ├── finance_api.py   # Yahoo Finance integration
│       └── analytics.py     # Profit/loss calculations
├── frontend/
│   ├── src/
│   │   ├── components/      # Reusable components
│   │   ├── pages/          # Page components
│   │   ├── context/        # React context
│   │   ├── App.jsx         # Main app component
│   │   └── main.jsx        # Entry point
│   ├── package.json        # Node dependencies
│   └── vite.config.js      # Vite configuration
├── env.example             # Environment variables template
└── README.md              # This file
```

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## License

This project is open source and available under the [MIT License](LICENSE).

## Support

For issues and questions, please open an issue on GitHub. 