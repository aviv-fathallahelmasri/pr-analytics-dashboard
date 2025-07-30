@echo off
echo.
echo ====================================================
echo    Checking GitHub Pages Deployment Status
echo ====================================================
echo.

call venv\Scripts\activate.bat 2>nul

python check_deployment_status.py

echo.
echo ====================================================
echo.
echo To fix deployment issues, run:
echo   python fix_github_pages_deployment.py
echo.
pause
