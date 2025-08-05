import uvicorn
import os
import sys
from database import create_tables

if __name__ == "__main__":
    try:
        print("Starting Investment Tracker API...")
        print(f"Python version: {sys.version}")
        print(f"Current working directory: {os.getcwd()}")
        
        # Initialize database tables
        print("Initializing database tables...")
        create_tables()
        print("Database tables initialized!")
        
        port = int(os.environ.get("PORT", 8000))
        print(f"Starting server on port {port}")
        
        uvicorn.run("app:app", host="0.0.0.0", port=port, reload=False)
    except Exception as e:
        print(f"Error starting server: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1) 