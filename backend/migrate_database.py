#!/usr/bin/env python3
"""
Database migration script to add missing columns to existing database
"""
from sqlalchemy import text
from database import engine, SessionLocal, UserDB, Base
import os

def migrate_database():
    """Add missing columns to existing database"""
    print("🔧 Starting database migration...")
    
    # Check if we're using SQLite
    if 'sqlite' in str(engine.url):
        print("📁 Detected SQLite database")
        
        # Get list of existing columns
        with engine.connect() as conn:
            result = conn.execute(text("PRAGMA table_info(users)"))
            existing_columns = [row[1] for row in result.fetchall()]
            print(f"Existing columns: {existing_columns}")
            
            # Add missing columns
            missing_columns = []
            
            if 'first_name' not in existing_columns:
                missing_columns.append("first_name TEXT")
            if 'last_name' not in existing_columns:
                missing_columns.append("last_name TEXT")
            if 'phone' not in existing_columns:
                missing_columns.append("phone TEXT")
            if 'country' not in existing_columns:
                missing_columns.append("country TEXT")
            if 'updated_at' not in existing_columns:
                missing_columns.append("updated_at DATETIME")
            
            if missing_columns:
                print(f"Adding missing columns: {missing_columns}")
                for column_def in missing_columns:
                    try:
                        conn.execute(text(f"ALTER TABLE users ADD COLUMN {column_def}"))
                        print(f"✅ Added column: {column_def}")
                    except Exception as e:
                        print(f"⚠️ Column might already exist: {e}")
                conn.commit()
            else:
                print("✅ All columns already exist!")
                
    else:
        print("🗄️ Detected PostgreSQL database")
        # For PostgreSQL, we'll recreate the tables
        print("Recreating tables for PostgreSQL...")
        Base.metadata.drop_all(bind=engine)
        Base.metadata.create_all(bind=engine)
        print("✅ Tables recreated!")

def list_users():
    """List all users in the database"""
    db = SessionLocal()
    try:
        users = db.query(UserDB).all()
        print(f"\n📋 Found {len(users)} users:")
        print("=" * 50)
        
        for user in users:
            admin_status = "ADMIN" if user.is_admin == 'true' else "USER"
            print(f"ID: {user.id}")
            print(f"Username: {user.username}")
            print(f"Email: {user.email}")
            print(f"Status: {admin_status}")
            print(f"Created: {user.created_at}")
            if hasattr(user, 'first_name') and user.first_name:
                print(f"First Name: {user.first_name}")
            if hasattr(user, 'last_name') and user.last_name:
                print(f"Last Name: {user.last_name}")
            print("-" * 30)
    except Exception as e:
        print(f"❌ Error listing users: {e}")
    finally:
        db.close()

if __name__ == "__main__":
    print("Database Migration Tool")
    print("=" * 30)
    
    # Run migration
    migrate_database()
    
    # List users after migration
    print("\n📊 Current users after migration:")
    list_users()
    
    print("\n🎉 Migration completed!") 