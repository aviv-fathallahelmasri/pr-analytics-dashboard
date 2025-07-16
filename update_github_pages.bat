@echo off
echo ==========================================
echo   🚀 UPDATING GITHUB PAGES DASHBOARD
echo ==========================================
echo.

echo Target: https://aviv-fathallahelmasri.github.io/pr-analytics-dashboard/
echo.

echo 📊 ENHANCED VISUALIZATIONS READY:
echo   ✅ Fixed chart container sizing
echo   ✅ Visible x-axis labels
echo   ✅ Centered donut chart
echo   ✅ Improved mobile responsiveness
echo   ✅ Professional spacing and padding
echo.

REM Check if enhanced file exists
set "ENHANCED_FILE=C:\Users\FElmasri\Desktop\github-pr-analytics\deployment\index.html"
if not exist "%ENHANCED_FILE%" (
    echo ❌ Enhanced dashboard file not found at: %ENHANCED_FILE%
    echo Please ensure the file exists and try again.
    pause
    exit /b 1
)

echo ✅ Enhanced dashboard file found
echo.

REM Check if repository already exists in current directory
if exist "pr-analytics-dashboard" (
    echo ✅ Repository already exists locally
    set "REPO_PATH=pr-analytics-dashboard"
    goto :copy_file
)

REM Prompt for repository path
echo Choose an option:
echo 1. Clone repository automatically
echo 2. Enter path to existing repository
echo.
set /p "choice=Enter your choice (1 or 2): "

if "%choice%"=="1" (
    set "REPO_PATH=pr-analytics-dashboard"
    echo 📁 Cloning repository to: %REPO_PATH%
    git clone https://github.com/aviv-fathallahelmasri/pr-analytics-dashboard.git "%REPO_PATH%"
    if %errorlevel% neq 0 (
        echo ❌ Failed to clone repository
        echo Please check:
        echo   - You have access to the repository
        echo   - Git is installed and configured
        echo   - Internet connection is working
        pause
        exit /b 1
    )
    echo ✅ Repository cloned successfully
) else if "%choice%"=="2" (
    set /p "REPO_PATH=Enter full path to your repository: "
    if "%REPO_PATH%"=="" (
        echo ❌ No path provided
        pause
        exit /b 1
    )
) else (
    echo ❌ Invalid choice
    pause
    exit /b 1
)

:copy_file
echo.

REM Check if repository directory exists
if not exist "%REPO_PATH%" (
    echo ❌ Repository directory not found: %REPO_PATH%
    echo Please check the path and try again.
    pause
    exit /b 1
)

echo ✅ Repository found: %REPO_PATH%
echo.

REM Copy enhanced file
echo 📋 Copying enhanced dashboard...
copy "%ENHANCED_FILE%" "%REPO_PATH%\index.html"
if %errorlevel% neq 0 (
    echo ❌ Failed to copy enhanced file
    pause
    exit /b 1
)

echo ✅ Enhanced dashboard copied successfully
echo.

REM Navigate to repository
cd "%REPO_PATH%"

REM Check git status
echo 🔍 Checking for changes...
git status --porcelain 2>nul | findstr index.html >nul
if %errorlevel% neq 0 (
    echo ℹ️  No changes detected in index.html
    echo The enhanced version might already be deployed.
    echo.
    echo Current repository status:
    git status
    echo.
    set /p "continue=Do you want to continue anyway? (y/n): "
    if /i not "%continue%"=="y" (
        echo Operation cancelled
        pause
        exit /b 0
    )
)

echo ✅ Proceeding with deployment
echo.

REM Add and commit changes
echo 🔄 Adding files to git...
git add index.html

echo 🔄 Committing enhanced dashboard...
git commit -m "🚀 Enhanced dashboard visualizations

- Fixed chart container sizing and overflow issues
- Made x-axis labels fully visible and readable
- Centered donut chart properly in container
- Improved mobile responsiveness across all devices
- Enhanced padding and spacing throughout dashboard
- Better Chart.js configuration for professional appearance
- Optimized for team collaboration and management reporting"

if %errorlevel% neq 0 (
    echo ⚠️  Commit failed - this might be because there are no changes
    echo Current git status:
    git status
    echo.
    set /p "continue=Do you want to try pushing anyway? (y/n): "
    if /i not "%continue%"=="y" (
        echo Operation cancelled
        pause
        exit /b 0
    )
)

echo ✅ Ready to push to GitHub
echo.

REM Push to GitHub
echo 🌐 Pushing to GitHub Pages...
git push origin main
if %errorlevel% neq 0 (
    echo ⚠️  Push to 'main' failed, trying 'master'...
    git push origin master
    if %errorlevel% neq 0 (
        echo ❌ Failed to push to GitHub
        echo.
        echo Git remote info:
        git remote -v
        echo.
        echo Current branch:
        git branch
        echo.
        echo Please check:
        echo   - You have push access to the repository
        echo   - You're authenticated with GitHub
        echo   - Your internet connection is stable
        echo.
        pause
        exit /b 1
    )
)

echo.
echo ==========================================
echo   ✅ DEPLOYMENT SUCCESSFUL!
echo ==========================================
echo.

echo 🌟 ENHANCED DASHBOARD DEPLOYED:
echo   • Charts now fit perfectly in containers
echo   • X-axis labels are fully visible
echo   • Donut chart is centered and properly sized
echo   • Excellent mobile responsiveness
echo   • Professional appearance throughout
echo.

echo 🌐 Your enhanced dashboard is now live at:
echo https://aviv-fathallahelmasri.github.io/pr-analytics-dashboard/
echo.

echo ⏰ Changes will be visible in 2-3 minutes
echo 🔄 Hard refresh (Ctrl+F5) if changes don't appear immediately
echo.

echo 🎉 Your team will now enjoy:
echo   • Better chart readability
echo   • Improved mobile experience
echo   • Professional data presentation
echo   • Enhanced decision-making capabilities
echo.

echo 📊 Daily automation at 8:00 AM Berlin time continues unchanged
echo 🔄 All future updates will preserve these enhancements
echo.

pause