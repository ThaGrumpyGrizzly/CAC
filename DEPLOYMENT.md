# Coffee Investment Tracker - Deployment Guide

This guide will help you deploy your Coffee investment tracking application online.

## Prerequisites

1. **GitHub Account** - Your code should be in a GitHub repository
2. **Supabase Account** - For database (you already have this)
3. **Firebase Account** - For authentication (you already have this)

## Option 1: Vercel + Railway (Recommended)

### Backend Deployment (Railway)

1. **Sign up for Railway**
   - Go to [railway.app](https://railway.app)
   - Sign up with your GitHub account

2. **Deploy Backend**
   - Click "New Project" → "Deploy from GitHub repo"
   - Select your Coffee repository
   - Railway will automatically detect it's a Python app
   - Set the following environment variables in Railway dashboard:
     ```
     DATABASE_URL=your_supabase_connection_string
     SECRET_KEY=your_secret_key_here
     ALGORITHM=HS256
     ACCESS_TOKEN_EXPIRE_MINUTES=30
     ```

3. **Get Backend URL**
   - Railway will provide a URL like: `https://your-app-name.railway.app`
   - Note this URL for frontend configuration

### Frontend Deployment (Vercel)

1. **Sign up for Vercel**
   - Go to [vercel.com](https://vercel.com)
   - Sign up with your GitHub account

2. **Deploy Frontend**
   - Click "New Project" → Import your GitHub repository
   - Set the root directory to `frontend`
   - Add the following environment variables:
     ```
     VITE_API_BASE_URL=https://your-backend-url.railway.app
     VITE_SUPABASE_URL=your_supabase_url
     VITE_SUPABASE_ANON_KEY=your_supabase_anon_key
     VITE_FIREBASE_API_KEY=your_firebase_api_key
     VITE_FIREBASE_AUTH_DOMAIN=your_project.firebaseapp.com
     VITE_FIREBASE_PROJECT_ID=your_project_id
     VITE_FIREBASE_STORAGE_BUCKET=your_project.appspot.com
     VITE_FIREBASE_MESSAGING_SENDER_ID=your_messaging_sender_id
     VITE_FIREBASE_APP_ID=your_app_id
     ```

3. **Deploy**
   - Vercel will automatically build and deploy your frontend
   - You'll get a URL like: `https://your-app-name.vercel.app`

## Option 2: Render (Alternative)

### Backend on Render

1. **Sign up for Render**
   - Go to [render.com](https://render.com)
   - Sign up with your GitHub account

2. **Deploy Backend**
   - Click "New" → "Web Service"
   - Connect your GitHub repository
   - Set build command: `pip install -r requirements.txt`
   - Set start command: `uvicorn app:app --host 0.0.0.0 --port $PORT`
   - Add environment variables (same as Railway)

### Frontend on Vercel
- Same as above

## Option 3: Netlify (Alternative Frontend)

1. **Sign up for Netlify**
   - Go to [netlify.com](https://netlify.com)
   - Sign up with your GitHub account

2. **Deploy Frontend**
   - Click "New site from Git"
   - Connect your repository
   - Set build command: `cd frontend && npm run build`
   - Set publish directory: `frontend/dist`
   - Add environment variables (same as Vercel)

## Environment Variables Setup

### Backend Environment Variables
```bash
DATABASE_URL=postgresql://username:password@host:port/database
SECRET_KEY=your_secret_key_here
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
```

### Frontend Environment Variables
```bash
VITE_API_BASE_URL=https://your-backend-url.com
VITE_SUPABASE_URL=your_supabase_url
VITE_SUPABASE_ANON_KEY=your_supabase_anon_key
VITE_FIREBASE_API_KEY=your_firebase_api_key
VITE_FIREBASE_AUTH_DOMAIN=your_project.firebaseapp.com
VITE_FIREBASE_PROJECT_ID=your_project_id
VITE_FIREBASE_STORAGE_BUCKET=your_project.appspot.com
VITE_FIREBASE_MESSAGING_SENDER_ID=your_messaging_sender_id
VITE_FIREBASE_APP_ID=your_app_id
```

## Post-Deployment Checklist

1. **Test Backend Health**
   - Visit: `https://your-backend-url.com/health`
   - Should return healthy status

2. **Test Frontend**
   - Visit your frontend URL
   - Test login/register functionality
   - Test investment tracking features

3. **Update CORS Settings**
   - If you get CORS errors, update the `allow_origins` in `backend/app.py`
   - Add your frontend URL to the allowed origins

4. **Database Migration**
   - Ensure your Supabase database is properly set up
   - Run any necessary migrations

## Troubleshooting

### Common Issues

1. **CORS Errors**
   - Update `allow_origins` in `backend/app.py`
   - Add your frontend URL to the list

2. **Database Connection Issues**
   - Check your `DATABASE_URL` environment variable
   - Ensure Supabase is properly configured

3. **Build Failures**
   - Check that all dependencies are in `requirements.txt`
   - Ensure Python version is compatible

4. **Environment Variables**
   - Double-check all environment variables are set correctly
   - Ensure no typos in variable names

## Cost Estimation

- **Vercel**: Free tier (100GB bandwidth/month)
- **Railway**: Free tier (500 hours/month)
- **Supabase**: Free tier (500MB database, 50MB file storage)
- **Firebase**: Free tier (10GB storage, 50,000 reads/day)

## Next Steps

1. Deploy using one of the options above
2. Test all functionality
3. Set up custom domain (optional)
4. Configure monitoring and analytics
5. Set up automatic deployments

Your application should now be live and accessible online!
