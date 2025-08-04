from fastapi import FastAPI, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from models import Investment, Purchase, UpdatePurchase, UserCreate, UserLogin, UserResponse, Token
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
from services.auth import (
    get_password_hash, authenticate_user, create_access_token, 
    get_current_user, get_user_by_email, get_user_by_username
)
from database import get_db, InvestmentDB, UserDB
from sqlalchemy.orm import Session
from typing import List, Dict
from datetime import timedelta

app = FastAPI(title='Investment Tracker API', version='1.0.0')

# Add security
security = HTTPBearer()

# Add CORS middleware for frontend communication
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        'http://localhost:3000', 
        'http://localhost:5173',
        'https://*.vercel.app',  # Allow Vercel deployments
        'https://*.railway.app',  # Allow Railway deployments
        'https://*.netlify.app',  # Allow Netlify deployments
        'https://cac-o513w0fc6-mr-grumpys-projects.vercel.app',  # Your specific Vercel domain
        '*',  # Allow all origins for development (remove in production)
    ],
    allow_credentials=True,
    allow_methods=['*'],
    allow_headers=['*'],
)

@app.get('/')
def read_root():
    return {'status': 'Investment Tracker API running', 'version': '1.0.0'}

@app.get('/health')
def health_check():
    try:
        # Test database connection
        from database import SessionLocal
        from sqlalchemy import text
        db = SessionLocal()
        db.execute(text('SELECT 1'))
        db.close()
        return {'status': 'healthy', 'service': 'Investment Tracker API', 'database': 'connected'}
    except Exception as e:
        return {'status': 'unhealthy', 'service': 'Investment Tracker API', 'database': 'error', 'error': str(e)}

# Authentication endpoints
@app.post('/register', response_model=UserResponse)
def register_user(user: UserCreate, db: Session = Depends(get_db)):
    # Check if user already exists
    if get_user_by_email(db, user.email):
        raise HTTPException(status_code=400, detail='Email already registered')
    if get_user_by_username(db, user.username):
        raise HTTPException(status_code=400, detail='Username already taken')
    
    # Create new user
    hashed_password = get_password_hash(user.password)
    db_user = UserDB(
        email=user.email,
        username=user.username,
        hashed_password=hashed_password
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    
    return UserResponse(
        id=db_user.id,
        email=db_user.email,
        username=db_user.username,
        created_at=db_user.created_at
    )

@app.post('/login', response_model=Token)
def login_user(user_credentials: UserLogin, db: Session = Depends(get_db)):
    user = authenticate_user(db, user_credentials.email, user_credentials.password)
    if not user:
        raise HTTPException(status_code=401, detail='Incorrect email or password')
    
    access_token = create_access_token(
        data={'sub': user.email},
        expires_delta=timedelta(minutes=30)
    )
    return {'access_token': access_token, 'token_type': 'bearer'}

# Protected endpoints
@app.post('/investment')
def add_investment(investment: Investment, credentials: HTTPAuthorizationCredentials = Depends(security), db: Session = Depends(get_db)):
    user = get_current_user(credentials.credentials)
    if not user:
        raise HTTPException(status_code=401, detail='Invalid token')
    
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
            'id': db_investment.id,
            'ticker': investment.ticker,
            'current_price': current_price,
            'profit': profit,
            'total_value': investment.amount * current_price
        }
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.get('/investments', response_model=List[dict])
def get_investments(credentials: HTTPAuthorizationCredentials = Depends(security), db: Session = Depends(get_db)):
    user = get_current_user(credentials.credentials)
    if not user:
        raise HTTPException(status_code=401, detail='Invalid token')
    
    investments = db.query(InvestmentDB).all()
    result = []
    
    for inv in investments:
        try:
            current_price = get_current_price(inv.ticker)
            profit = calculate_profit(inv, current_price)
            result.append({
                'id': inv.id,
                'ticker': inv.ticker,
                'amount': inv.amount,
                'price_per_share': inv.price_per_share,
                'date': inv.date,
                'costs': inv.costs,
                'current_price': current_price,
                'profit': profit,
                'total_value': inv.amount * current_price
            })
        except Exception as e:
            result.append({
                'id': inv.id,
                'ticker': inv.ticker,
                'amount': inv.amount,
                'price_per_share': inv.price_per_share,
                'date': inv.date,
                'costs': inv.costs,
                'current_price': None,
                'profit': None,
                'total_value': None,
                'error': str(e)
            })
    
    return result

@app.delete('/investment/{investment_id}')
def delete_investment(investment_id: str, credentials: HTTPAuthorizationCredentials = Depends(security), db: Session = Depends(get_db)):
    user = get_current_user(credentials.credentials)
    if not user:
        raise HTTPException(status_code=401, detail='Invalid token')
    
    investment = db.query(InvestmentDB).filter(InvestmentDB.id == investment_id).first()
    if not investment:
        raise HTTPException(status_code=404, detail='Investment not found')
    
    db.delete(investment)
    db.commit()
    return {'message': 'Investment deleted successfully'}

@app.post('/purchase')
def add_purchase_endpoint(purchase: Purchase, credentials: HTTPAuthorizationCredentials = Depends(security)):
    user = get_current_user(credentials.credentials)
    if not user:
        raise HTTPException(status_code=401, detail='Invalid token')
    
    try:
        result = add_purchase(purchase.dict(), user.id)
        return result
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.get('/investments/summary')
def get_investments_summary(credentials: HTTPAuthorizationCredentials = Depends(security)):
    user = get_current_user(credentials.credentials)
    if not user:
        raise HTTPException(status_code=401, detail='Invalid token')
    
    try:
        summaries = get_all_investment_summaries(user.id)
        return summaries
    except Exception as e:
        print(f'Error in get_investments_summary: {e}')
        return []

