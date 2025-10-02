# GitHub PR Analytics - Quick Update Script
Write-Host "======================================" -ForegroundColor Cyan
Write-Host "  GitHub PR Analytics - Quick Update  " -ForegroundColor Cyan
Write-Host "======================================" -ForegroundColor Cyan
Write-Host ""

# Ensure we're in the right directory
Set-Location "C:\Users\FElmasri\Desktop\github-pr-analytics"

Write-Host "Current Directory: $(Get-Location)" -ForegroundColor Yellow
Write-Host ""

# Check if virtual environment is activated
if ($env:VIRTUAL_ENV) {
    Write-Host "✓ Virtual environment is active" -ForegroundColor Green
} else {
    Write-Host "⚠ Activating virtual environment..." -ForegroundColor Yellow
    & ".\venv\Scripts\Activate.ps1"
}

Write-Host ""
Write-Host "Step 1: Fetching latest PR data from GitHub..." -ForegroundColor Cyan
Write-Host "-----------------------------------------------" -ForegroundColor Gray

# Run the fetch script directly
python src\fetch_pr_data.py

if ($LASTEXITCODE -eq 0) {
    Write-Host "✓ Data fetch completed successfully!" -ForegroundColor Green
} else {
    Write-Host "✗ Data fetch failed!" -ForegroundColor Red
    exit 1
}

Write-Host ""
Write-Host "Step 2: Copying data to deployment directory..." -ForegroundColor Cyan
Write-Host "-----------------------------------------------" -ForegroundColor Gray

# Copy files to deployment
Copy-Item -Path "data\pr_metrics_all_prs.csv" -Destination "deployment\" -Force
Copy-Item -Path "data\metadata.json" -Destination "deployment\" -Force
Copy-Item -Path "data\last_update.json" -Destination "deployment\" -Force

Write-Host "✓ Files copied to deployment directory" -ForegroundColor Green

Write-Host ""
Write-Host "Step 3: Updating dashboard timestamp..." -ForegroundColor Cyan
Write-Host "-----------------------------------------------" -ForegroundColor Gray

# Update timestamp in index.html
$indexPath = "deployment\index.html"
if (Test-Path $indexPath) {
    $content = Get-Content $indexPath -Raw
    $currentTime = Get-Date -Format "M/d/yyyy, h:mm:ss tt"
    $content = $content -replace 'Last Updated: [^<]+', "Last Updated: $currentTime"
    Set-Content -Path $indexPath -Value $content -NoNewline
    Write-Host "✓ Updated timestamp to: $currentTime" -ForegroundColor Green
}

Write-Host ""
Write-Host "======================================" -ForegroundColor Green
Write-Host "     ✓ UPDATE COMPLETED!              " -ForegroundColor Green
Write-Host "======================================" -ForegroundColor Green
Write-Host ""
Write-Host "To push to GitHub and update live dashboard:" -ForegroundColor Yellow
Write-Host "  git add -A" -ForegroundColor White
Write-Host '  git commit -m "Update PR data - October 2, 2025"' -ForegroundColor White
Write-Host "  git push origin main" -ForegroundColor White
Write-Host ""
Write-Host "Dashboard URL: https://aviv-fathallahelmasri.github.io/pr-analytics-dashboard/" -ForegroundColor Cyan
