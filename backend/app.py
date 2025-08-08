from fastapi import FastAPI, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from models import Investment, Purchase, UpdatePurchase, UserCreate, UserLogin, UserResponse, UserUpdate, Token, ForgotPasswordRequest, ResetPasswordRequest, ChangePasswordRequest, PasswordResetResponse
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
from services.auth_simple import (
    get_password_hash, authenticate_user, create_access_token, 
    get_current_user, get_user_by_email, get_user_by_username
)
from services.password_reset import (
    generate_reset_token, store_reset_token, verify_reset_token,
    clear_reset_token, reset_user_password, change_user_password
)
from services.admin_service import (
    get_all_users, get_user_details, get_top_investments, get_user_statistics,
    make_user_admin, remove_admin_status, delete_user, get_popular_tickers, get_stock_analytics
)
from database import get_db, InvestmentDB, UserDB
from sqlalchemy.orm import Session
from typing import List, Dict
from datetime import timedelta
import os
from datetime import datetime

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

@app.get('/health-simple')
def simple_health_check():
    """Simple health check that doesn't require database connection"""
    return {
        'status': 'healthy',
        'service': 'Investment Tracker API',
        'message': 'Service is running',
        'timestamp': datetime.utcnow().isoformat()
    }

@app.get('/health')
def health_check():
    try:
        # Basic service health check
        service_status = 'healthy'
        database_status = 'unknown'
        error_message = None
        
        # Test database connection only if DATABASE_URL is available
        if os.getenv('DATABASE_URL'):
            try:
                from database import SessionLocal
                from sqlalchemy import text
                db = SessionLocal()
                db.execute(text('SELECT 1'))
                db.close()
                database_status = 'connected'
            except Exception as db_error:
                database_status = 'error'
                error_message = f"Database error: {str(db_error)}"
        else:
            database_status = 'not_configured'
        
        return {
            'status': service_status,
            'service': 'Investment Tracker API',
            'database': database_status,
            'timestamp': datetime.utcnow().isoformat(),
            'error': error_message
        }
    except Exception as e:
        return {
            'status': 'unhealthy',
            'service': 'Investment Tracker API',
            'database': 'error',
            'error': str(e),
            'timestamp': datetime.utcnow().isoformat()
        }

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
        hashed_password=hashed_password,
        first_name=user.first_name,
        last_name=user.last_name,
        phone=user.phone,
        country=user.country
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    
    return UserResponse(
        id=db_user.id,
        email=db_user.email,
        username=db_user.username,
        first_name=db_user.first_name,
        last_name=db_user.last_name,
        phone=db_user.phone,
        country=db_user.country,
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

@app.post('/forgot-password', response_model=PasswordResetResponse)
def forgot_password(request: ForgotPasswordRequest, db: Session = Depends(get_db)):
    """Request password reset"""
    user = get_user_by_email(db, request.email)
    if not user:
        # Don't reveal if user exists or not for security
        return PasswordResetResponse(
            message="If an account with this email exists, a password reset link has been sent.",
            success=True
        )
    
    # Generate reset token
    reset_token = generate_reset_token()
    store_reset_token(request.email, reset_token)
    
    # In a real application, send email here
    # For now, we'll just return the token in the response for testing
    print(f"Password reset token for {request.email}: {reset_token}")
    
    return PasswordResetResponse(
        message="Password reset link sent to your email. Check the console for the token.",
        success=True
    )

@app.post('/reset-password', response_model=PasswordResetResponse)
def reset_password(request: ResetPasswordRequest):
    """Reset password using token"""
    if not verify_reset_token(request.email, request.reset_token):
        raise HTTPException(status_code=400, detail='Invalid or expired reset token')
    
    success = reset_user_password(request.email, request.new_password)
    if not success:
        raise HTTPException(status_code=400, detail='Failed to reset password')
    
    # Clear the used token
    clear_reset_token(request.email)
    
    return PasswordResetResponse(
        message="Password reset successful. You can now login with your new password.",
        success=True
    )

@app.post('/change-password', response_model=PasswordResetResponse)
def change_password(request: ChangePasswordRequest, credentials: HTTPAuthorizationCredentials = Depends(security)):
    """Change password (requires authentication)"""
    user = get_current_user(credentials.credentials)
    if not user:
        raise HTTPException(status_code=401, detail='Invalid token')
    
    success = change_user_password(user.email, request.current_password, request.new_password)
    if not success:
        raise HTTPException(status_code=400, detail='Current password is incorrect')
    
    return PasswordResetResponse(
        message="Password changed successfully.",
        success=True
    )

@app.get('/profile', response_model=UserResponse)
def get_user_profile(credentials: HTTPAuthorizationCredentials = Depends(security), db: Session = Depends(get_db)):
    user = get_current_user(credentials.credentials)
    if not user:
        raise HTTPException(status_code=401, detail='Invalid token')
    
    # Debug output
    print(f"DEBUG: User admin status: {user.is_admin}, Type: {type(user.is_admin)}")
    
    response = UserResponse(
        id=user.id,
        email=user.email,
        username=user.username,
        first_name=user.first_name,
        last_name=user.last_name,
        phone=user.phone,
        country=user.country,
        is_admin=user.is_admin,
        created_at=user.created_at
    )
    
    print(f"DEBUG: Response admin status: {response.is_admin}")
    return response

@app.put('/profile', response_model=UserResponse)
def update_user_profile(user_update: UserUpdate, credentials: HTTPAuthorizationCredentials = Depends(security), db: Session = Depends(get_db)):
    # Get user from token
    token_user = get_current_user(credentials.credentials)
    if not token_user:
        raise HTTPException(status_code=401, detail='Invalid token')
    
    # Get user from database session
    user = db.query(UserDB).filter(UserDB.id == token_user.id).first()
    if not user:
        raise HTTPException(status_code=404, detail='User not found')
    
    # Update user fields
    if user_update.first_name is not None:
        user.first_name = user_update.first_name
    if user_update.last_name is not None:
        user.last_name = user_update.last_name
    if user_update.email is not None:
        # Check if email is already taken by another user
        existing_user = db.query(UserDB).filter(UserDB.email == user_update.email, UserDB.id != user.id).first()
        if existing_user:
            raise HTTPException(status_code=400, detail='Email already registered')
        user.email = user_update.email
    if user_update.phone is not None:
        user.phone = user_update.phone
    if user_update.country is not None:
        user.country = user_update.country
    
    # Update the updated_at timestamp
    user.updated_at = datetime.utcnow()
    
    try:
        db.commit()
        db.refresh(user)
        
        # Return updated user profile
        response = UserResponse(
            id=user.id,
            email=user.email,
            username=user.username,
            first_name=user.first_name,
            last_name=user.last_name,
            phone=user.phone,
            country=user.country,
            is_admin=user.is_admin,
            created_at=user.created_at
        )
        return response
    except Exception as e:
        db.rollback()
        print(f"Error updating profile: {e}")
        raise HTTPException(status_code=500, detail=f'Failed to update profile: {str(e)}')

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

@app.get('/test-stock-price/{ticker}')
def test_stock_price(ticker: str):
    """Test endpoint to get current stock price"""
    try:
        from services.stock_price_service import stock_price_service
        price = stock_price_service.get_stock_price(ticker)
        if price:
            return {'ticker': ticker, 'current_price': price, 'status': 'success'}
        else:
            return {'ticker': ticker, 'current_price': None, 'status': 'not_found'}
    except ImportError as e:
        return {'ticker': ticker, 'error': f'Import error: {str(e)}', 'status': 'error'}
    except Exception as e:
        return {'ticker': ticker, 'error': str(e), 'status': 'error'}

@app.get('/debug-stock-prices')
def debug_stock_prices():
    """Debug endpoint to test stock price service"""
    try:
        from services.stock_price_service import stock_price_service
        from services.admin_service import get_stock_analytics
        
        # Test individual stock prices
        test_results = {}
        test_tickers = ['NKE', 'BEL.BR', 'BIRG.L', 'COLR.BR']
        
        for ticker in test_tickers:
            try:
                price = stock_price_service.get_stock_price(ticker)
                test_results[ticker] = {
                    'price': price,
                    'status': 'success' if price else 'no_price'
                }
            except Exception as e:
                test_results[ticker] = {
                    'price': None,
                    'status': 'error',
                    'error': str(e)
                }
        
        # Test the full analytics function
        try:
            analytics = get_stock_analytics()
            return {
                'individual_tests': test_results,
                'analytics_function': 'success',
                'analytics_data': analytics
            }
        except Exception as e:
            return {
                'individual_tests': test_results,
                'analytics_function': 'error',
                'analytics_error': str(e)
            }
            
    except ImportError as e:
        return {'error': f'Import error: {str(e)}'}
    except Exception as e:
        return {'error': f'General error: {str(e)}'}

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

# Admin endpoints
def check_admin_permissions(credentials: HTTPAuthorizationCredentials = Depends(security)):
    """Check if user has admin permissions"""
    user = get_current_user(credentials.credentials)
    if not user:
        raise HTTPException(status_code=401, detail='Invalid token')
    
    # Check if user is admin
    if user.is_admin != 'true':
        raise HTTPException(status_code=403, detail='Admin access required')
    
    return user

@app.get('/admin/users')
def get_users_admin(admin_user = Depends(check_admin_permissions)):
    """Get all users (admin only)"""
    try:
        users = get_all_users()
        return {'users': users}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.get('/admin/users/{user_id}')
def get_user_details_admin(user_id: str, admin_user = Depends(check_admin_permissions)):
    """Get detailed user information (admin only)"""
    try:
        user_details = get_user_details(user_id)
        if user_details:
            return user_details
        else:
            raise HTTPException(status_code=404, detail='User not found')
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.get('/admin/statistics')
def get_admin_statistics(admin_user = Depends(check_admin_permissions)):
    """Get overall statistics (admin only)"""
    try:
        stats = get_user_statistics()
        return stats
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.get('/admin/top-investments')
def get_top_investments_admin(limit: int = 10, admin_user = Depends(check_admin_permissions)):
    """Get top investments across all users (admin only)"""
    try:
        top_investments = get_top_investments(limit)
        return {'top_investments': top_investments}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.get('/admin/popular-tickers')
def get_popular_tickers_admin(admin_user = Depends(check_admin_permissions)):
    """Get most popular tickers (admin only)"""
    try:
        popular_tickers = get_popular_tickers()
        return {'popular_tickers': popular_tickers}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.get('/admin/stock-analytics')
def get_stock_analytics_admin(admin_user = Depends(check_admin_permissions)):
    """Get stock analytics with user counts and average buy prices (admin only)"""
    try:
        result = get_stock_analytics()
        return result
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.post('/admin/users/{user_id}/make-admin')
def make_user_admin_endpoint(user_id: str, admin_user = Depends(check_admin_permissions)):
    """Make a user an admin (admin only)"""
    try:
        success = make_user_admin(user_id)
        if success:
            return {'message': 'User made admin successfully'}
        else:
            raise HTTPException(status_code=404, detail='User not found')
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.post('/admin/users/{user_id}/remove-admin')
def remove_admin_status_endpoint(user_id: str, admin_user = Depends(check_admin_permissions)):
    """Remove admin status from a user (admin only)"""
    try:
        success = remove_admin_status(user_id)
        if success:
            return {'message': 'Admin status removed successfully'}
        else:
            raise HTTPException(status_code=404, detail='User not found')
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.delete('/admin/users/{user_id}')
def delete_user_admin(user_id: str, admin_user = Depends(check_admin_permissions)):
    """Delete a user and all their purchases (admin only)"""
    try:
        success = delete_user(user_id)
        if success:
            return {'message': 'User deleted successfully'}
        else:
            raise HTTPException(status_code=404, detail='User not found')
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.post('/make-me-admin')
def make_me_admin_endpoint(credentials: HTTPAuthorizationCredentials = Depends(security)):
    """Make the current user an admin (for testing)"""
    try:
        user = get_current_user(credentials.credentials)
        if not user:
            raise HTTPException(status_code=401, detail='Invalid token')
        
        # Make user admin
        from database import SessionLocal
        db = SessionLocal()
        try:
            db_user = db.query(UserDB).filter(UserDB.id == user.id).first()
            if db_user:
                db_user.is_admin = 'true'
                db.commit()
                return {'message': 'User made admin successfully', 'user_id': user.id}
            else:
                raise HTTPException(status_code=404, detail='User not found')
        finally:
            db.close()
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)