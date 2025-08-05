#!/usr/bin/env python3
"""
Simple test script to verify deployment works
"""
import os
import sys
import requests
import time

def test_health_endpoint(base_url):
    """Test the health endpoint"""
    try:
        print(f"Testing health endpoint at {base_url}/health-simple")
        response = requests.get(f"{base_url}/health-simple", timeout=10)
        print(f"Status code: {response.status_code}")
        print(f"Response: {response.json()}")
        return response.status_code == 200
    except Exception as e:
        print(f"Error testing health endpoint: {e}")
        return False

def test_root_endpoint(base_url):
    """Test the root endpoint"""
    try:
        print(f"Testing root endpoint at {base_url}/")
        response = requests.get(f"{base_url}/", timeout=10)
        print(f"Status code: {response.status_code}")
        print(f"Response: {response.json()}")
        return response.status_code == 200
    except Exception as e:
        print(f"Error testing root endpoint: {e}")
        return False

if __name__ == "__main__":
    # Get the URL from command line or use default
    base_url = sys.argv[1] if len(sys.argv) > 1 else "http://localhost:8000"
    
    print(f"Testing deployment at: {base_url}")
    print("=" * 50)
    
    # Test endpoints
    root_ok = test_root_endpoint(base_url)
    health_ok = test_health_endpoint(base_url)
    
    print("=" * 50)
    if root_ok and health_ok:
        print("✅ All tests passed! Deployment is working.")
    else:
        print("❌ Some tests failed. Check the deployment.")
        sys.exit(1) 