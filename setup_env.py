#!/usr/bin/env python3
"""
Environment Variables Setup Helper for Coffee Investment Tracker
"""

import secrets
import os

def generate_secret_key():
    """Generate a secure secret key for JWT tokens"""
    return secrets.token_urlsafe(32)

def main():
    print("🔧 Coffee Investment Tracker - Environment Setup")
    print("=" * 50)
    print()
    
    # Generate secret key
    secret_key = generate_secret_key()
    print("🔑 Generated Secret Key:")
    print(f"SECRET_KEY={secret_key}")
    print()
    
    print("📋 Environment Variables You Need:")
    print("=" * 40)
    print()
    
    print("🔧 Backend Variables (for Render):")
    print("-" * 30)
    print(f"DATABASE_URL=postgresql://username:password@host:port/database")
    print(f"SECRET_KEY={secret_key}")
    print("ALGORITHM=HS256")
    print("ACCESS_TOKEN_EXPIRE_MINUTES=30")
    print()
    
    print("🌐 Frontend Variables (for Render):")
    print("-" * 30)
    print("VITE_API_BASE_URL=https://your-backend-service.onrender.com")
    print("VITE_SUPABASE_URL=your_supabase_url")
    print("VITE_SUPABASE_ANON_KEY=your_supabase_anon_key")
    print("VITE_FIREBASE_API_KEY=your_firebase_api_key")
    print("VITE_FIREBASE_AUTH_DOMAIN=your_project.firebaseapp.com")
    print("VITE_FIREBASE_PROJECT_ID=your_project_id")
    print("VITE_FIREBASE_STORAGE_BUCKET=your_project.appspot.com")
    print("VITE_FIREBASE_MESSAGING_SENDER_ID=your_messaging_sender_id")
    print("VITE_FIREBASE_APP_ID=your_app_id")
    print()
    
    print("📖 How to get these values:")
    print("=" * 30)
    print()
    print("1. Supabase Connection String:")
    print("   - Go to Supabase Dashboard → Settings → Database")
    print("   - Copy the 'Connection string' (URI format)")
    print("   - Replace [YOUR-PASSWORD] with your database password")
    print()
    print("2. Firebase Configuration:")
    print("   - Go to Firebase Console → Project Settings → General")
    print("   - Scroll to 'Your apps' section")
    print("   - Copy the configuration values")
    print()
    print("3. Backend URL:")
    print("   - Will be provided by Render after deployment")
    print("   - Format: https://your-service-name.onrender.com")
    print()
    
    print("🚀 Next Steps:")
    print("=" * 15)
    print("1. Commit your changes: git add . && git commit -m 'Add Render config' && git push")
    print("2. Go to render.com and sign up")
    print("3. Click 'New' → 'Blueprint'")
    print("4. Connect your GitHub repository")
    print("5. Update environment variables with the values above")
    print("6. Deploy!")
    print()
    print("🎉 Your app will be live once deployed!")

if __name__ == "__main__":
    main()
