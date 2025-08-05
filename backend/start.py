import uvicorn
import os
import sys
from database import create_tables

if __name__ == "__main__":
    try:
        print("Starting Investment Tracker API...")
        print(f"Python version: {sys.version}")
        print(f"Current working directory: {os.getcwd()}")
        print(f"Environment variables:")
        print(f"  PORT: {os.environ.get('PORT', 'Not set')}")
        print(f"  DATABASE_URL: {'Set' if os.environ.get('DATABASE_URL') else 'Not set'}")
        
        # Initialize database tables (but don't fail if it doesn't work)
        try:
            print("Initializing database tables...")
            create_tables()
            print("Database tables initialized!")
        except Exception as db_error:
            print(f"Warning: Database initialization failed: {db_error}")
            print("Continuing without database initialization...")
        
        port = int(os.environ.get("PORT", 8000))
        print(f"Starting server on port {port}")
        
        uvicorn.run(
            "app:app", 
            host="0.0.0.0", 
            port=port, 
            reload=False,
            log_level="info"
        )
    except Exception as e:
        print(f"Error starting server: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1) 