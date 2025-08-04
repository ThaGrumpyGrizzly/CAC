<<<<<<< HEAD
🧩 Projectstructuur
bash
Kopiëren
Bewerken
investment-tracker/
├── backend/
│   ├── app.py               # API met FastAPI of Flask
│   ├── models.py            # Datamodellen (User, Investment, etc.)
│   ├── database.py          # Connectie met DB (PostgreSQL)
│   └── services/
│       ├── finance_api.py   # Yahoo Finance of Finnhub integratie
│       └── analytics.py     # Berekeningen winst/verlies, highs/lows
│
├── frontend/
│   ├── public/
│   ├── src/
│   │   ├── components/
│   │   ├── pages/
│   │   ├── App.jsx
│   │   └── main.jsx
│   └── package.json         # React + Tailwind
│
├── .env
├── README.md
└── requirements.txt         # Python dependencies
⚙️ Backend (FastAPI)
app.py

python
Kopiëren
Bewerken
from fastapi import FastAPI
from models import Investment
from services.finance_api import get_current_price
from services.analytics import calculate_profit

app = FastAPI()

@app.get("/")
def read_root():
    return {"status": "Investment Tracker API running"}

@app.post("/investment")
def add_investment(investment: Investment):
    current_price = get_current_price(investment.ticker)
    profit = calculate_profit(investment, current_price)
    return {"current_price": current_price, "profit": profit}
models.py

python
Kopiëren
Bewerken
from pydantic import BaseModel

class Investment(BaseModel):
    ticker: str
    amount: float
    price_per_share: float
    date: str
    costs: float
services/finance_api.py

python
Kopiëren
Bewerken
import requests

def get_current_price(ticker: str) -> float:
    url = f"https://query1.finance.yahoo.com/v7/finance/quote?symbols={ticker}"
    response = requests.get(url)
    data = response.json()
    return data['quoteResponse']['result'][0]['regularMarketPrice']
services/analytics.py

python
Kopiëren
Bewerken
def calculate_profit(investment, current_price):
    total_cost = investment.amount * investment.price_per_share + investment.costs
    current_value = investment.amount * current_price
    return round(current_value - total_cost, 2)
requirements.txt

nginx
Kopiëren
Bewerken
fastapi
uvicorn
requests
pydantic
🎨 Frontend (React + Tailwind)
src/pages/Dashboard.jsx

jsx
Kopiëren
Bewerken
import { useEffect, useState } from 'react';
import axios from 'axios';

function Dashboard() {
  const [investments, setInvestments] = useState([]);
  
  const fetchInvestments = async () => {
    // Dummy data for now, in praktijk haal je uit backend of DB
    const response = await axios.post('/investment', {
      ticker: "ASML.AS",
      amount: 10,
      price_per_share: 750,
      date: "2024-06-01",
      costs: 5
    });
    setInvestments([response.data]);
  };

  useEffect(() => {
    fetchInvestments();
  }, []);

  return (
    <div className="p-4">
      <h1 className="text-2xl font-bold">Dashboard</h1>
      {investments.map((inv, i) => (
        <div key={i}>
          <p>Huidige prijs: €{inv.current_price}</p>
          <p>Winst/verlies: €{inv.profit}</p>
        </div>
      ))}
    </div>
  );
}

export default Dashboard;
package.json (Fragment)

json
Kopiëren
Bewerken
{
  "dependencies": {
    "axios": "^1.5.0",
    "react": "^18.2.0",
    "tailwindcss": "^3.3.0"
  }
}
🧠 Suggestie voor AI Prompts in Cursor
Zodra je deze structuur hebt, kun je Cursor AI vragen:

text
Kopiëren
Bewerken
"Help me uitbreiden zodat ik meerdere investeringen tegelijk kan toevoegen en opslaan in een database zoals PostgreSQL."
text
Kopiëren
Bewerken
"Genereer grafieken voor koersverloop en winst/verlies met Chart.js of Recharts."
text
Kopiëren
Bewerken
"Voeg automatische koersupdates toe elke dag om 9:00 met een achtergrondtaak."
🗂️ Optioneel: Database (PostgreSQL via database.py)
python
Kopiëren
Bewerken
from sqlalchemy import create_engine, Column, Float, String
from sqlalchemy.orm import declarative_base

Base = declarative_base()
engine = create_engine("postgresql://user:password@localhost/investment_db")

class Investment(Base):
    __tablename__ = "investments"
    id = Column(String, primary_key=True)
    ticker = Column(String)
    amount = Column(Float)
    price_per_share = Column(Float)
