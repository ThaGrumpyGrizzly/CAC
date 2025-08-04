from sqlalchemy import create_engine, Column, Float, String, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import os
from datetime import datetime
import uuid

# Database configuration
# For development, use SQLite by default
if os.getenv("USE_SQLITE", "true").lower() == "true":
    DATABASE_URL = "sqlite:///./investment_tracker.db"
else:
    DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://user:password@localhost/investment_db")

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

class PurchaseDB(Base):
    __tablename__ = "purchases"
    
    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    ticker = Column(String, nullable=False)
    amount = Column(Float, nullable=False)
    price_per_share = Column(Float, nullable=False)
    date = Column(String, nullable=False)  # Store as string for simplicity
    costs = Column(Float, nullable=False, default=0.0)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

# Keep the old table for backward compatibility during migration
class InvestmentDB(Base):
    __tablename__ = "investments"
    
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
if __name__ == "__main__":
    create_tables()
    print("Database tables created successfully!") 