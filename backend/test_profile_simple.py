#!/usr/bin/env python3
import requests
import json

def test_profile_update_simple():
    """Simple test for profile update"""
    print("🧪 Simple Profile Update Test")
    print("=" * 40)
    
    API_BASE_URL = "http://localhost:8000"
    
    # Step 1: Login
    print("1. Logging in...")
    login_data = {
        "email": "Gust.philippaerts@outlook.com",
        "password": "admin123"
    }
    
    try:
        response = requests.post(f"{API_BASE_URL}/login", json=login_data)
        if response.status_code == 200:
            token = response.json()["access_token"]
            print("✅ Login successful")
        else:
            print(f"❌ Login failed: {response.status_code}")
            return
    except Exception as e:
        print(f"❌ Login error: {e}")
        return
    
    # Step 2: Update profile with simple data
    print("2. Updating profile...")
    update_data = {
        "first_name": "Test First",
        "last_name": "Test Last",
        "phone": "123456789",
        "country": "Test Country"
    }
    
    try:
        response = requests.put(f"{API_BASE_URL}/profile", json=update_data, headers={"Authorization": f"Bearer {token}"})
        print(f"Response status: {response.status_code}")
        print(f"Response text: {response.text}")
        
        if response.status_code == 200:
            updated_profile = response.json()
            print("✅ Profile updated successfully")
            print(f"   First Name: {updated_profile.get('first_name')}")
            print(f"   Last Name: {updated_profile.get('last_name')}")
            print(f"   Phone: {updated_profile.get('phone')}")
            print(f"   Country: {updated_profile.get('country')}")
        else:
            print(f"❌ Failed to update profile: {response.status_code}")
            print(f"   Response: {response.text}")
    except Exception as e:
        print(f"❌ Error updating profile: {e}")

if __name__ == "__main__":
    test_profile_update_simple() 