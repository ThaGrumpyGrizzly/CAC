from database import SessionLocal, UserDB, PurchaseDB
from sqlalchemy import func, desc
from typing import List, Dict, Optional
from datetime import datetime, timedelta

# Try to import stock price service, fallback if not available
try:
    from .stock_price_service import stock_price_service
    STOCK_PRICE_AVAILABLE = True
except ImportError:
    STOCK_PRICE_AVAILABLE = False
    stock_price_service = None

def get_all_users() -> List[Dict]:
    """Get all users with their basic info"""
    db = SessionLocal()
    try:
        users = db.query(UserDB).all()
        return [
            {
                'id': user.id,
                'email': user.email,
                'username': user.username,
                'is_admin': user.is_admin == 'true',
                'created_at': user.created_at,
                'purchase_count': len(user.purchases)
            }
            for user in users
        ]
    finally:
        db.close()

def get_user_details(user_id: str) -> Optional[Dict]:
    """Get detailed user information including all purchases"""
    db = SessionLocal()
    try:
        user = db.query(UserDB).filter(UserDB.id == user_id).first()
        if not user:
            return None
        
        return {
            'id': user.id,
            'email': user.email,
            'username': user.username,
            'is_admin': user.is_admin == 'true',
            'created_at': user.created_at,
            'purchases': [
                {
                    'id': purchase.id,
                    'ticker': purchase.ticker,
                    'amount': purchase.amount,
                    'price_per_share': purchase.price_per_share,
                    'date': purchase.date,
                    'costs': purchase.costs,
                    'created_at': purchase.created_at
                }
                for purchase in user.purchases
            ]
        }
    finally:
        db.close()

def get_top_investments(limit: int = 10) -> List[Dict]:
    """Get top investments across all users"""
    db = SessionLocal()
    try:
        # Get total amount invested per ticker across all users
        top_investments = db.query(
            PurchaseDB.ticker,
            func.sum(PurchaseDB.amount).label('total_shares'),
            func.avg(PurchaseDB.price_per_share).label('avg_price'),
            func.sum(PurchaseDB.costs).label('total_costs'),
            func.count(PurchaseDB.id).label('purchase_count')
        ).group_by(PurchaseDB.ticker).order_by(desc(func.sum(PurchaseDB.costs))).limit(limit).all()
        
        return [
            {
                'ticker': investment.ticker,
                'total_shares': float(investment.total_shares),
                'avg_price': float(investment.avg_price),
                'total_costs': float(investment.total_costs),
                'purchase_count': investment.purchase_count
            }
            for investment in top_investments
        ]
    finally:
        db.close()

def get_user_statistics() -> Dict:
    """Get overall user statistics"""
    db = SessionLocal()
    try:
        total_users = db.query(UserDB).count()
        admin_users = db.query(UserDB).filter(UserDB.is_admin == 'true').count()
        total_purchases = db.query(PurchaseDB).count()
        total_invested = db.query(func.sum(PurchaseDB.costs)).scalar() or 0
        
        # Users with purchases
        users_with_purchases = db.query(func.count(func.distinct(PurchaseDB.user_id))).scalar() or 0
        
        # Recent activity (last 7 days)
        week_ago = datetime.utcnow() - timedelta(days=7)
        recent_purchases = db.query(PurchaseDB).filter(PurchaseDB.created_at >= week_ago).count()
        recent_users = db.query(UserDB).filter(UserDB.created_at >= week_ago).count()
        
        return {
            'total_users': total_users,
            'admin_users': admin_users,
            'regular_users': total_users - admin_users,
            'total_purchases': total_purchases,
            'total_invested': float(total_invested),
            'users_with_purchases': users_with_purchases,
            'recent_purchases': recent_purchases,
            'recent_users': recent_users
        }
    finally:
        db.close()

def make_user_admin(user_id: str) -> bool:
    """Make a user an admin"""
    db = SessionLocal()
    try:
        user = db.query(UserDB).filter(UserDB.id == user_id).first()
        if user:
            user.is_admin = 'true'
            db.commit()
            return True
        return False
    finally:
        db.close()

