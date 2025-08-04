#!/usr/bin/env python3
"""
Startup script for the Investment Tracker backend
"""

import os
import sys
import subprocess
from pathlib import Path

def check_python_version():
    """Check if Python version is compatible"""
    if sys.version_info < (3, 8):
        print("❌ Python 3.8 or higher is required")
        sys.exit(1)
    print(f"✅ Python {sys.version_info.major}.{sys.version_info.minor} detected")
    
    # Check if we can import required modules
    try:
        import subprocess
        result = subprocess.run(['py', '--version'], capture_output=True, text=True)
        if result.returncode == 0:
            print(f"✅ Python launcher available: {result.stdout.strip()}")
        else:
            print("⚠️  Python launcher not available, using sys.executable")
    except Exception as e:
        print(f"⚠️  Could not check Python launcher: {e}")

def check_dependencies():
    """Check if required dependencies are installed"""
    try:
        import fastapi
        import uvicorn
        import sqlalchemy
        import requests
        import pydantic
        print("✅ All required dependencies are installed")
        return True
    except ImportError as e:
        print(f"❌ Missing dependency: {e}")
        print("Please run: pip install -r backend/requirements.txt")
        return False

def setup_environment():
    """Set up environment variables"""
    if not os.path.exists('.env'):
        if os.path.exists('env.example'):
            print("📝 Creating .env file from template...")
            with open('env.example', 'r') as f:
                content = f.read()
            with open('.env', 'w') as f:
                f.write(content)
            print("✅ .env file created. Please edit it with your database settings.")
        else:
            print("⚠️  No .env file found. Please create one with your database settings.")
    
    # Set default environment variables
    os.environ.setdefault('USE_SQLITE', 'true')
    os.environ.setdefault('API_HOST', '0.0.0.0')
    os.environ.setdefault('API_PORT', '8000')

def initialize_database():
    """Initialize the database"""
    try:
        print("🗄️  Initializing database...")
        from backend.database import create_tables
        create_tables()
        print("✅ Database initialized successfully")
        return True
    except Exception as e:
        print(f"❌ Failed to initialize database: {e}")
        return False

def start_server():
    """Start the FastAPI server"""
    try:
        print("🚀 Starting Investment Tracker API server...")
        print("📍 API will be available at: http://localhost:8000")
        print("📖 API documentation at: http://localhost:8000/docs")
        print("🛑 Press Ctrl+C to stop the server")
        print("-" * 50)
        
        # Change to backend directory and start server
        os.chdir('backend')
        subprocess.run([
            'py', '-m', 'uvicorn', 
            'app:app', 
            '--host', '0.0.0.0', 
            '--port', '8000',
            '--reload'
        ])
    except KeyboardInterrupt:
        print("\n👋 Server stopped by user")
    except Exception as e:
        print(f"❌ Failed to start server: {e}")

def main():
    """Main startup function"""
    print("🎯 Investment Tracker Backend Startup")
    print("=" * 40)
    
    # Check Python version
    check_python_version()
    
    # Check dependencies
    if not check_dependencies():
        sys.exit(1)
    
    # Setup environment
    setup_environment()
    
    # Initialize database
    if not initialize_database():
        sys.exit(1)
    
    # Start server
    start_server()

if __name__ == "__main__":
    main() 