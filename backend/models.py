from pydantic import BaseModel, Field, EmailStr
from datetime import date, datetime
from typing import Optional, List

# User models
class UserCreate(BaseModel):
    email: EmailStr
    username: str = Field(..., min_length=3, max_length=50)
    password: str = Field(..., min_length=6)

class UserLogin(BaseModel):
    email: EmailStr
    password: str

class UserResponse(BaseModel):
    id: str
    email: str
    username: str
    created_at: datetime

class Token(BaseModel):
    access_token: str
    token_type: str

# Existing models
class Purchase(BaseModel):
    ticker: str = Field(..., description='Stock ticker symbol (e.g., AAPL, ASML.AS)')
    amount: float = Field(..., gt=0, description='Number of shares purchased')
    price_per_share: float = Field(..., gt=0, description='Price per share at purchase')
    date: str = Field(..., description='Purchase date in YYYY-MM-DD format')
    costs: float = Field(..., ge=0, description='Additional costs (brokerage fees, etc.)')

class PurchaseResponse(BaseModel):
    id: str
    ticker: str
    amount: float
    price_per_share: float
    date: str
    costs: float
    created_at: str

class UpdatePurchase(BaseModel):
    amount: float = Field(..., gt=0, description='Number of shares purchased')
    price_per_share: float = Field(..., gt=0, description='Price per share at purchase')
    date: str = Field(..., description='Purchase date in YYYY-MM-DD format')
    costs: float = Field(..., ge=0, description='Additional costs (brokerage fees, etc.)')

class InvestmentSummary(BaseModel):
    ticker: str
    total_amount: float
    average_price: float
    total_costs: float
    current_price: Optional[float]
    total_value: Optional[float]
    total_profit: Optional[float]
    profit_percentage: Optional[float]
    purchases: List[PurchaseResponse]

class InvestmentCreate(BaseModel):
    ticker: str = Field(..., description='Stock ticker symbol')
    amount: float = Field(..., gt=0, description='Number of shares')
    price_per_share: float = Field(..., gt=0, description='Price per share')
    date: str = Field(..., description='Purchase date')
    costs: float = Field(..., ge=0, description='Additional costs')

# Keep old models for backward compatibility
class Investment(BaseModel):
    ticker: str = Field(..., description='Stock ticker symbol (e.g., AAPL, ASML.AS)')
    amount: float = Field(..., gt=0, description='Number of shares purchased')
    price_per_share: float = Field(..., gt=0, description='Price per share at purchase')
    date: str = Field(..., description='Purchase date in YYYY-MM-DD format')
    costs: float = Field(..., ge=0, description='Additional costs (brokerage fees, etc.)')

class InvestmentResponse(BaseModel):
    id: str
    ticker: str
    amount: float
    price_per_share: float
    date: str
    costs: float
    current_price: Optional[float]
    profit: Optional[float]
    total_value: Optional[float]
    error: Optional[str] = None
