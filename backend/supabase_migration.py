#!/usr/bin/env python3
"""
Migration script to move from SQLite to Supabase
"""
import os
import sys
from sqlalchemy import create_engine, text
from database import SessionLocal, UserDB, PurchaseDB
from supabase import create_client, Client
from dotenv import load_dotenv

load_dotenv()

# Supabase configuration
SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_ANON_KEY")

if not SUPABASE_URL or not SUPABASE_KEY:
    print("❌ Error: SUPABASE_URL and SUPABASE_ANON_KEY must be set in .env file")
    sys.exit(1)

def migrate_to_supabase():
    """Migrate data from SQLite to Supabase"""
    try:
        print("🔄 Starting migration to Supabase...")
        
        # Initialize Supabase client
        supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)
        
        # Get SQLite data
        db = SessionLocal()
        
        # Migrate users
        print("📊 Migrating users...")
        users = db.query(UserDB).all()
        for user in users:
            try:
                # Check if user already exists
                existing_user = supabase.table('users').select('*').eq('id', user.id).execute()
                
                if not existing_user.data:
                    user_data = {
                        'id': user.id,
                        'email': user.email,
                        'username': user.username,
                        'is_admin': user.is_admin == 'true',
                        'created_at': user.created_at.isoformat() if user.created_at else None,
                        'updated_at': user.updated_at.isoformat() if user.updated_at else None
                    }
                    supabase.table('users').insert(user_data).execute()
                    print(f"✅ Migrated user: {user.email}")
                else:
                    print(f"⏭️  User already exists: {user.email}")
                    
            except Exception as e:
                print(f"❌ Error migrating user {user.email}: {e}")
        
        # Migrate purchases
        print("📊 Migrating purchases...")
        purchases = db.query(PurchaseDB).all()
        for purchase in purchases:
            try:
                purchase_data = {
                    'id': purchase.id,
                    'user_id': purchase.user_id,
                    'ticker': purchase.ticker,
                    'amount': float(purchase.amount),
                    'price_per_share': float(purchase.price_per_share),
                    'costs': float(purchase.costs),
                    'purchase_date': purchase.purchase_date.isoformat() if purchase.purchase_date else None,
                    'created_at': purchase.created_at.isoformat() if purchase.created_at else None,
                    'updated_at': purchase.updated_at.isoformat() if purchase.updated_at else None
                }
                supabase.table('purchases').insert(purchase_data).execute()
                print(f"✅ Migrated purchase: {purchase.ticker} - {purchase.amount} shares")
                
            except Exception as e:
                print(f"❌ Error migrating purchase {purchase.id}: {e}")
        
        db.close()
        print("✅ Migration completed successfully!")
        
    except Exception as e:
        print(f"❌ Migration failed: {e}")
        sys.exit(1)

if __name__ == "__main__":
    migrate_to_supabase() 