#!/usr/bin/env python3
"""
Simple test to verify server is running updated code
"""
import requests

# Test the root endpoint to see if server is running
response = requests.get('http://localhost:8000/')
print("Server response:", response.json()) 