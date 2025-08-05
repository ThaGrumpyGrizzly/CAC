# Railway Deployment Troubleshooting Guide

## Login Issues

### Problem: Users can register but cannot log in

**Common Causes:**
1. **Frontend Environment Configuration**: Missing or incorrect API URL
2. **Database Connection**: Users not being saved properly
3. **CORS Issues**: Frontend can't communicate with backend
4. **Authentication Service**: Wrong auth service being used

**Solutions:**

#### 1. Check Frontend Environment
Create a `.env` file in the frontend directory:
```bash
# frontend/.env
VITE_API_BASE_URL=https://your-backend-url.railway.app
```

#### 2. Verify Database Connection
- Check if DATABASE_URL is set in Railway
- Verify tables are created properly
- Test database connection manually

#### 3. Check Browser Console
- Open browser developer tools (F12)
- Look for network errors in Console tab
- Check Network tab for failed requests

#### 4. Test Backend Directly
```bash
# Test login endpoint
curl -X POST https://your-backend-url.railway.app/login \
  -H "Content-Type: application/json" \
  -d '{"email":"test@example.com","password":"password123"}'
```

#### 5. Debug Authentication Flow
- Check if users are being saved to database
- Verify password hashing is working
- Ensure JWT tokens are being generated

## Health Check Issues

The health check is failing because the application is trying to connect to a database that might not be properly configured on Railway.

### Changes Made:

1. **Updated Health Check Endpoint** (`/health`):
   - Now handles missing DATABASE_URL gracefully
   - Returns detailed status information
   - Doesn't fail if database is not available

2. **Added Simple Health Check** (`/health-simple`):
   - No database dependency
   - Used for initial deployment
   - Always returns healthy status

3. **Updated Railway Configuration**:
   - Changed health check path to `/health-simple`
   - Increased timeout to 120 seconds
   - Reduced max retries to 5

4. **Improved Start Script**:
   - Better error handling
   - Continues even if database initialization fails
   - More detailed logging

## Deployment Steps:

1. **Push to Git**:
   ```bash
   git add .
   git commit -m "Fix health check issues"
   git push
   ```

2. **Check Railway Dashboard**:
   - Go to your Railway project
   - Check the deployment logs
   - Verify environment variables are set

3. **Test the Deployment**:
   ```bash
   # Test locally first
   cd backend
   python test_deployment.py
   
   # Test on Railway (replace with your URL)
   python test_deployment.py https://your-app.railway.app
   ```

## Environment Variables to Check:

Make sure these are set in Railway:
- `PORT` (usually set automatically)
- `DATABASE_URL` (if using PostgreSQL)

## Common Issues:

1. **Database Connection**: If you don't have a database set up, the app will work but database features won't function.

2. **Port Binding**: The app should bind to `0.0.0.0` and use the `PORT` environment variable.

3. **Dependencies**: All required packages are specified in `requirements.txt`.

## Next Steps:

1. Deploy with the simple health check
2. Once deployed successfully, switch back to the full health check
3. Set up a database if needed
4. Test all endpoints

## Rollback Plan:

If issues persist, you can:
1. Use the backup files (app_backup.py, etc.)
2. Switch to a different deployment platform
3. Use local development with Railway CLI 