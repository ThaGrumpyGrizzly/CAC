# Supabase Setup Guide

## Step 1: Get Your Supabase Credentials

1. Go to your Supabase project dashboard
2. Navigate to **Settings** → **API**
3. Copy these values:

### Project URL
```
https://oflxtydqaavlbvraqlur.supabase.co
```

### Anon Public Key
```
eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6Im9mbHh0eWRxYWF2bGJ2cmFxbHVyIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NTQ2NjMwMzgsImV4cCI6MjA3MDIzOTAzOH0._SEbj9WZWTZQ4LGBDNRfqvEpnUyRAbhC7GsDjdhoOWk
```

### Service Role Key
```
eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.your_service_role_key_here
```

## Step 2: Backend Configuration

Create a file `backend/.env` with:

```env
# Database Configuration
DATABASE_URL=sqlite:///./investment_tracker.db

# Supabase Configuration
SUPABASE_URL=https://your-project-id.supabase.co
SUPABASE_ANON_KEY=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.your_anon_key_here
SUPABASE_SERVICE_ROLE_KEY=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.your_service_role_key_here

# JWT Configuration
SECRET_KEY=your_secret_key_here_make_it_long_and_random
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30

# Stock Price API
YAHOO_FINANCE_API_URL=https://query1.finance.yahoo.com/v8/finance/chart/
```

## Step 3: Frontend Configuration

Create a file `frontend/.env` with:

```env
# Backend API URL
VITE_API_BASE_URL=http://localhost:8000

# Supabase Configuration
VITE_SUPABASE_URL=https://your-project-id.supabase.co
VITE_SUPABASE_ANON_KEY=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.your_anon_key_here

# Firebase Configuration
VITE_FIREBASE_API_KEY=your_firebase_api_key_here
VITE_FIREBASE_AUTH_DOMAIN=your_project.firebaseapp.com
VITE_FIREBASE_PROJECT_ID=your_project_id
VITE_FIREBASE_STORAGE_BUCKET=your_project.appspot.com
VITE_FIREBASE_MESSAGING_SENDER_ID=your_messaging_sender_id
VITE_FIREBASE_APP_ID=your_app_id
```

## Step 4: Replace Placeholder Values

Replace these placeholders with your actual values:

- `your-project-id` → Your actual Supabase project ID
- `your_anon_key_here` → Your actual anon public key
- `your_service_role_key_here` → Your actual service role key
- `your_secret_key_here` → A long random string for JWT signing

## Step 5: Test Configuration

After setting up the environment files, test your configuration:

```bash
# Backend
cd backend
py start.py

# Frontend
cd frontend
npm run dev
```

## Security Notes

- ✅ **Never commit `.env` files** to Git
- ✅ **Use different keys** for development and production
- ✅ **Keep service role key secret** - it has admin privileges
- ✅ **Anon key is safe** to use in frontend code 