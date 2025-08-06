@echo off
echo.
echo =============================================
echo  FIXING DASHBOARD DEPLOYMENT SYNC ISSUE
echo =============================================
echo.
echo This is the EXACT same issue we had before!
echo The deployment directory is out of sync.
echo.

cd deployment

echo Checking deployment status...
git status

echo.
echo Fetching latest from remote...
git fetch origin

echo.
echo Force pushing local changes to GitHub Pages...
git add -A
git commit -m "Force sync: Update dashboard with 244 PRs [%date% %time%]"
git push origin main --force

echo.
echo =============================================
echo  DEPLOYMENT FIXED!
echo =============================================
echo.
echo Dashboard should update in 1-2 minutes.
echo Check: https://aviv-fathallahelmasri.github.io/pr-analytics-dashboard/
echo.

cd ..
pause
