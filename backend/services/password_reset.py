import secrets
import hashlib
from datetime import datetime, timedelta
from typing import Optional
from database import SessionLocal, UserDB
from sqlalchemy.orm import Session

# In-memory storage for reset tokens (in production, use Redis or database)
reset_tokens = {}

def generate_reset_token() -> str:
    """Generate a secure reset token"""
    return secrets.token_urlsafe(32)

def store_reset_token(email: str, token: str, expires_in: int = 3600) -> None:
    """Store reset token with expiration"""
    reset_tokens[email] = {
        'token': token,
        'expires_at': datetime.utcnow() + timedelta(seconds=expires_in)
    }

def verify_reset_token(email: str, token: str) -> bool:
    """Verify if reset token is valid and not expired"""
    if email not in reset_tokens:
        return False
    
    token_data = reset_tokens[email]
    if datetime.utcnow() > token_data['expires_at']:
        # Remove expired token
        del reset_tokens[email]
        return False
    
    return token_data['token'] == token

def clear_reset_token(email: str) -> None:
    """Clear reset token after use"""
    if email in reset_tokens:
        del reset_tokens[email]

def hash_password(password: str) -> str:
    """Hash password using SHA256 (same as auth_simple.py)"""
    return hashlib.sha256(password.encode()).hexdigest()

def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Verify password hash"""
    return hash_password(plain_password) == hashed_password

def get_user_by_email(db: Session, email: str) -> Optional[UserDB]:
    """Get user by email"""
    return db.query(UserDB).filter(UserDB.email == email).first()

def reset_user_password(email: str, new_password: str) -> bool:
    """Reset user password"""
    db = SessionLocal()
    try:
        user = get_user_by_email(db, email)
        if not user:
            return False
        
        # Hash the new password
        hashed_password = hash_password(new_password)
        
        # Update the password
        user.hashed_password = hashed_password
        db.commit()
        
        return True
    except Exception as e:
        print(f"Error resetting password: {e}")
        return False
    finally:
        db.close()

def change_user_password(email: str, current_password: str, new_password: str) -> bool:
    """Change user password (requires current password)"""
    db = SessionLocal()
    try:
        user = get_user_by_email(db, email)
        if not user:
            return False
        
        # Verify current password
        if not verify_password(current_password, user.hashed_password):
            return False
        
        # Hash the new password
        hashed_password = hash_password(new_password)
        
        # Update the password
        user.hashed_password = hashed_password
        db.commit()
        
        return True
    except Exception as e:
        print(f"Error changing password: {e}")
        return False
    finally:
        db.close() 