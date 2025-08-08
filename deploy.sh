#!/bin/bash

echo "🚀 Coffee Investment Tracker - Deployment Helper"
echo "================================================"
echo ""

# Check if git is initialized
if [ ! -d ".git" ]; then
    echo "❌ Git repository not found!"
    echo "Please initialize git and push your code to GitHub first:"
    echo "  git init"
    echo "  git add ."
    echo "  git commit -m 'Initial commit'"
    echo "  git remote add origin https://github.com/yourusername/your-repo-name.git"
    echo "  git push -u origin main"
    echo ""
    exit 1
fi

echo "✅ Git repository found"
echo ""

# Check if backend files exist
if [ -f "backend/app.py" ]; then
    echo "✅ Backend files found"
else
    echo "❌ Backend files not found in backend/ directory"
    exit 1
fi

# Check if frontend files exist
if [ -f "frontend/package.json" ]; then
    echo "✅ Frontend files found"
else
    echo "❌ Frontend files not found in frontend/ directory"
    exit 1
fi

echo ""
echo "📋 Deployment Checklist:"
echo "========================"
echo ""
echo "1. ✅ Code is in GitHub repository"
echo "2. ✅ Backend files present"
echo "3. ✅ Frontend files present"
echo ""
echo "🔧 Next Steps:"
echo "=============="
echo ""
echo "1. Deploy Backend (Railway):"
echo "   - Go to https://railway.app"
echo "   - Sign up with GitHub"
echo "   - Click 'New Project' → 'Deploy from GitHub repo'"
echo "   - Select your repository"
echo "   - Set environment variables:"
echo "     DATABASE_URL=your_supabase_connection_string"
echo "     SECRET_KEY=your_secret_key_here"
echo "     ALGORITHM=HS256"
echo "     ACCESS_TOKEN_EXPIRE_MINUTES=30"
echo ""
echo "2. Deploy Frontend (Vercel):"
echo "   - Go to https://vercel.com"
echo "   - Sign up with GitHub"
echo "   - Click 'New Project' → Import your repository"
echo "   - Set root directory to 'frontend'"
echo "   - Add environment variables (see DEPLOYMENT.md)"
echo ""
echo "3. Update CORS settings in backend/app.py if needed"
echo ""
echo "📖 For detailed instructions, see DEPLOYMENT.md"
echo ""
echo "🎉 Your app will be live once both deployments are complete!"
