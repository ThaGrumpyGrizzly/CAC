#!/usr/bin/env python3
"""
Script to reset admin password
"""
import hashlib
from database import SessionLocal, UserDB

def hash_password(password: str) -> str:
    """Hash password using SHA256 (same as auth_simple.py)"""
    return hashlib.sha256(password.encode()).hexdigest()

def reset_admin_password(email: str, new_password: str):
    """Reset password for admin user"""
    db = SessionLocal()
    try:
        # Find user by email
        user = db.query(UserDB).filter(UserDB.email == email).first()
        
        if not user:
            print(f"❌ No user found with email: {email}")
            return False
        
        # Check if user is admin
        if user.is_admin != 'true':
            print(f"❌ User {email} is not an admin")
            return False
        
        # Hash the new password
        hashed_password = hash_password(new_password)
        
        # Update the password
        user.hashed_password = hashed_password
        db.commit()
        
        print(f"✅ Successfully reset password for admin user: {email}")
        print(f"   Username: {user.username}")
        print(f"   New password: {new_password}")
        return True
        
    except Exception as e:
        print(f"❌ Error resetting password: {e}")
        return False
    finally:
        db.close()

def list_admin_users():
    """List all admin users"""
    db = SessionLocal()
    try:
        admin_users = db.query(UserDB).filter(UserDB.is_admin == 'true').all()
        print(f"\nFound {len(admin_users)} admin users:")
        print("=" * 50)
        
        for user in admin_users:
            print(f"ID: {user.id}")
            print(f"Username: {user.username}")
            print(f"Email: {user.email}")
            print(f"Created: {user.created_at}")
            print("-" * 30)
    finally:
        db.close()

if __name__ == "__main__":
    print("Admin Password Reset Tool")
    print("=" * 30)
    
    # List current admin users
    list_admin_users()
    
    # Get user input
    email = input("\nEnter admin email: ").strip()
    new_password = input("Enter new password: ").strip()
    
    if not email or not new_password:
        print("❌ Email and password are required")
        exit(1)
    
    # Reset the password
    success = reset_admin_password(email, new_password)
    
    if success:
        print("\n🎉 Password reset successful!")
        print("You can now login with your new password.")
    else:
        print("\n❌ Password reset failed!") 