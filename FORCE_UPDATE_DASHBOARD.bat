@echo off
echo.
echo ====================================
echo  FORCING DASHBOARD UPDATE NOW
echo ====================================
echo.

cd /d "C:\Users\FElmasri\Desktop\github-pr-analytics"

REM Activate virtual environment
call venv\Scripts\activate.bat

REM Run the force update script
python force_dashboard_update_now.py

echo.
echo ====================================
echo  UPDATE PROCESS COMPLETE
echo ====================================
echo.
pause
