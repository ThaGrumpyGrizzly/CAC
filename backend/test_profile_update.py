#!/usr/bin/env python3
import requests
import json

def test_profile_update():
    """Test the profile update functionality"""
    print("🧪 Testing Profile Update Functionality")
    print("=" * 50)
    
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
    
    # Step 2: Get current profile
    print("2. Getting current profile...")
    try:
        response = requests.get(f"{API_BASE_URL}/profile", headers={"Authorization": f"Bearer {token}"})
        if response.status_code == 200:
            current_profile = response.json()
            print("✅ Current profile retrieved")
            print(f"   First Name: {current_profile.get('first_name')}")
            print(f"   Last Name: {current_profile.get('last_name')}")
            print(f"   Phone: {current_profile.get('phone')}")
            print(f"   Country: {current_profile.get('country')}")
        else:
            print(f"❌ Failed to get profile: {response.status_code}")
            return
    except Exception as e:
        print(f"❌ Error getting profile: {e}")
        return
    
    # Step 3: Update profile
    print("3. Updating profile...")
    update_data = {
        "first_name": "Gust Updated",
        "last_name": "Philippaerts Updated",
        "phone": "+31 6 12345678",
        "country": "Netherlands"
    }
    
    try:
        response = requests.put(f"{API_BASE_URL}/profile", json=update_data, headers={"Authorization": f"Bearer {token}"})
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
            return
    except Exception as e:
        print(f"❌ Error updating profile: {e}")
        return
    
    # Step 4: Verify the update persisted
    print("4. Verifying update persisted...")
    try:
        response = requests.get(f"{API_BASE_URL}/profile", headers={"Authorization": f"Bearer {token}"})
        if response.status_code == 200:
            final_profile = response.json()
            print("✅ Profile verification successful")
            print(f"   First Name: {final_profile.get('first_name')}")
            print(f"   Last Name: {final_profile.get('last_name')}")
            print(f"   Phone: {final_profile.get('phone')}")
            print(f"   Country: {final_profile.get('country')}")
            
            # Check if values match what we set
            if (final_profile.get('first_name') == update_data['first_name'] and
                final_profile.get('last_name') == update_data['last_name'] and
                final_profile.get('phone') == update_data['phone'] and
                final_profile.get('country') == update_data['country']):
                print("🎉 Profile update test completed successfully!")
            else:
                print("❌ Profile update values don't match expected values")
        else:
            print(f"❌ Failed to verify profile: {response.status_code}")
    except Exception as e:
        print(f"❌ Error verifying profile: {e}")

if __name__ == "__main__":
    test_profile_update() 