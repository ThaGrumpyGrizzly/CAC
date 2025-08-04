<<<<<<< HEAD
# Using ngrok to Access Your App from Anywhere

## Step 1: Install ngrok
1. Go to https://ngrok.com/
2. Sign up for a free account
3. Download ngrok for Windows
4. Extract and add to your PATH

## Step 2: Start your app
```bash
# Terminal 1: Start backend
cd backend
python app.py

# Terminal 2: Start frontend  
cd frontend
npm run dev
```

## Step 3: Create ngrok tunnel
```bash
# Terminal 3: Create tunnel to frontend
ngrok http 3000

# Or tunnel to backend directly
ngrok http 8000
```

## Step 4: Access from anywhere
- ngrok will give you a public URL like: `https://abc123.ngrok.io`
- Share this URL with anyone to access your app
- Works on any device with internet connection

## Note: 
- Free ngrok has limitations (connections per minute)
- URL changes each time you restart ngrok
=======
# Using ngrok to Access Your App from Anywhere

## Step 1: Install ngrok
1. Go to https://ngrok.com/
2. Sign up for a free account
3. Download ngrok for Windows
4. Extract and add to your PATH

## Step 2: Start your app
```bash
# Terminal 1: Start backend
cd backend
python app.py

# Terminal 2: Start frontend  
cd frontend
npm run dev
```

## Step 3: Create ngrok tunnel
```bash
# Terminal 3: Create tunnel to frontend
ngrok http 3000

# Or tunnel to backend directly
ngrok http 8000
```

## Step 4: Access from anywhere
- ngrok will give you a public URL like: `https://abc123.ngrok.io`
- Share this URL with anyone to access your app
- Works on any device with internet connection

## Note: 
- Free ngrok has limitations (connections per minute)
- URL changes each time you restart ngrok
>>>>>>> 6217901f54d4a616e11e547dcf1f9cf5faa65607
- Good for testing, not for permanent deployment 