@app.get('/investment/{ticker}/summary')
def get_investment_summary_endpoint(ticker: str, credentials: HTTPAuthorizationCredentials = Depends(security)):
    user = get_current_user(credentials.credentials)
    if not user:
        raise HTTPException(status_code=401, detail='Invalid token')
    
    try:
        summary = get_investment_summary(ticker, user.id)
        if summary:
            return summary
        else:
            raise HTTPException(status_code=404, detail='Investment not found')
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.delete('/purchase/{purchase_id}')
def delete_purchase_endpoint(purchase_id: str, credentials: HTTPAuthorizationCredentials = Depends(security)):
    user = get_current_user(credentials.credentials)
    if not user:
        raise HTTPException(status_code=401, detail='Invalid token')
    
    try:
        success = delete_purchase(purchase_id, user.id)
        if success:
            return {'message': 'Purchase deleted successfully'}
        else:
            raise HTTPException(status_code=404, detail='Purchase not found')
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.put('/purchase/{purchase_id}')
def update_purchase_endpoint(purchase_id: str, purchase_data: UpdatePurchase, credentials: HTTPAuthorizationCredentials = Depends(security)):
    user = get_current_user(credentials.credentials)
    if not user:
        raise HTTPException(status_code=401, detail='Invalid token')
    
    try:
        result = update_purchase(purchase_id, purchase_data.dict(), user.id)
        if result:
            return result
        else:
            raise HTTPException(status_code=404, detail='Purchase not found')
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.post('/migrate')
def migrate_endpoint(credentials: HTTPAuthorizationCredentials = Depends(security)):
    user = get_current_user(credentials.credentials)
    if not user:
        raise HTTPException(status_code=401, detail='Invalid token')
    
    try:
        migrate_old_investments(user.id)
        return {'message': 'Migration completed successfully'}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.get('/search')
def search_investments(query: str):
    try:
        results = search_stocks(query)
        return {'results': results}
    except Exception as e:
        print(f'Search error for query \'{query}\': {e}')
        # Return fallback results instead of error
        fallback_results = _get_fallback_search_results(query)
        return {'results': fallback_results}

@app.get('/suggestions')
def get_suggestions(query: str):
    try:
        suggestions = get_stock_suggestions(query)
        return {'suggestions': suggestions}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

def _get_fallback_search_results(query: str) -> List[Dict]:
    """Fallback search results when external APIs fail"""
    query_lower = query.lower()
    
    # Common stocks and ETFs database
    stock_database = [
        {'ticker': 'AAPL', 'name': 'Apple Inc.', 'type': 'Stock'},
        {'ticker': 'MSFT', 'name': 'Microsoft Corporation', 'type': 'Stock'},
        {'ticker': 'GOOGL', 'name': 'Alphabet Inc.', 'type': 'Stock'},
        {'ticker': 'AMZN', 'name': 'Amazon.com Inc.', 'type': 'Stock'},
        {'ticker': 'TSLA', 'name': 'Tesla Inc.', 'type': 'Stock'},
        {'ticker': 'META', 'name': 'Meta Platforms Inc.', 'type': 'Stock'},
        {'ticker': 'NVDA', 'name': 'NVIDIA Corporation', 'type': 'Stock'},
        {'ticker': 'NFLX', 'name': 'Netflix Inc.', 'type': 'Stock'},
        {'ticker': 'ASML.AS', 'name': 'ASML Holding N.V.', 'type': 'Stock'},
        {'ticker': 'SAP.DE', 'name': 'SAP SE', 'type': 'Stock'},
        {'ticker': 'LVMH.PA', 'name': 'LVMH Moët Hennessy Louis Vuitton', 'type': 'Stock'},
        {'ticker': 'KBC.BR', 'name': 'KBC Group NV', 'type': 'Stock'},
        {'ticker': 'INGA.AS', 'name': 'ING Groep N.V.', 'type': 'Stock'},
        {'ticker': 'ABI.BR', 'name': 'Anheuser-Busch InBev SA/NV', 'type': 'Stock'},
        {'ticker': 'SPY', 'name': 'SPDR S&P 500 ETF Trust', 'type': 'ETF'},
        {'ticker': 'QQQ', 'name': 'Invesco QQQ Trust', 'type': 'ETF'},
        {'ticker': 'VTI', 'name': 'Vanguard Total Stock Market ETF', 'type': 'ETF'},
        {'ticker': 'VXUS', 'name': 'Vanguard Total International Stock ETF', 'type': 'ETF'},
        {'ticker': 'BND', 'name': 'Vanguard Total Bond Market ETF', 'type': 'ETF'},
        {'ticker': 'GLD', 'name': 'SPDR Gold Shares', 'type': 'ETF'},
        {'ticker': 'VWRL.L', 'name': 'Vanguard FTSE All-World UCITS ETF', 'type': 'ETF'},
        {'ticker': 'IWDA.L', 'name': 'iShares Core MSCI World UCITS ETF', 'type': 'ETF'},
        {'ticker': 'BEL.BR', 'name': 'BEL 20 Index', 'type': 'Index'},
        {'ticker': 'BIRG.IE', 'name': 'Bank of Ireland Group PLC', 'type': 'Stock'},
    ]
    
    # Filter results based on query
    results = []
    for stock in stock_database:
        if (query_lower in stock['ticker'].lower() or 
            query_lower in stock['name'].lower()):
            results.append(stock)
    
    return results[:10]  # Return top 10 results
