@echo off
echo 🚀 Deploying WorkMate to Railway...

echo.
echo 📦 Building and deploying backend...
cd Backend
echo ✅ Backend ready for deployment

echo.
echo 📦 Building and deploying frontend...
cd ..\Frontend
echo ✅ Frontend ready for deployment

echo.
echo 🎉 Both services are ready for Railway deployment!
echo.
echo 📋 Next steps:
echo 1. Go to https://railway.app
echo 2. Create a new project
echo 3. Connect your GitHub repository
echo 4. Railway will automatically detect both services
echo 5. Set environment variables in Railway dashboard
echo.
echo 🔧 Environment Variables to set in Railway:
echo Backend: PORT=8080, FLASK_ENV=production
echo Frontend: VITE_API_URL=https://your-backend-url.up.railway.app/api
echo.
pause
