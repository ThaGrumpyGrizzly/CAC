#!/usr/bin/env python3
"""
Test profile function directly
"""
from app import get_user_profile
from services.auth_simple import create_access_token
from fastapi.security import HTTPAuthorizationCredentials
from fastapi import HTTPException

def test_direct_profile():
    """Test the profile function directly"""
    print("🔍 Testing Profile Function Directly")
    print("=" * 40)
    
    # Create a token for the user
    token = create_access_token(data={'sub': 'Gust.philippaerts@outlook.com'})
    
    # Create credentials object
    credentials = HTTPAuthorizationCredentials(credentials=token, scheme="bearer")
    
    try:
        # Call the profile function directly
        from database import get_db
        db = next(get_db())
        
        response = get_user_profile(credentials, db)
        print("✅ Profile function works")
        print("Response:", response)
        
        # Check if is_admin is in the response
        if hasattr(response, 'is_admin'):
            print(f"✅ is_admin field present: {response.is_admin}")
        else:
            print("❌ is_admin field missing")
            
    except Exception as e:
        print("❌ Error:", e)

if __name__ == "__main__":
    test_direct_profile() 