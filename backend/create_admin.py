#!/usr/bin/env python3
"""
Script to create an admin user
"""
from database import SessionLocal, UserDB

def create_admin():
    """Make the first user an admin"""
    db = SessionLocal()
    try:
        # Get the first user
        first_user = db.query(UserDB).first()
        
        if first_user:
            first_user.is_admin = 'true'
            db.commit()
            print(f"✅ Made user '{first_user.username}' ({first_user.email}) an admin!")
            return True
        else:
            print("❌ No users found in database")
            return False
    except Exception as e:
        print(f"❌ Error creating admin: {e}")
        return False
    finally:
        db.close()

def list_users():
    """List all users and their admin status"""
    db = SessionLocal()
    try:
        users = db.query(UserDB).all()
        print(f"\nFound {len(users)} users:")
        print("=" * 50)
        
        for user in users:
            admin_status = "ADMIN" if user.is_admin == 'true' else "USER"
            print(f"ID: {user.id}")
            print(f"Username: {user.username}")
            print(f"Email: {user.email}")
            print(f"Status: {admin_status}")
            print(f"Created: {user.created_at}")
            print("-" * 30)
    finally:
        db.close()

if __name__ == "__main__":
    print("Creating admin user...")
    success = create_admin()
    
    if success:
        print("\nCurrent users:")
        list_users()
    else:
        print("Failed to create admin user") 