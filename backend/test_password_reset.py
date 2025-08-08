#!/usr/bin/env python3
"""
Test script for password reset functionality
"""
import requests
import json

BASE_URL = "http://localhost:8000"

def test_password_reset():
    """Test the complete password reset flow"""
    print("🧪 Testing Password Reset Functionality")
    print("=" * 50)
    
    # Test data
    test_email = "Gust.philippaerts@outlook.com"
    test_password = "newpassword123"
    
    # Step 1: Request password reset
    print("1. Requesting password reset...")
    try:
        response = requests.post(f"{BASE_URL}/forgot-password", json={
            "email": test_email
        })
        
        if response.status_code == 200:
            print("✅ Password reset request successful")
            print(f"   Response: {response.json()}")
        else:
            print(f"❌ Password reset request failed: {response.status_code}")
            print(f"   Response: {response.text}")
            return False
    except Exception as e:
        print(f"❌ Error requesting password reset: {e}")
        return False
    
    # Step 2: Get the reset token from console (you'll need to check the backend console)
    print("\n2. Check the backend console for the reset token")
    print("   The token will be printed in the backend console output")
    
    # Step 3: Test password change (requires authentication)
    print("\n3. Testing password change (requires login)...")
    
    # First login to get a token
    try:
        login_response = requests.post(f"{BASE_URL}/login", json={
            "email": test_email,
            "password": "vieGg4i'oc"  # Current password
        })
        
        if login_response.status_code == 200:
            token = login_response.json()["access_token"]
            print("✅ Login successful")
            
            # Test password change
            change_response = requests.post(f"{BASE_URL}/change-password", 
                json={
                    "current_password": "vieGg4i'oc",
                    "new_password": "newpassword123"
                },
                headers={"Authorization": f"Bearer {token}"}
            )
            
            if change_response.status_code == 200:
                print("✅ Password change successful")
                print(f"   Response: {change_response.json()}")
            else:
                print(f"❌ Password change failed: {change_response.status_code}")
                print(f"   Response: {change_response.text}")
        else:
            print(f"❌ Login failed: {login_response.status_code}")
            print(f"   Response: {login_response.text}")
    except Exception as e:
        print(f"❌ Error testing password change: {e}")
    
    print("\n🎉 Password reset functionality test completed!")
    print("To test the reset token flow:")
    print("1. Check the backend console for the reset token")
    print("2. Use the token in the frontend forgot password page")
    print("3. Or test the /reset-password endpoint directly")

if __name__ == "__main__":
    test_password_reset() 