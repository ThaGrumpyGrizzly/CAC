# Investment Tracker - Cloud Deployment Guide

This guide will help you deploy your investment tracking app to the cloud so you can access it from any device.

## Prerequisites

1. **GitHub Account** - Your code needs to be on GitHub
2. **Railway Account** - For backend hosting (free tier available)
3. **Vercel Account** - For frontend hosting (free tier available)

## Step 1: Push Code to GitHub

If your code isn't already on GitHub:

```bash
# Initialize git repository (if not already done)
git init
git add .
git commit -m "Initial commit"

# Create a new repository on GitHub, then:
git remote add origin https://github.com/YOUR_USERNAME/YOUR_REPO_NAME.git
git push -u origin main
```

## Step 2: Deploy Backend to Railway

1. **Go to [Railway.app](https://railway.app/)**
2. **Sign up with GitHub**
3. **Click "New Project"**
4. **Select "Deploy from GitHub repo"**
5. **Choose your repository**
6. **Railway will automatically detect the configuration and deploy**

### Railway Configuration
- Uses `railway.json` for deployment settings
- Uses `requirements.txt` for Python dependencies
- Health check endpoint: `/health`
- Auto-deploys when you push to GitHub

## Step 3: Deploy Frontend to Vercel

1. **Go to [Vercel.com](https://vercel.com/)**
2. **Sign up with GitHub**
3. **Click "New Project"**
4. **Import your GitHub repository**
5. **Configure build settings:**
   - Framework Preset: Vite
   - Build Command: `npm run build`
   - Output Directory: `dist`
   - Install Command: `npm install`

## Step 4: Connect Frontend to Backend

1. **Get your Railway backend URL** (e.g., `https://your-app.railway.app`)
2. **In Vercel project settings:**
   - Go to Settings → Environment Variables
   - Add variable: `VITE_API_BASE_URL`
   - Set value to your Railway URL
   - Redeploy the project

## Step 5: Test Your Deployment

1. **Visit your Vercel URL** (e.g., `https://your-app.vercel.app`)
2. **Test adding an investment**
3. **Test viewing your portfolio**
4. **Access from your phone** using the same URL

## Environment Variables

### Backend (Railway)
- `PORT` - Automatically set by Railway
- `DATABASE_URL` - Automatically set by Railway

### Frontend (Vercel)
- `VITE_API_BASE_URL` - Your Railway backend URL

## Troubleshooting

### Backend Issues
- Check Railway logs for errors
- Verify `requirements.txt` has all dependencies
- Ensure health check endpoint `/health` is working

### Frontend Issues
- Check Vercel build logs
- Verify environment variable is set correctly
- Check browser console for API errors

### CORS Issues
- Backend is configured to allow Vercel domains
- If using custom domain, add it to CORS origins

## Security Notes

✅ **HTTPS enabled** by default  
✅ **CORS properly configured**  
✅ **Environment variables** for sensitive data  
✅ **Professional hosting** with security updates  

## Cost

- **Railway**: Free tier includes 500 hours/month
- **Vercel**: Free tier includes unlimited deployments
- **Total cost**: $0/month for personal use

## Access Your App

Once deployed, you can access your investment tracker from:
- 📱 **Your phone** - Just open the Vercel URL in your browser
- 💻 **Any computer** - No need to install anything
- 🌍 **Anywhere** - Works from any location with internet

Your app will be available 24/7 without needing your computer to be running! 