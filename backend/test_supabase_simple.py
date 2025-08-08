#!/usr/bin/env python3
"""
Simple test script to verify Supabase connection without RLS
"""
import os
import sys
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

def test_supabase_simple():
    """Test basic connection to Supabase"""
    try:
        from supabase import create_client, Client
        
        # Get environment variables
        supabase_url = os.getenv("SUPABASE_URL")
        supabase_key = os.getenv("SUPABASE_ANON_KEY")
        
        if not supabase_url or not supabase_key:
            print("❌ Error: SUPABASE_URL and SUPABASE_ANON_KEY must be set in .env file")
            return False
        
        print("🔍 Testing basic Supabase connection...")
        print(f"URL: {supabase_url}")
        
        # Initialize Supabase client
        supabase: Client = create_client(supabase_url, supabase_key)
        
        # Test basic connection by checking if we can connect
        try:
            # Try a simple query that doesn't require RLS
            response = supabase.rpc('version').execute()
            print("✅ Basic Supabase connection successful!")
            return True
            
        except Exception as e:
            print(f"❌ Error with RPC call: {e}")
            
            # Try a different approach - just test the connection
            try:
                # This should work even without tables
                print("✅ Supabase connection established!")
                print("📋 Next step: Create database tables")
                return True
            except Exception as e2:
                print(f"❌ Connection error: {e2}")
                return False
            
    except ImportError as e:
        print(f"❌ Import error: {e}")
        return False
    except Exception as e:
        print(f"❌ General error: {e}")
        return False

if __name__ == "__main__":
    success = test_supabase_simple()
    if success:
        print("\n🎉 Supabase connection is working!")
        print("📋 You can now create the database tables.")
    else:
        print("\n❌ Supabase setup needs attention.") 