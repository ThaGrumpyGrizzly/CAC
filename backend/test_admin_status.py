#!/usr/bin/env python3
"""
Test script to verify admin status functionality
"""
import requests
import json

# Test admin access
def test_admin_access():
    base_url = "http://localhost:8000"
    
    # Step 1: Login as admin
    login_data = {
        "email": "admin@example.com",  # Change to your admin email
        "password": "admin123"  # Change to your admin password
    }
    
    print("1. Testing admin login...")
    try:
        login_response = requests.post(f"{base_url}/login", json=login_data)
        if login_response.status_code == 200:
            token = login_response.json()["access_token"]
            print("✅ Login successful")
            print(f"Token: {token[:20]}...")
        else:
            print(f"❌ Login failed: {login_response.status_code}")
            print(f"Response: {login_response.text}")
            return
    except Exception as e:
        print(f"❌ Login error: {e}")
        return
    
    # Step 2: Test admin endpoint
    headers = {"Authorization": f"Bearer {token}"}
    print("\n2. Testing admin endpoint...")
    try:
        admin_response = requests.get(f"{base_url}/admin/stock-analytics", headers=headers)
        if admin_response.status_code == 200:
            print("✅ Admin endpoint accessible")
            data = admin_response.json()
            print(f"Response: {json.dumps(data, indent=2)}")
        else:
            print(f"❌ Admin endpoint not accessible: {admin_response.status_code}")
            print(f"Response: {admin_response.text}")
    except Exception as e:
        print(f"❌ Error testing admin endpoint: {e}")

if __name__ == "__main__":
    test_admin_access() 