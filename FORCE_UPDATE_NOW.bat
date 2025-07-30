@echo off
REM ====================================================
REM  SOLUTION: Force Update GitHub Pages Dashboard
REM ====================================================
echo.
echo This will force update your GitHub Pages dashboard
echo.

REM Activate virtual environment
call venv\Scripts\activate.bat 2>nul

echo.
echo Step 1: Updating data files in deployment directory...
echo.

REM Force copy latest data to deployment
copy /Y data\pr_metrics_all_prs.csv deployment\data\pr_metrics_all_prs.csv
copy /Y data\last_update.json deployment\data\last_update.json

echo Files copied successfully!
echo.
echo Step 2: Pushing to GitHub Pages...
echo.

REM Change to deployment directory
cd deployment

REM Configure git
git config user.name "aviv-fathallahelmasri"
git config user.email "aviv.fathalla.helmasri@asideas.de"

REM Check current branch
git branch --show-current

REM Make sure we're on gh-pages
git checkout gh-pages 2>nul || git checkout -b gh-pages

REM Add a timestamp file to force a change
echo Last forced update: %date% %time% > .force_update

REM Add all changes
git add -A

REM Commit with timestamp
git commit -m "Force update: Dashboard data %date% %time% [skip ci]"

REM Push to gh-pages
git push origin gh-pages --force

REM Return to main directory
cd ..

echo.
echo ====================================================
echo Update complete!
echo.
echo Dashboard: https://aviv-fathallahelmasri.github.io/pr-analytics-dashboard/
echo.
echo IMPORTANT: 
echo - Wait 2-5 minutes for GitHub Pages to update
echo - Use Ctrl+F5 to force refresh your browser
echo - Or open in incognito/private window
echo ====================================================
echo.
pause