=======
🧩 Projectstructuur
bash
Kopiëren
Bewerken
investment-tracker/
├── backend/
│   ├── app.py               # API met FastAPI of Flask
│   ├── models.py            # Datamodellen (User, Investment, etc.)
│   ├── database.py          # Connectie met DB (PostgreSQL)
│   └── services/
│       ├── finance_api.py   # Yahoo Finance of Finnhub integratie
│       └── analytics.py     # Berekeningen winst/verlies, highs/lows
│
├── frontend/
│   ├── public/
│   ├── src/
│   │   ├── components/
│   │   ├── pages/
│   │   ├── App.jsx
│   │   └── main.jsx
│   └── package.json         # React + Tailwind
│
├── .env
├── README.md
└── requirements.txt         # Python dependencies
⚙️ Backend (FastAPI)
app.py

python
Kopiëren
Bewerken
from fastapi import FastAPI
from models import Investment
from services.finance_api import get_current_price
from services.analytics import calculate_profit

app = FastAPI()

@app.get("/")
def read_root():
    return {"status": "Investment Tracker API running"}

@app.post("/investment")
def add_investment(investment: Investment):
    current_price = get_current_price(investment.ticker)
    profit = calculate_profit(investment, current_price)
    return {"current_price": current_price, "profit": profit}
models.py

python
Kopiëren
Bewerken
from pydantic import BaseModel

class Investment(BaseModel):
    ticker: str
    amount: float
    price_per_share: float
    date: str
    costs: float
services/finance_api.py

python
Kopiëren
Bewerken
import requests

def get_current_price(ticker: str) -> float:
    url = f"https://query1.finance.yahoo.com/v7/finance/quote?symbols={ticker}"
    response = requests.get(url)
    data = response.json()
    return data['quoteResponse']['result'][0]['regularMarketPrice']
services/analytics.py

python
Kopiëren
Bewerken
def calculate_profit(investment, current_price):
    total_cost = investment.amount * investment.price_per_share + investment.costs
    current_value = investment.amount * current_price
    return round(current_value - total_cost, 2)
requirements.txt

nginx
Kopiëren
Bewerken
fastapi
uvicorn
requests
pydantic
🎨 Frontend (React + Tailwind)
src/pages/Dashboard.jsx

jsx
Kopiëren
Bewerken
import { useEffect, useState } from 'react';
import axios from 'axios';

function Dashboard() {
  const [investments, setInvestments] = useState([]);
  
  const fetchInvestments = async () => {
    // Dummy data for now, in praktijk haal je uit backend of DB
    const response = await axios.post('/investment', {
      ticker: "ASML.AS",
      amount: 10,
      price_per_share: 750,
      date: "2024-06-01",
      costs: 5
    });
    setInvestments([response.data]);
  };

  useEffect(() => {
    fetchInvestments();
  }, []);

  return (
    <div className="p-4">
      <h1 className="text-2xl font-bold">Dashboard</h1>
      {investments.map((inv, i) => (
        <div key={i}>
          <p>Huidige prijs: €{inv.current_price}</p>
          <p>Winst/verlies: €{inv.profit}</p>
        </div>
      ))}
    </div>
  );
}

export default Dashboard;
package.json (Fragment)

json
Kopiëren
Bewerken
{
  "dependencies": {
    "axios": "^1.5.0",
    "react": "^18.2.0",
    "tailwindcss": "^3.3.0"
  }
}
🧠 Suggestie voor AI Prompts in Cursor
Zodra je deze structuur hebt, kun je Cursor AI vragen:

text
Kopiëren
Bewerken
"Help me uitbreiden zodat ik meerdere investeringen tegelijk kan toevoegen en opslaan in een database zoals PostgreSQL."
text
Kopiëren
Bewerken
"Genereer grafieken voor koersverloop en winst/verlies met Chart.js of Recharts."
text
Kopiëren
Bewerken
"Voeg automatische koersupdates toe elke dag om 9:00 met een achtergrondtaak."
🗂️ Optioneel: Database (PostgreSQL via database.py)
python
Kopiëren
Bewerken
from sqlalchemy import create_engine, Column, Float, String
from sqlalchemy.orm import declarative_base

Base = declarative_base()
engine = create_engine("postgresql://user:password@localhost/investment_db")

class Investment(Base):
    __tablename__ = "investments"
    id = Column(String, primary_key=True)
    ticker = Column(String)
    amount = Column(Float)
    price_per_share = Column(Float)
>>>>>>> 6217901f54d4a616e11e547dcf1f9cf5faa65607
    costs = Column(Float)