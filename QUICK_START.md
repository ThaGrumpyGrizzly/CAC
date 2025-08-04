# 🚀 Investment Tracker - Quick Start Guide

## ✅ **Fixed Issues**
- **API Errors Fixed**: Multiple data sources now available
- **Search Functionality**: Search by name, ticker, or ETF name
- **Better Error Handling**: Fallback to mock data if APIs fail
- **No API Keys Required**: Works out of the box

## 🎯 **New Features**

### **Smart Search**
- Search by company name: "Apple", "Microsoft", "KBC"
- Search by ticker: "AAPL", "MSFT", "KBC.BR"
- Search by ETF name: "AMUNDI BEL 20", "iShares MSCI"
- Auto-complete suggestions
- Shows Stock vs ETF labels

### **Supported Stocks & ETFs**
- **US Stocks**: AAPL, MSFT, GOOGL, AMZN, TSLA, META, NVDA
- **European Stocks**: ASML.AS, SAP.DE, LVMH.PA, KBC.BR, INGA.AS
- **Belgian Stocks**: KBC.BR, ABI.BR, UCB.BR, SOLB.BR, PROX.BR
- **ETFs**: SPY, QQQ, VTI, VWRL.L, IWDA.L, AMUNDI BEL 20 UCITS ETF DIST

## 🚀 **Quick Start**

### **Option 1: Simple Batch File**
```cmd
start_app.bat
```
Then open a new PowerShell window:
```cmd
cd frontend
npm run dev
```

### **Option 2: Manual Start**

**Backend (PowerShell Window 1):**
```powershell
cd C:\GPCODING\Coffee\backend
venv\Scripts\activate
py app.py
```

**Frontend (PowerShell Window 2):**
```powershell
cd C:\GPCODING\Coffee\frontend
npm run dev
```

## 🌐 **Access Your App**
- **Main App**: http://localhost:3000
- **API Docs**: http://localhost:8000/docs

## 🔍 **How to Use Search**

### **Search Examples:**
1. **By Company Name**: Type "Apple" → Select "AAPL - Apple Inc."
2. **By Ticker**: Type "MSFT" → Select "MSFT - Microsoft Corporation"
3. **By ETF Name**: Type "AMUNDI BEL" → Select "AMUNDI BEL 20 UCITS ETF DIST"
4. **By Belgian Stock**: Type "KBC" → Select "KBC.BR - KBC Group NV"

### **Search Tips:**
- Start typing any part of the name or ticker
- Results show Stock/ETF labels
- Click on any result to select it
- Clear button (X) to reset search

## 🎯 **Try These Examples**

### **Popular Stocks:**
- "Apple" → AAPL
- "Microsoft" → MSFT
- "Tesla" → TSLA
- "ASML" → ASML.AS

### **Belgian Stocks:**
- "KBC" → KBC.BR
- "AB InBev" → ABI.BR
- "UCB" → UCB.BR
- "BIRG" → BIRG.BR

### **ETFs:**
- "AMUNDI BEL" → AMUNDI BEL 20 UCITS ETF DIST
- "iShares MSCI" → IWDA.L
- "Vanguard FTSE" → VWRL.L
- "SP500" → SPY

## 🔧 **Troubleshooting**

### **If Search Doesn't Work:**
- Make sure backend is running on http://localhost:8000
- Check browser console for errors
- Try refreshing the page

### **If Prices Show Mock Data:**
- This is normal when external APIs are unavailable
- Mock prices are generated for demo purposes
- Real prices will work when APIs are accessible

### **If Backend Won't Start:**
```powershell
cd backend
venv\Scripts\activate
pip install -r requirements.txt
py app.py
```

## 📱 **Features Available**
- ✅ Smart search by name/ticker
- ✅ Real-time price fetching (with fallback)
- ✅ Portfolio overview
- ✅ Profit/loss calculations
- ✅ Add/delete investments
- ✅ Responsive design
- ✅ No API keys required

## 🎉 **You're Ready!**
Your investment tracker now has:
- **Smart search** for easy stock/ETF finding
- **Multiple data sources** for reliable prices
- **Beautiful UI** with autocomplete
- **No setup required** - just run and use!

Start adding your investments and track your portfolio! 🚀 