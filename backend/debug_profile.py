#!/usr/bin/env python3
"""
Debug script to test profile endpoint
"""
from services.auth_simple import get_current_user
from database import SessionLocal, UserDB

def debug_profile():
    """Debug the profile endpoint"""
    print("🔍 Debugging Profile Endpoint")
    print("=" * 40)
    
    # Test with a known token (you'll need to get this from a login)
    # For now, let's just check the user directly
    db = SessionLocal()
    try:
        user = db.query(UserDB).filter(UserDB.email == 'Gust.philippaerts@outlook.com').first()
        if user:
            print(f"✅ User found in database:")
            print(f"   ID: {user.id}")
            print(f"   Email: {user.email}")
            print(f"   Username: {user.username}")
            print(f"   Admin Status: {user.is_admin}")
            print(f"   Admin Type: {type(user.is_admin)}")
            print(f"   First Name: {user.first_name}")
            print(f"   Last Name: {user.last_name}")
            print(f"   Phone: {user.phone}")
            print(f"   Country: {user.country}")
        else:
            print("❌ User not found")
    finally:
        db.close()

if __name__ == "__main__":
    debug_profile() 