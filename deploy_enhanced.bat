@echo off
echo ========================================
echo   🚀 DEPLOYING ENHANCED PR DASHBOARD
echo ========================================
echo.

:: Change to deployment directory
cd "C:\Users\FElmasri\Desktop\github-pr-analytics\deployment"

:: Check if we're in the right directory
if not exist "index.html" (
    echo ❌ Error: index.html not found in deployment directory
    echo Please ensure you're in the correct folder
    pause
    exit /b 1
)

echo ✅ Found index.html with enhanced visualizations
echo.

:: Check if Firebase is installed
firebase --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ❌ Firebase CLI not found. Installing...
    npm install -g firebase-tools
    if %errorlevel% neq 0 (
        echo ❌ Failed to install Firebase CLI
        echo Please install Node.js first from https://nodejs.org
        pause
        exit /b 1
    )
)

echo ✅ Firebase CLI is ready
echo.

:: Check if user is logged in to Firebase
echo 🔐 Checking Firebase authentication...
firebase projects:list >nul 2>&1
if %errorlevel% neq 0 (
    echo ❌ Not logged in to Firebase. Please login first:
    echo Run: firebase login
    pause
    exit /b 1
)

echo ✅ Firebase authentication verified
echo.

:: Check if Firebase project is initialized
if not exist "firebase.json" (
    echo ⚠️  Firebase project not initialized in this directory
    echo.
    echo Please run the following commands:
    echo 1. firebase init hosting
    echo 2. Select existing project or create new one
    echo 3. Use "." as public directory
    echo 4. Answer "N" to single-page app
    echo 5. Answer "N" to GitHub setup
    echo 6. Answer "N" to overwrite index.html
    echo.
    echo After initialization, run this script again.
    pause
    exit /b 1
)

echo ✅ Firebase project initialized
echo.

:: Display current enhancements
echo 📊 ENHANCED DASHBOARD FEATURES:
echo   ✅ Fixed chart container sizing
echo   ✅ Proper x-axis label visibility
echo   ✅ Centered donut chart display
echo   ✅ Improved responsive design
echo   ✅ Better chart padding and margins
echo   ✅ Enhanced mobile compatibility
echo.

:: Deploy to Firebase
echo 🚀 Deploying enhanced dashboard...
echo.
firebase deploy --only hosting

if %errorlevel% eq 0 (
    echo.
    echo ========================================
    echo   ✅ DEPLOYMENT SUCCESSFUL!
    echo ========================================
    echo.
    echo Your enhanced dashboard is now live!
    echo.
    echo 🌟 NEW VISUALIZATION IMPROVEMENTS:
    echo   • Charts now fit properly in containers
    echo   • X-axis labels are fully visible
    echo   • Donut chart is properly centered
    echo   • Better spacing and padding
    echo   • Improved mobile responsiveness
    echo.
    echo 📱 Access your dashboard at:
    firebase hosting:channel:list
    echo.
    echo Share this URL with your team!
    echo.
) else (
    echo.
    echo ❌ Deployment failed!
    echo Please check the error messages above.
    echo.
)

pause