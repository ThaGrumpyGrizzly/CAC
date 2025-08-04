#!/usr/bin/env python3
# Use: py test_backend.py
"""
Simple test script for the Investment Tracker backend API
"""

import requests
import json
import time

def test_api_health():
    """Test if the API is running and healthy"""
    try:
        response = requests.get('http://localhost:8000/', timeout=5)
        if response.status_code == 200:
            print("✅ API is running and healthy")
            print(f"   Response: {response.json()}")
            return True
        else:
            print(f"❌ API returned status code: {response.status_code}")
            return False
    except requests.exceptions.ConnectionError:
        print("❌ Cannot connect to API. Make sure the backend server is running on http://localhost:8000")
        return False
    except Exception as e:
        print(f"❌ Error testing API: {e}")
        return False

def test_add_investment():
    """Test adding a new investment"""
    test_investment = {
        "ticker": "AAPL",
        "amount": 10,
        "price_per_share": 150.00,
        "date": "2024-01-15",
        "costs": 5.00
    }
    
    try:
        response = requests.post(
            'http://localhost:8000/investment',
            json=test_investment,
            timeout=10
        )
        
        if response.status_code == 200:
            data = response.json()
            print("✅ Successfully added test investment")
            print(f"   Ticker: {data.get('ticker')}")
            print(f"   Current Price: €{data.get('current_price')}")
            print(f"   Profit: €{data.get('profit')}")
            return True
        else:
            print(f"❌ Failed to add investment. Status: {response.status_code}")
            print(f"   Error: {response.text}")
            return False
    except Exception as e:
        print(f"❌ Error adding investment: {e}")
        return False

def test_get_investments():
    """Test getting all investments"""
    try:
        response = requests.get('http://localhost:8000/investments', timeout=10)
        
        if response.status_code == 200:
            investments = response.json()
            print(f"✅ Successfully retrieved {len(investments)} investments")
            
            for inv in investments:
                print(f"   - {inv.get('ticker')}: {inv.get('amount')} shares")
            
            return True
        else:
            print(f"❌ Failed to get investments. Status: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Error getting investments: {e}")
        return False

def main():
    """Run all tests"""
    print("🧪 Investment Tracker Backend API Tests")
    print("=" * 40)
    
    # Test 1: API Health
    if not test_api_health():
        print("\n❌ API health check failed. Please start the backend server first.")
        return
    
    print("\n" + "-" * 40)
    
    # Test 2: Add Investment
    if test_add_investment():
        print("\n" + "-" * 40)
        
        # Test 3: Get Investments
        test_get_investments()
    
    print("\n" + "=" * 40)
    print("🎉 All tests completed!")

if __name__ == "__main__":
    main() 