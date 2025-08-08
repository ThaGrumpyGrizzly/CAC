# Coffee Investment Tracker - Render Deployment Guide

This guide will help you deploy your Coffee investment tracking application on Render.

## 🚀 Quick Start (Recommended)

### Step 1: Prepare Your Code

1. **Commit your changes:**
   ```bash
   git add .
   git commit -m "Add Render deployment configuration"
   git push
   ```

### Step 2: Deploy on Render

1. **Sign up for Render**
   - Go to [render.com](https://render.com)
   - Sign up with your GitHub account

2. **Deploy Both Services**
   - Click "New" → "Blueprint"
   - Connect your GitHub repository
   - Render will automatically detect the `render.yaml` file
   - Click "Apply" to deploy both services

3. **Configure Environment Variables**
   - After deployment, go to each service dashboard
   - Update the environment variables with your actual values

## 🔧 Environment Variables Setup

### Backend Environment Variables
```bash
DATABASE_URL=postgresql://username:password@host:port/database
SECRET_KEY=your_secret_key_here_make_it_long_and_random
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
```

### Frontend Environment Variables
```bash
VITE_API_BASE_URL=https://your-backend-service.onrender.com
VITE_SUPABASE_URL=your_supabase_url
VITE_SUPABASE_ANON_KEY=your_supabase_anon_key
VITE_FIREBASE_API_KEY=your_firebase_api_key
VITE_FIREBASE_AUTH_DOMAIN=your_project.firebaseapp.com
VITE_FIREBASE_PROJECT_ID=your_project_id
VITE_FIREBASE_STORAGE_BUCKET=your_project.appspot.com
VITE_FIREBASE_MESSAGING_SENDER_ID=your_messaging_sender_id
VITE_FIREBASE_APP_ID=your_app_id
```

## 📋 Manual Deployment (Alternative)

If the Blueprint doesn't work, deploy services manually:

### Backend Service
1. Click "New" → "Web Service"
2. Connect your GitHub repository
3. Set build command: `pip install -r backend/requirements.txt`
4. Set start command: `cd backend && uvicorn app:app --host 0.0.0.0 --port $PORT`
5. Add environment variables (see above)

### Frontend Service
1. Click "New" → "Static Site"
2. Connect your GitHub repository
3. Set build command: `cd frontend && npm install && npm run build`
4. Set publish directory: `frontend/dist`
5. Add environment variables (see above)

## 🔍 Getting Your Environment Variables

### Supabase Connection String
1. Go to your Supabase dashboard
2. Click "Settings" → "Database"
3. Copy the "Connection string" (URI format)
4. Replace `[YOUR-PASSWORD]` with your database password

### Generate Secret Key
```bash
# Run this in your terminal to generate a secure secret key
python -c "import secrets; print(secrets.token_urlsafe(32))"
```

### Firebase Configuration
1. Go to your Firebase console
2. Click "Project settings" → "General"
3. Scroll down to "Your apps" section
4. Copy the configuration values

## ✅ Post-Deployment Checklist

1. **Test Backend Health**
   - Visit: `https://your-backend-service.onrender.com/health`
   - Should return healthy status

2. **Test Frontend**
   - Visit your frontend URL
   - Test login/register functionality
   - Test investment tracking features

3. **Update CORS Settings**
   - If you get CORS errors, update `backend/app.py`
   - Add your frontend URL to `allow_origins`

4. **Database Migration**
   - Ensure your Supabase database is properly set up
   - Run any necessary migrations

## 🐛 Troubleshooting

### Common Issues

1. **Build Failures**
   - Check that all dependencies are in `requirements.txt`
   - Ensure Python version is compatible (3.11+)

2. **CORS Errors**
   - Update `allow_origins` in `backend/app.py`
   - Add your frontend URL to the list

3. **Database Connection Issues**
   - Check your `DATABASE_URL` environment variable
   - Ensure Supabase is properly configured

4. **Environment Variables**
   - Double-check all environment variables are set correctly
   - Ensure no typos in variable names

## 💰 Cost

- **Render**: Free tier (750 hours/month for each service)
- **Supabase**: Free tier (500MB database, 50MB file storage)
- **Firebase**: Free tier (10GB storage, 50,000 reads/day)

## 🎉 Success!

Your application will be accessible at:
- Frontend: `https://your-frontend-service.onrender.com`
- Backend: `https://your-backend-service.onrender.com`

Both services will be on the same platform, making it easy to manage!
