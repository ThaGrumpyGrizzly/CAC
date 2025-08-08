from fastapi import FastAPI, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from datetime import datetime
import os

app = FastAPI(title='Investment Tracker API', version='1.0.0')

# Add security
security = HTTPBearer()

# Add CORS middleware for frontend communication
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        'http://localhost:3000', 
        'http://localhost:5173',
        'https://*.vercel.app',
        'https://*.railway.app',
        'https://*.netlify.app',
        'https://*.onrender.com',
        '*',
    ],
    allow_credentials=True,
    allow_methods=['*'],
    allow_headers=['*'],
)

@app.get('/')
def read_root():
    return {'status': 'Investment Tracker API running', 'version': '1.0.0'}

@app.get('/health-simple')
def simple_health_check():
    """Simple health check that doesn't require database connection"""
    return {
        'status': 'healthy',
        'service': 'Investment Tracker API',
        'message': 'Service is running',
        'timestamp': datetime.utcnow().isoformat()
    }

@app.get('/health')
def health_check():
    try:
        # Basic service health check
        service_status = 'healthy'
        database_status = 'not_configured'
        
        return {
            'status': service_status,
            'service': 'Investment Tracker API',
            'database': database_status,
            'timestamp': datetime.utcnow().isoformat(),
        }
    except Exception as e:
        return {
            'status': 'unhealthy',
            'service': 'Investment Tracker API',
            'error': str(e),
            'timestamp': datetime.utcnow().isoformat()
        }

@app.get('/test')
def test_endpoint():
    return {'message': 'Backend is working!'}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
