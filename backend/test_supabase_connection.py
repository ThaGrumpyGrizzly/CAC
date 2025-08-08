#!/usr/bin/env python3
"""
Test script to verify Supabase connection
"""
import os
import sys
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

def test_supabase_connection():
    """Test connection to Supabase"""
    try:
        from supabase import create_client, Client
        
        # Get environment variables
        supabase_url = os.getenv("SUPABASE_URL")
        supabase_key = os.getenv("SUPABASE_ANON_KEY")
        
        if not supabase_url or not supabase_key:
            print("❌ Error: SUPABASE_URL and SUPABASE_ANON_KEY must be set in .env file")
            print(f"SUPABASE_URL: {'Set' if supabase_url else 'Not set'}")
            print(f"SUPABASE_ANON_KEY: {'Set' if supabase_key else 'Not set'}")
            return False
        
        print("🔍 Testing Supabase connection...")
        print(f"URL: {supabase_url}")
        print(f"Key: {supabase_key[:20]}...")
        
        # Initialize Supabase client
        supabase: Client = create_client(supabase_url, supabase_key)
        
        # Test connection by trying to access a table
        try:
            # Try to query the users table
            response = supabase.table('users').select('*').limit(1).execute()
            print("✅ Supabase connection successful!")
            print(f"Response status: {response}")
            return True
            
        except Exception as e:
            print(f"❌ Error querying database: {e}")
            print("This might be normal if the tables don't exist yet.")
            return False
            
    except ImportError as e:
        print(f"❌ Import error: {e}")
        print("Make sure you've installed supabase: pip install supabase")
        return False
    except Exception as e:
        print(f"❌ Connection error: {e}")
        return False

if __name__ == "__main__":
    success = test_supabase_connection()
    if success:
        print("\n🎉 Supabase is ready to use!")
    else:
        print("\n❌ Supabase setup needs attention.")
        print("Please check your .env file and credentials.") 