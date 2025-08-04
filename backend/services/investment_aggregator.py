from typing import Dict, List, Optional
from database import SessionLocal, PurchaseDB, InvestmentDB
from services.finance_api import get_current_price
from services.currency_converter import detect_currency_from_ticker
from services.analytics import calculate_profit, calculate_profit_percentage

def get_investment_summary(ticker: str) -> Optional[Dict]:
    """
    Get aggregated summary for a specific ticker
    """
    db = SessionLocal()
    try:
        # Get all purchases for this ticker
        purchases = db.query(PurchaseDB).filter(PurchaseDB.ticker == ticker).all()
        
        if not purchases:
            return None
        
        # Calculate aggregated metrics
        total_amount = sum(p.amount for p in purchases)
        total_cost_amount = sum(p.amount * p.price_per_share for p in purchases)
        total_costs = sum(p.costs for p in purchases)
        
        # Calculate average price
        average_price = total_cost_amount / total_amount if total_amount > 0 else 0
        
        # Get current price
        try:
            current_price_data = get_current_price(ticker)
            current_price = current_price_data[0]  # Converted price in EUR
            original_price = current_price_data[1]  # Original price
            original_currency = current_price_data[2]  # Original currency
            
            # Validate that current_price is not NaN
            if current_price is not None and (current_price != current_price or current_price <= 0):
                current_price = None
                print(f"Warning: Invalid current price for {ticker}: {current_price_data[0]}")
        except:
            current_price = None
            original_price = None
            original_currency = detect_currency_from_ticker(ticker)
        
        # Calculate current value and profit
        total_value = None
        total_profit = None
        profit_percentage = None
        
        if current_price is not None and current_price > 0:
            total_value = total_amount * current_price
            total_cost = total_cost_amount + total_costs
            total_profit = total_value - total_cost
            profit_percentage = ((total_value - total_cost) / total_cost * 100) if total_cost > 0 else 0
            
            # Validate that we don't have NaN values
            if total_value is not None and (total_value != total_value or total_value < 0):
                total_value = None
            if total_profit is not None and (total_profit != total_profit):
                total_profit = None
            if profit_percentage is not None and (profit_percentage != profit_percentage):
                profit_percentage = None
        
        # Format purchases for response
        purchase_list = []
        for purchase in purchases:
            purchase_list.append({
                'id': purchase.id,
                'ticker': purchase.ticker,
                'amount': purchase.amount,
                'price_per_share': purchase.price_per_share,
                'date': purchase.date,
                'costs': purchase.costs,
                'created_at': purchase.created_at.isoformat()
            })
        
        return {
            'ticker': ticker,
            'total_amount': round(total_amount, 2),
            'average_price': round(average_price, 2),
            'total_costs': round(total_costs, 2),
            'current_price': current_price,
            'original_price': original_price,
            'total_value': round(total_value, 2) if total_value else None,
            'total_profit': round(total_profit, 2) if total_profit else None,
            'profit_percentage': round(profit_percentage, 2) if profit_percentage else None,
            'original_currency': original_currency,
            'purchases': purchase_list
        }
        
    finally:
        db.close()

def get_all_investment_summaries() -> List[Dict]:
    """
    Get aggregated summaries for all tickers
    """
    db = SessionLocal()
    try:
        # Get all unique tickers
        tickers = db.query(PurchaseDB.ticker).distinct().all()
        ticker_list = [t[0] for t in tickers]
        
        summaries = []
        for ticker in ticker_list:
            summary = get_investment_summary(ticker)
            if summary:
                summaries.append(summary)
        
        return summaries
        
    finally:
        db.close()

def add_purchase(purchase_data: Dict) -> Dict:
    """
    Add a new purchase to the database
    """
    db = SessionLocal()
    try:
        # Create new purchase
        purchase = PurchaseDB(
            ticker=purchase_data['ticker'],
            amount=purchase_data['amount'],
            price_per_share=purchase_data['price_per_share'],
            date=purchase_data['date'],
            costs=purchase_data['costs']
        )
        
        db.add(purchase)
        db.commit()
        db.refresh(purchase)
        
        return {
            'id': purchase.id,
            'ticker': purchase.ticker,
            'amount': purchase.amount,
            'price_per_share': purchase.price_per_share,
            'date': purchase.date,
            'costs': purchase.costs,
            'created_at': purchase.created_at.isoformat()
        }
        
    finally:
        db.close()

def delete_purchase(purchase_id: str) -> bool:
    """
    Delete a specific purchase
    """
    db = SessionLocal()
    try:
        purchase = db.query(PurchaseDB).filter(PurchaseDB.id == purchase_id).first()
        if purchase:
            db.delete(purchase)
            db.commit()
            return True
        return False
        
    finally:
        db.close()

def update_purchase(purchase_id: str, purchase_data: Dict) -> Optional[Dict]:
    """
    Update a specific purchase
    """
    db = SessionLocal()
    try:
        purchase = db.query(PurchaseDB).filter(PurchaseDB.id == purchase_id).first()
        if not purchase:
            return None
        
        # Update the purchase fields
        purchase.amount = purchase_data['amount']
        purchase.price_per_share = purchase_data['price_per_share']
        purchase.date = purchase_data['date']
        purchase.costs = purchase_data['costs']
        
        db.commit()
        db.refresh(purchase)
        
        return {
            'id': purchase.id,
            'ticker': purchase.ticker,
            'amount': purchase.amount,
            'price_per_share': purchase.price_per_share,
            'date': purchase.date,
            'costs': purchase.costs,
            'created_at': purchase.created_at.isoformat()
        }
        
    finally:
        db.close()

def migrate_old_investments():
    """
    Migrate old investment records to the new purchase system
    """
    db = SessionLocal()
    try:
        # Check if there are old investments to migrate
        old_investments = db.query(InvestmentDB).all()
        
        if not old_investments:
            return {"message": "No old investments to migrate"}
        
        migrated_count = 0
        for old_inv in old_investments:
            # Check if we already have purchases for this ticker
            existing_purchases = db.query(PurchaseDB).filter(PurchaseDB.ticker == old_inv.ticker).count()
            
            if existing_purchases == 0:
                # Create purchase from old investment
                purchase = PurchaseDB(
                    ticker=old_inv.ticker,
                    amount=old_inv.amount,
                    price_per_share=old_inv.price_per_share,
                    date=old_inv.date,
                    costs=old_inv.costs
                )
                db.add(purchase)
                migrated_count += 1
        
        db.commit()
        return {"message": f"Migrated {migrated_count} old investments to purchases"}
        
    finally:
        db.close() 