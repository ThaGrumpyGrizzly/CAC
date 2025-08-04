#!/bin/bash

echo "🚀 Investment Tracker Deployment Script"
echo "======================================"

# Check if git is initialized
if [ ! -d ".git" ]; then
    echo "📁 Initializing git repository..."
    git init
    git add .
    git commit -m "Initial commit - Investment Tracker App"
    echo "✅ Git repository initialized"
    echo ""
    echo "⚠️  IMPORTANT: You need to create a GitHub repository and connect it:"
    echo "1. Go to https://github.com/new"
    echo "2. Create a new repository"
    echo "3. Run: git remote add origin https://github.com/YOUR_USERNAME/YOUR_REPO_NAME.git"
    echo "4. Run: git push -u origin main"
    echo ""
else
    echo "📝 Committing latest changes..."
    git add .
    git commit -m "Update: Prepare for cloud deployment"
    echo "✅ Changes committed"
    echo ""
    echo "📤 Pushing to GitHub..."
    git push
    echo "✅ Code pushed to GitHub"
    echo ""
fi

echo "🎯 Next Steps:"
echo "1. Deploy backend to Railway: https://railway.app/"
echo "2. Deploy frontend to Vercel: https://vercel.com/"
echo "3. Connect them using the guide in DEPLOYMENT.md"
echo ""
echo "📖 See DEPLOYMENT.md for detailed instructions" 