def remove_admin_status(user_id: str) -> bool:
    """Remove admin status from a user"""
    db = SessionLocal()
    try:
        user = db.query(UserDB).filter(UserDB.id == user_id).first()
        if user:
            user.is_admin = 'false'
            db.commit()
            return True
        return False
    finally:
        db.close()

def delete_user(user_id: str) -> bool:
    """Delete a user and all their purchases"""
    db = SessionLocal()
    try:
        user = db.query(UserDB).filter(UserDB.id == user_id).first()
        if user:
            # Delete all purchases first (due to foreign key constraint)
            db.query(PurchaseDB).filter(PurchaseDB.user_id == user_id).delete()
            # Delete the user
            db.delete(user)
            db.commit()
            return True
        return False
    finally:
        db.close()

def get_popular_tickers() -> List[Dict]:
    """Get most popular tickers by number of users investing in them"""
    db = SessionLocal()
    try:
        popular_tickers = db.query(
            PurchaseDB.ticker,
            func.count(func.distinct(PurchaseDB.user_id)).label('user_count'),
            func.sum(PurchaseDB.amount).label('total_shares'),
            func.sum(PurchaseDB.costs).label('total_costs')
        ).group_by(PurchaseDB.ticker).order_by(desc(func.count(func.distinct(PurchaseDB.user_id)))).limit(10).all()
        
        return [
            {
                'ticker': ticker.ticker,
                'user_count': ticker.user_count,
                'total_shares': float(ticker.total_shares),
                'total_costs': float(ticker.total_costs)
            }
            for ticker in popular_tickers
        ]
    finally:
        db.close()

def get_stock_analytics() -> Dict:
    """Get stock analytics with user counts, average buy prices, and current prices"""
    db = SessionLocal()
    try:
        # Get aggregated data per ticker
        stock_data = db.query(
            PurchaseDB.ticker,
            func.count(func.distinct(PurchaseDB.user_id)).label('user_count'),
            func.sum(PurchaseDB.amount).label('total_shares'),
            func.avg(PurchaseDB.price_per_share).label('avg_buy_price'),
            func.sum(PurchaseDB.costs).label('total_costs'),
            func.count(PurchaseDB.id).label('purchase_count')
        ).group_by(PurchaseDB.ticker).order_by(desc(func.count(func.distinct(PurchaseDB.user_id)))).all()
        
        # Get total unique users
        total_unique_users = db.query(func.count(func.distinct(PurchaseDB.user_id))).scalar() or 0
        
        # Get current prices for all tickers
        tickers = [stock.ticker for stock in stock_data]
        current_prices = {}
        
        print(f"🔍 Debug: Stock price service available: {STOCK_PRICE_AVAILABLE}")
        print(f"🔍 Debug: Stock price service object: {stock_price_service}")
        print(f"🔍 Debug: Tickers to fetch: {tickers}")
        
        if STOCK_PRICE_AVAILABLE and stock_price_service:
            try:
                print(f"🔍 Debug: Attempting to fetch stock prices...")
                current_prices = stock_price_service.get_batch_stock_prices(tickers)
                print(f"🔍 Debug: Fetched prices: {current_prices}")
            except Exception as e:
                print(f"❌ Error fetching stock prices: {e}")
                current_prices = {}
        else:
            print(f"❌ Stock price service not available")
        
        # For now, we'll return the data without current prices
        # Current prices would need to be fetched from an external API
        return {
            'stock_analytics': [
                {
                    'ticker': stock.ticker,
                    'user_count': stock.user_count,
                    'total_shares': float(stock.total_shares),
                    'avg_buy_price': float(stock.avg_buy_price),
                    'total_costs': float(stock.total_costs),
                    'purchase_count': stock.purchase_count,
                    'current_price': current_prices.get(stock.ticker)  # Real current price
                }
                for stock in stock_data
            ],
            'total_unique_users': total_unique_users
        }
    finally:
        db.close() 