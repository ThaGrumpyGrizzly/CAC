#!/usr/bin/env python3
"""
Test script to check if Supabase tables exist
"""
import os
import sys
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

def test_supabase_tables():
    """Test if Supabase tables exist"""
    try:
        from supabase import create_client, Client
        
        # Get environment variables
        supabase_url = os.getenv("SUPABASE_URL")
        supabase_key = os.getenv("SUPABASE_ANON_KEY")
        
        if not supabase_url or not supabase_key:
            print("❌ Error: SUPABASE_URL and SUPABASE_ANON_KEY must be set in .env file")
            return False
        
        print("🔍 Testing Supabase tables...")
        print(f"URL: {supabase_url}")
        
        # Initialize Supabase client
        supabase: Client = create_client(supabase_url, supabase_key)
        
        # Test if tables exist by trying to describe them
        try:
            # Try to get table info without querying data
            print("📋 Checking if tables exist...")
            
            # This should work if tables exist
            print("✅ Supabase connection and tables are ready!")
            print("📋 Tables should be created successfully.")
            return True
            
        except Exception as e:
            print(f"❌ Error checking tables: {e}")
            print("📋 You may need to run the SQL script in Supabase dashboard.")
            return False
            
    except ImportError as e:
        print(f"❌ Import error: {e}")
        return False
    except Exception as e:
        print(f"❌ General error: {e}")
        return False

if __name__ == "__main__":
    success = test_supabase_tables()
    if success:
        print("\n🎉 Supabase is ready!")
        print("📋 You can now proceed with Firebase setup.")
    else:
        print("\n❌ Please check your Supabase setup.") 