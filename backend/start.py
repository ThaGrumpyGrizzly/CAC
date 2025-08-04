import uvicorn
import os
from database import create_tables

if __name__ == "__main__":
    # Initialize database tables
    create_tables()
    print("Database tables initialized!")
    
    port = int(os.environ.get("PORT", 8000))
    uvicorn.run("app:app", host="0.0.0.0", port=port, reload=False) 