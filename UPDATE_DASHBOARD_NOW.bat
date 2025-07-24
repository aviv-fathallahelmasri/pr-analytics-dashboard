@echo off
REM ========================================
REM Quick Manual Update - One Click Solution
REM ========================================

echo.
echo ====================================================
echo    GitHub PR Analytics - Quick Manual Update
echo ====================================================
echo.
echo This will update your dashboard with the latest PR data.
echo.

REM Activate virtual environment
call venv\Scripts\activate.bat 2>nul

REM Quick verification
echo Performing quick environment check...
python verify_before_update.py
if errorlevel 1 (
    echo.
    echo Environment check failed! Please fix issues above.
    pause
    exit /b 1
)

echo.
echo Environment verified! Starting update...
echo.
timeout /t 2 /nobreak >nul

REM Run the update
python manual_dashboard_update.py

echo.
echo ====================================================
echo Dashboard update process completed!
echo.
echo Check your dashboard at:
echo https://aviv-fathallahelmasri.github.io/pr-analytics-dashboard/
echo.
echo Note: GitHub Pages may take 2-5 minutes to update
echo ====================================================
echo.
pause
