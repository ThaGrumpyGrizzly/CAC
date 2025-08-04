from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from models import Investment, Purchase, UpdatePurchase
from services.finance_api import get_current_price, search_stocks, get_stock_suggestions
from services.analytics import calculate_profit
from services.investment_aggregator import (
    get_all_investment_summaries, 
    get_investment_summary, 
    add_purchase, 
    delete_purchase,
    update_purchase,
    migrate_old_investments
)
from database import get_db, InvestmentDB
from sqlalchemy.orm import Session
from fastapi import Depends
from typing import List

app = FastAPI(title="Investment Tracker API", version="1.0.0")

# Add CORS middleware for frontend communication
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000", 
        "http://localhost:5173",
        "https://*.vercel.app",  # Allow Vercel deployments
        "https://*.railway.app",  # Allow Railway deployments
        "https://*.netlify.app",  # Allow Netlify deployments
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def read_root():
    return {"status": "Investment Tracker API running", "version": "1.0.0"}

@app.get("/health")
def health_check():
    return {"status": "healthy", "service": "Investment Tracker API"}

@app.post("/investment")
def add_investment(investment: Investment, db: Session = Depends(get_db)):
    try:
        current_price = get_current_price(investment.ticker)
        profit = calculate_profit(investment, current_price)
        
        # Save to database
        db_investment = InvestmentDB(
            ticker=investment.ticker,
            amount=investment.amount,
            price_per_share=investment.price_per_share,
            date=investment.date,
            costs=investment.costs
        )
        db.add(db_investment)
        db.commit()
        db.refresh(db_investment)
        
        return {
            "id": db_investment.id,
            "ticker": investment.ticker,
            "current_price": current_price,
            "profit": profit,
            "total_value": investment.amount * current_price
        }
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.get("/investments", response_model=List[dict])
def get_investments(db: Session = Depends(get_db)):
    investments = db.query(InvestmentDB).all()
    result = []
    
    for inv in investments:
        try:
            current_price = get_current_price(inv.ticker)
            profit = calculate_profit(inv, current_price)
            result.append({
                "id": inv.id,
                "ticker": inv.ticker,
                "amount": inv.amount,
                "price_per_share": inv.price_per_share,
                "date": inv.date,
                "costs": inv.costs,
                "current_price": current_price,
                "profit": profit,
                "total_value": inv.amount * current_price
            })
        except Exception as e:
            # If we can't get current price, still return the investment with error
            result.append({
                "id": inv.id,
                "ticker": inv.ticker,
                "amount": inv.amount,
                "price_per_share": inv.price_per_share,
                "date": inv.date,
                "costs": inv.costs,
                "current_price": None,
                "profit": None,
                "total_value": None,
                "error": str(e)
            })
    
    return result

@app.delete("/investment/{investment_id}")
def delete_investment(investment_id: str, db: Session = Depends(get_db)):
    investment = db.query(InvestmentDB).filter(InvestmentDB.id == investment_id).first()
    if not investment:
        raise HTTPException(status_code=404, detail="Investment not found")
    
    db.delete(investment)
    db.commit()
    return {"message": "Investment deleted successfully"}

# New endpoints for the purchase system
@app.post("/purchase")
def add_purchase_endpoint(purchase: Purchase):
    """Add a new purchase (can be for existing or new stock)"""
    try:
        result = add_purchase(purchase.dict())
        return result
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.get("/investments/summary")
def get_investments_summary():
    """Get aggregated summary of all investments"""
    try:
        summaries = get_all_investment_summaries()
        return summaries
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.get("/investment/{ticker}/summary")
def get_investment_summary_endpoint(ticker: str):
    """Get detailed summary for a specific ticker including all purchases"""
    try:
        summary = get_investment_summary(ticker)
        if not summary:
            raise HTTPException(status_code=404, detail=f"No investments found for {ticker}")
        return summary
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.delete("/purchase/{purchase_id}")
def delete_purchase_endpoint(purchase_id: str):
    """Delete a specific purchase"""
    try:
        success = delete_purchase(purchase_id)
        if not success:
            raise HTTPException(status_code=404, detail="Purchase not found")
        return {"message": "Purchase deleted successfully"}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.put("/purchase/{purchase_id}")
def update_purchase_endpoint(purchase_id: str, purchase_data: UpdatePurchase):
    """Update a specific purchase"""
    try:
        result = update_purchase(purchase_id, purchase_data.dict())
        if not result:
            raise HTTPException(status_code=404, detail="Purchase not found")
        return result
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.post("/migrate")
def migrate_endpoint():
    """Migrate old investments to the new purchase system"""
    try:
        result = migrate_old_investments()
        return result
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.get("/search")
def search_investments(query: str):
    """Search for stocks and ETFs by name or ticker"""
    try:
        results = search_stocks(query)
        return {"results": results}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.get("/suggestions")
def get_suggestions(query: str):
    """Get stock ticker suggestions"""
    try:
        suggestions = get_stock_suggestions(query)
        return {"suggestions": suggestions}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000) 