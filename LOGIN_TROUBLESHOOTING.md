# Login Troubleshooting Guide

## Problem: Can register but cannot log in

You can create an account but when you try to log in with your email and password, nothing happens.

## Step-by-Step Debugging

### 1. Check Browser Console
1. Open your browser's developer tools (F12)
2. Go to the Console tab
3. Try to log in
4. Look for any error messages

**Common errors:**
- `CORS error`: Frontend can't reach backend
- `Network error`: Backend URL is wrong
- `401 Unauthorized`: Wrong credentials or authentication issue

### 2. Check Network Tab
1. In developer tools, go to Network tab
2. Try to log in
3. Look for the login request
4. Check if it's being sent to the correct URL

### 3. Verify Backend URL
The most common issue is that the frontend is trying to connect to `localhost:8000` instead of your Railway backend.

**Fix:**
1. Find your Railway backend URL (from Railway dashboard)
2. Create a `.env` file in the `frontend` directory:
   ```
   VITE_API_BASE_URL=https://your-app.railway.app
   ```
3. Restart your frontend development server

### 4. Test Backend Directly
Run the debug script to test your backend:

```bash
cd backend
python debug_login.py https://your-app.railway.app
```

This will:
- Test database connection
- Test user registration
- Test user login
- Show detailed error messages

### 5. Check Database
The issue might be that users aren't being saved properly:

```bash
cd backend
python -c "
from database import SessionLocal, UserDB
db = SessionLocal()
users = db.query(UserDB).all()
print(f'Found {len(users)} users:')
for user in users:
    print(f'- {user.email} ({user.username})')
db.close()
"
```

### 6. Test Authentication Manually
```bash
# Test registration
curl -X POST https://your-app.railway.app/register \
  -H "Content-Type: application/json" \
  -d '{"email":"test@example.com","username":"testuser","password":"testpass123"}'

# Test login
curl -X POST https://your-app.railway.app/login \
  -H "Content-Type: application/json" \
  -d '{"email":"test@example.com","password":"testpass123"}'
```

## Quick Fixes

### Fix 1: Environment Configuration
1. Run the setup script:
   ```bash
   setup_frontend_env.bat
   ```
2. Enter your Railway backend URL when prompted
3. Restart your frontend server

### Fix 2: Check Railway Environment Variables
1. Go to your Railway dashboard
2. Check if `DATABASE_URL` is set
3. If not, add it with your database connection string

### Fix 3: Restart Backend
1. Go to Railway dashboard
2. Restart your deployment
3. Wait for it to be healthy

## Common Issues and Solutions

### Issue: "Nothing happens when I click login"
**Cause:** Frontend is not connecting to backend
**Solution:** Check browser console for errors, verify backend URL

### Issue: "Invalid email or password"
**Cause:** User not in database or password hash mismatch
**Solution:** Check if user was actually saved, verify password hashing

### Issue: CORS errors
**Cause:** Backend not allowing frontend domain
**Solution:** Check CORS configuration in backend

### Issue: Network errors
**Cause:** Backend URL is wrong or backend is down
**Solution:** Verify backend URL and check if backend is running

## Getting Help

If you're still having issues:

1. Run the debug script and share the output
2. Check browser console and share any errors
3. Verify your Railway backend URL is correct
4. Make sure your backend is healthy in Railway dashboard

## Next Steps

Once login is working:
1. Test all other features
2. Set up proper environment variables
3. Consider using a more secure authentication method
4. Add proper error handling to frontend 