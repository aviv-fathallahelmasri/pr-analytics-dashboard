# ========================================
# Manual Dashboard Update PowerShell Script
# ========================================
# This script activates the virtual environment and runs the manual update
#
# Usage: Right-click and "Run with PowerShell" or execute from PowerShell terminal
# ========================================

Write-Host ""
Write-Host "====================================================" -ForegroundColor Cyan
Write-Host "   GitHub PR Analytics - Manual Dashboard Update" -ForegroundColor Cyan
Write-Host "====================================================" -ForegroundColor Cyan
Write-Host ""

# Get the script directory
$scriptPath = Split-Path -Parent $MyInvocation.MyCommand.Path
Set-Location $scriptPath

# Activate virtual environment
Write-Host "Activating Python virtual environment..." -ForegroundColor Yellow
& ".\venv\Scripts\Activate.ps1"

if ($LASTEXITCODE -ne 0) {
    Write-Host "ERROR: Failed to activate virtual environment" -ForegroundColor Red
    Write-Host "Please ensure the virtual environment is set up correctly"
    Read-Host "Press Enter to exit"
    exit 1
}

Write-Host "Virtual environment activated successfully!" -ForegroundColor Green
Write-Host ""

# Run the manual update script
Write-Host "Starting dashboard update process..." -ForegroundColor Yellow
Write-Host ""
python manual_dashboard_update.py

# Check if the update was successful
if ($LASTEXITCODE -eq 0) {
    Write-Host ""
    Write-Host "SUCCESS: Dashboard update completed!" -ForegroundColor Green
    Write-Host ""
    Write-Host "Dashboard URL: " -NoNewline
    Write-Host "https://aviv-fathallahelmasri.github.io/pr-analytics-dashboard/" -ForegroundColor Cyan
    Write-Host "Note: Changes may take 2-5 minutes to appear on GitHub Pages" -ForegroundColor Yellow
} else {
    Write-Host ""
    Write-Host "ERROR: Dashboard update failed!" -ForegroundColor Red
    Write-Host "Check the manual_update.log file for details" -ForegroundColor Red
}

Write-Host ""
Write-Host "====================================================" -ForegroundColor Cyan
Write-Host "Process completed. Press any key to exit..."
$null = $Host.UI.RawUI.ReadKey("NoEcho,IncludeKeyDown")
