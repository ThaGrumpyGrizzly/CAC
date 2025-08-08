from pydantic import BaseModel, Field
from datetime import date, datetime
from typing import Optional, List

# User models
class UserCreate(BaseModel):
    email: str = Field(..., description='User email address')
    username: str = Field(..., min_length=3, max_length=50)
    password: str = Field(..., min_length=6)
    first_name: Optional[str] = Field(None, description='User first name')
    last_name: Optional[str] = Field(None, description='User last name')
    phone: Optional[str] = Field(None, description='User phone number')
    country: Optional[str] = Field(None, description='User country')

class UserLogin(BaseModel):
    email: str = Field(..., description='User email address')
    password: str

class UserResponse(BaseModel):
    id: str
    email: str
    username: str
    first_name: Optional[str]
    last_name: Optional[str]
    phone: Optional[str]
    country: Optional[str]
    is_admin: str
    created_at: datetime

class UserUpdate(BaseModel):
    first_name: Optional[str] = Field(None, description='User first name')
    last_name: Optional[str] = Field(None, description='User last name')
    email: Optional[str] = Field(None, description='User email address')
    phone: Optional[str] = Field(None, description='User phone number')
    country: Optional[str] = Field(None, description='User country')

class Token(BaseModel):
    access_token: str
    token_type: str

# Password reset models
class ForgotPasswordRequest(BaseModel):
    email: str = Field(..., description='User email address')

class ResetPasswordRequest(BaseModel):
    email: str = Field(..., description='User email address')
    reset_token: str = Field(..., description='Reset token from email')
    new_password: str = Field(..., min_length=6, description='New password')

class ChangePasswordRequest(BaseModel):
    current_password: str = Field(..., description='Current password')
    new_password: str = Field(..., min_length=6, description='New password')

class PasswordResetResponse(BaseModel):
    message: str
    success: bool

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
