@echo off
REM ========================================
REM Manual Dashboard Update Batch Script
REM ========================================
REM This script activates the virtual environment and runs the manual update
REM
REM Usage: Just double-click this file or run from command line
REM ========================================

echo.
echo ====================================================
echo    GitHub PR Analytics - Manual Dashboard Update
echo ====================================================
echo.

REM Activate virtual environment
echo Activating Python virtual environment...
call venv\Scripts\activate.bat

REM Check if activation was successful
if errorlevel 1 (
    echo ERROR: Failed to activate virtual environment
    echo Please ensure the virtual environment is set up correctly
    pause
    exit /b 1
)

echo Virtual environment activated successfully!
echo.

REM Run the manual update script
echo Starting dashboard update process...
echo.
python manual_dashboard_update.py

REM Check if the update was successful
if errorlevel 1 (
    echo.
    echo ERROR: Dashboard update failed!
    echo Check the manual_update.log file for details
) else (
    echo.
    echo SUCCESS: Dashboard update completed!
    echo.
    echo Dashboard URL: https://aviv-fathallahelmasri.github.io/pr-analytics-dashboard/
    echo Note: Changes may take 2-5 minutes to appear on GitHub Pages
)

echo.
echo ====================================================
echo Process completed. Press any key to exit...
pause >nul
