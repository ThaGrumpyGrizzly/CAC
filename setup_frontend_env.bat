@echo off
echo Setting up frontend environment...
echo.

echo Please enter your Railway backend URL (e.g., https://your-app.railway.app):
set /p BACKEND_URL=

echo Creating .env file in frontend directory...
(
echo # API Configuration
echo VITE_API_BASE_URL=%BACKEND_URL%
echo.
echo # Note: This file was auto-generated. Update the URL above if needed.
) > frontend\.env

echo.
echo ✅ Frontend environment file created successfully!
echo 📁 Location: frontend\.env
echo 🔗 Backend URL: %BACKEND_URL%
echo.
echo Next steps:
echo 1. Restart your frontend development server
echo 2. Try logging in again
echo 3. Check browser console for any errors
echo.
pause 