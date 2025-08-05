#!/usr/bin/env python3
"""
Test script to verify all imports work correctly
"""
import sys
import os

def test_imports():
    """Test all critical imports"""
    try:
        print("Testing imports...")
        
        # Test basic imports
        print("✓ Testing basic imports...")
        import fastapi
        import uvicorn
        import requests
        import pydantic
        import sqlalchemy
        
        # Test app imports
        print("✓ Testing app imports...")
        from models import UserCreate, UserLogin, Investment, Purchase
        from database import get_db, create_tables
        from services.auth import get_password_hash, authenticate_user
        
        print("✓ All imports successful!")
        return True
        
    except Exception as e:
        print(f"❌ Import error: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    success = test_imports()
    if success:
        print("✅ All imports working correctly!")
        sys.exit(0)
    else:
        print("❌ Import test failed!")
        sys.exit(1) 