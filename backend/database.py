from sqlalchemy import create_engine, Column, Float, String, DateTime, Integer, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship
import os
from datetime import datetime
import uuid

# Database configuration
# Use Railway's DATABASE_URL if available, otherwise use SQLite for development
DATABASE_URL = os.getenv('DATABASE_URL', 'sqlite:///./investment_tracker.db')

# If DATABASE_URL is from Railway (PostgreSQL), we need to handle the format
if DATABASE_URL.startswith('postgres://'):
    DATABASE_URL = DATABASE_URL.replace('postgres://', 'postgresql://', 1)

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

class UserDB(Base):
    __tablename__ = 'users'
    
    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    email = Column(String, unique=True, nullable=False, index=True)
    username = Column(String, unique=True, nullable=False, index=True)
    hashed_password = Column(String, nullable=False)
    is_admin = Column(String, default='false')  # 'true' or 'false' as string
    
    # Profile fields
    first_name = Column(String, nullable=True)
    last_name = Column(String, nullable=True)
    phone = Column(String, nullable=True)
    country = Column(String, nullable=True)
    
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationship to purchases
    purchases = relationship('PurchaseDB', back_populates='user')

class PurchaseDB(Base):
    __tablename__ = 'purchases'
    
    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    user_id = Column(String, ForeignKey('users.id'), nullable=False)
    ticker = Column(String, nullable=False)
    amount = Column(Float, nullable=False)
    price_per_share = Column(Float, nullable=False)
    date = Column(String, nullable=False)  # Store as string for simplicity
    costs = Column(Float, nullable=False, default=0.0)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationship to user
    user = relationship('UserDB', back_populates='purchases')

# Keep the old table for backward compatibility during migration
class InvestmentDB(Base):
    __tablename__ = 'investments'
    
    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    ticker = Column(String, nullable=False)
    amount = Column(Float, nullable=False)
    price_per_share = Column(Float, nullable=False)
    date = Column(String, nullable=False)  # Store as string for simplicity
    costs = Column(Float, nullable=False, default=0.0)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def create_tables():
    Base.metadata.create_all(bind=engine)

# Initialize database tables
if __name__ == '__main__':
    create_tables()
    print('Database tables created successfully!')
