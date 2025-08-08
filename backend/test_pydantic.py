#!/usr/bin/env python3
"""
Test Pydantic model
"""
from models import UserResponse
from datetime import datetime

# Test the UserResponse model
test_data = {
    "id": "test-id",
    "email": "test@example.com",
    "username": "testuser",
    "first_name": None,
    "last_name": None,
    "phone": None,
    "country": None,
    "is_admin": "true",
    "created_at": datetime.utcnow()
}

try:
    user_response = UserResponse(**test_data)
    print("✅ UserResponse model works")
    print("UserResponse data:", user_response.dict())
except Exception as e:
    print("❌ UserResponse model error:", e) 