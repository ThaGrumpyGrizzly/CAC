#!/usr/bin/env python3
"""
Test script to check profile response
"""
import requests
import json

def test_profile_response():
    """Test the profile endpoint response"""
    print("🔍 Testing Profile Response")
    print("=" * 40)
    
    # Login
    login_response = requests.post('http://localhost:8000/login', json={
        'email': 'Gust.philippaerts@outlook.com',
        'password': 'vieGg4i\'oc'
    })
    
    if login_response.status_code != 200:
        print("❌ Login failed")
        return
    
    token = login_response.json()['access_token']
    print("✅ Login successful")
    
    # Get profile
    profile_response = requests.get('http://localhost:8000/profile', headers={
        'Authorization': f'Bearer {token}'
    })
    
    if profile_response.status_code != 200:
        print("❌ Profile request failed")
        return
    
    profile_data = profile_response.json()
    print("✅ Profile retrieved")
    print("Profile data:")
    print(json.dumps(profile_data, indent=2))
    
    # Check if is_admin is in the response
    if 'is_admin' in profile_data:
        print(f"✅ is_admin field present: {profile_data['is_admin']}")
    else:
        print("❌ is_admin field missing")

if __name__ == "__main__":
    test_profile_response() 