#!/usr/bin/env python3
"""
Debug script to test login functionality
"""
import os
import sys
import requests
import json
from database import SessionLocal, UserDB
from services.auth_simple import get_password_hash, authenticate_user

def test_database_connection():
    """Test if database is accessible and users table exists"""
    try:
        db = SessionLocal()
        # Try to query users table
        users = db.query(UserDB).all()
        print(f"✅ Database connection successful. Found {len(users)} users.")
        db.close()
        return True
    except Exception as e:
        print(f"❌ Database connection failed: {e}")
        return False

def test_user_registration(base_url):
    """Test user registration"""
    test_user = {
        "email": "test@example.com",
        "username": "testuser",
        "password": "testpass123"
    }
    
    try:
        print(f"Testing user registration at {base_url}/register")
        response = requests.post(
            f"{base_url}/register",
            json=test_user,
            headers={"Content-Type": "application/json"},
            timeout=10
        )
        print(f"Status code: {response.status_code}")
        print(f"Response: {response.json()}")
        return response.status_code == 200
    except Exception as e:
        print(f"❌ Registration test failed: {e}")
        return False

def test_user_login(base_url):
    """Test user login"""
    login_data = {
        "email": "test@example.com",
        "password": "testpass123"
    }
    
    try:
        print(f"Testing user login at {base_url}/login")
        response = requests.post(
            f"{base_url}/login",
            json=login_data,
            headers={"Content-Type": "application/json"},
            timeout=10
        )
        print(f"Status code: {response.status_code}")
        print(f"Response: {response.json()}")
        
        if response.status_code == 200:
            token = response.json().get('access_token')
            if token:
                print("✅ Login successful! Token received.")
                return True
            else:
                print("❌ Login successful but no token received.")
                return False
        else:
            print("❌ Login failed.")
            return False
    except Exception as e:
        print(f"❌ Login test failed: {e}")
        return False

def check_user_in_database():
    """Check if test user exists in database"""
    try:
        db = SessionLocal()
        user = db.query(UserDB).filter(UserDB.email == "test@example.com").first()
        if user:
            print(f"✅ Test user found in database: {user.email}")
            print(f"   Username: {user.username}")
            print(f"   Hashed password: {user.hashed_password[:20]}...")
            return True
        else:
            print("❌ Test user not found in database")
            return False
    except Exception as e:
        print(f"❌ Database query failed: {e}")
        return False
    finally:
        db.close()

def test_password_hashing():
    """Test password hashing functionality"""
    try:
        password = "testpass123"
        hashed = get_password_hash(password)
        print(f"✅ Password hashing works: {hashed[:20]}...")
        return True
    except Exception as e:
        print(f"❌ Password hashing failed: {e}")
        return False

if __name__ == "__main__":
    # Get the URL from command line or use default
    base_url = sys.argv[1] if len(sys.argv) > 1 else "http://localhost:8000"
    
    print(f"Debugging login issues at: {base_url}")
    print("=" * 60)
    
    # Run tests
    db_ok = test_database_connection()
    hash_ok = test_password_hashing()
    
    if db_ok:
        user_exists = check_user_in_database()
        if not user_exists:
            print("\nAttempting to register test user...")
            reg_ok = test_user_registration(base_url)
            if reg_ok:
                check_user_in_database()
    
    print("\nTesting login...")
    login_ok = test_user_login(base_url)
    
    print("=" * 60)
    if login_ok:
        print("✅ Login functionality is working!")
    else:
        print("❌ Login functionality has issues. Check the errors above.")
        print("\nTroubleshooting tips:")
        print("1. Check if DATABASE_URL is set correctly")
        print("2. Verify the backend is running")
        print("3. Check CORS configuration")
        print("4. Ensure frontend is pointing to correct backend URL") 