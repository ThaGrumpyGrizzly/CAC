<<<<<<< HEAD
# Setting Up Your GitHub Repository

## Step 1: Install Git
1. Download Git from: https://git-scm.com/download/win
2. Install with default settings
3. Restart your terminal/PowerShell

## Step 2: Initialize Local Repository
Open PowerShell in your project folder and run:

```powershell
# Initialize git repository
git init

# Add all files
git add .

# Make first commit
git commit -m "Initial commit - Investment Tracker App"

# Set your Git identity (replace with your details)
git config --global user.name "Your Name"
git config --global user.email "your.email@example.com"
```

## Step 3: Create GitHub Repository
1. Go to https://github.com/new
2. Repository name: `investment-tracker` (or any name you prefer)
3. Make it **Public** (for free hosting)
4. **Don't** initialize with README (we already have files)
5. Click "Create repository"

## Step 4: Connect and Push
After creating the repository, GitHub will show you commands. Run these:

```powershell
# Add the remote repository (replace with your actual URL)
git remote add origin https://github.com/YOUR_USERNAME/YOUR_REPO_NAME.git

# Push to GitHub
git push -u origin main
```

## Step 5: Verify
1. Go to your GitHub repository URL
2. You should see all your files there
3. Now you're ready to deploy!

## Troubleshooting
- If you get authentication errors, you may need to set up a Personal Access Token
=======
# Setting Up Your GitHub Repository

## Step 1: Install Git
1. Download Git from: https://git-scm.com/download/win
2. Install with default settings
3. Restart your terminal/PowerShell

## Step 2: Initialize Local Repository
Open PowerShell in your project folder and run:

```powershell
# Initialize git repository
git init

# Add all files
git add .

# Make first commit
git commit -m "Initial commit - Investment Tracker App"

# Set your Git identity (replace with your details)
git config --global user.name "Your Name"
git config --global user.email "your.email@example.com"
```

## Step 3: Create GitHub Repository
1. Go to https://github.com/new
2. Repository name: `investment-tracker` (or any name you prefer)
3. Make it **Public** (for free hosting)
4. **Don't** initialize with README (we already have files)
5. Click "Create repository"

## Step 4: Connect and Push
After creating the repository, GitHub will show you commands. Run these:

```powershell
# Add the remote repository (replace with your actual URL)
git remote add origin https://github.com/YOUR_USERNAME/YOUR_REPO_NAME.git

# Push to GitHub
git push -u origin main
```

## Step 5: Verify
1. Go to your GitHub repository URL
2. You should see all your files there
3. Now you're ready to deploy!

## Troubleshooting
- If you get authentication errors, you may need to set up a Personal Access Token
>>>>>>> 6217901f54d4a616e11e547dcf1f9cf5faa65607
- If the branch is called "master" instead of "main", use: `git push -u origin master` 