@echo off
echo ======================================================================
echo FORCE COMPLETE UPDATE - GitHub PR Analytics Dashboard
echo ======================================================================
echo.

REM Check if we're in the right directory
cd /d "C:\Users\FElmasri\Desktop\github-pr-analytics"

REM Check if virtual environment exists and activate it
if exist "venv\Scripts\activate.bat" (
    echo Activating virtual environment...
    call venv\Scripts\activate.bat
) else (
    echo Virtual environment not found, using system Python...
)

REM Check if GITHUB_TOKEN is set
if "%GITHUB_TOKEN%"=="" (
    echo.
    echo WARNING: GITHUB_TOKEN is not set!
    echo Please set it using: set GITHUB_TOKEN=your_token_here
    echo.
    set /p token="Enter your GitHub token now (or press Enter to skip): "
    if not "!token!"=="" (
        set GITHUB_TOKEN=!token!
    )
)

echo.
echo Running Force Complete Update...
echo ======================================================================
python force_complete_update.py

echo.
echo ======================================================================
echo Update process completed!
echo Check the output above for any errors.
echo ======================================================================
pause
