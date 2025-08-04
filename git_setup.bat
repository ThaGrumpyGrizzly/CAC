@echo off
echo Setting up Git repository and pushing to GitHub...
echo.

REM Initialize git repository
git init

REM Add all files
git add .

REM Set user identity (replace with your details)
git config --global user.name "Your Name"
git config --global user.email "your.email@example.com"

REM Make first commit
git commit -m "Initial commit - Investment Tracker App"

echo.
echo ✅ Git repository initialized and files committed!
echo.
echo 📝 Next steps:
echo 1. Go to https://github.com/new
echo 2. Create a new repository (make it PUBLIC)
echo 3. Copy the repository URL
echo 4. Run: git remote add origin YOUR_REPOSITORY_URL
echo 5. Run: git push -u origin main
echo.
pause 