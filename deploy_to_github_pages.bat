@echo off
echo ========================================
echo   🚀 DEPLOY ENHANCED DASHBOARD TO GITHUB PAGES
echo ========================================
echo.

echo Your enhanced dashboard will be deployed to:
echo https://aviv-fathallahelmasri.github.io/pr-analytics-dashboard/
echo.

echo ✅ VISUALIZATION IMPROVEMENTS READY:
echo   • Fixed chart container sizing
echo   • Visible x-axis labels
echo   • Centered donut chart
echo   • Better responsive design
echo   • Professional spacing and padding
echo.

set /p "repo_path=Enter the path to your pr-analytics-dashboard repository: "

if not exist "%repo_path%" (
    echo ❌ Error: Repository path not found
    echo Please clone your repository first:
    echo git clone https://github.com/aviv-fathallahelmasri/pr-analytics-dashboard.git
    pause
    exit /b 1
)

echo.
echo 📂 Copying enhanced dashboard file...
copy "C:\Users\FElmasri\Desktop\github-pr-analytics\deployment\index.html" "%repo_path%\index.html"

if %errorlevel% neq 0 (
    echo ❌ Error: Failed to copy file
    pause
    exit /b 1
)

echo ✅ File copied successfully
echo.

echo 🔄 Committing changes to GitHub...
cd "%repo_path%"

git add index.html
git commit -m "🚀 Enhanced dashboard visualizations - fixed chart containers, x-axis labels, and responsive design"
git push origin main

if %errorlevel% eq 0 (
    echo.
    echo ========================================
    echo   ✅ DEPLOYMENT SUCCESSFUL!
    echo ========================================
    echo.
    echo Your enhanced dashboard is now live at:
    echo https://aviv-fathallahelmasri.github.io/pr-analytics-dashboard/
    echo.
    echo 🎉 IMPROVEMENTS DEPLOYED:
    echo   • Charts now fit perfectly in containers
    echo   • X-axis labels are fully visible
    echo   • Donut chart is centered and sized properly
    echo   • Better mobile responsiveness
    echo   • Professional appearance throughout
    echo.
    echo ⏰ GitHub Pages will update in 1-2 minutes
    echo 🔄 Hard refresh (Ctrl+F5) if changes don't appear immediately
    echo.
) else (
    echo.
    echo ❌ Git push failed!
    echo Please check:
    echo   • You have push access to the repository
    echo   • You're authenticated with GitHub
    echo   • The repository path is correct
    echo.
)

pause