@echo off
REM ====================================================
REM  QUICK FIX: Direct gh-pages update via web
REM ====================================================
echo.
echo The issue is that your local gh-pages is updated but
echo GitHub's gh-pages branch is not synced.
echo.
echo QUICK MANUAL FIX:
echo.
echo 1. Go to: https://github.com/aviv-fathallahelmasri/pr-analytics-dashboard/tree/gh-pages/data
echo.
echo 2. Click on "last_update.json"
echo.
echo 3. Click the pencil icon to edit
echo.
echo 4. The file should show:
echo    - total_prs: 232 (this is OLD)
echo.
echo 5. Change it to:
echo    - total_prs: 236
echo    - last_update_time: "2025-07-24T10:36:34.069052+00:00"
echo.
echo 6. Commit directly to gh-pages branch
echo.
echo This will force GitHub Pages to rebuild with new data!
echo.
echo ====================================================
echo.
echo Or run: python guaranteed_force_update.py
echo.
pause
