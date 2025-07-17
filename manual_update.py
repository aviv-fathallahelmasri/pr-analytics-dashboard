#!/usr/bin/env python3
"""
Manual Update Script for GitHub PR Analytics Dashboard
This script performs the same operations as the GitHub Actions workflow
to update the dashboard data and deploy it to GitHub Pages.
"""

import os
import sys
import subprocess
import shutil
from datetime import datetime

def run_command(cmd, cwd=None):
    """Execute a command and return the result."""
    print(f"Running: {cmd}")
    result = subprocess.run(cmd, shell=True, capture_output=True, text=True, cwd=cwd)
    if result.returncode != 0:
        print(f"Error: {result.stderr}")
        return False
    print(result.stdout)
    return True

def main():
    """Main execution function."""
    print("=== GitHub PR Analytics Manual Update ===")
    print(f"Update started at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
    # Step 1: Update PR data
    print("\n1. Fetching latest PR data...")
    if not run_command(f"{sys.executable} src/fetch_pr_data.py"):
        print("Failed to fetch PR data")
        return
    
    # Step 2: Commit data updates to main branch
    print("\n2. Committing data updates to main branch...")
    run_command("git add data/")
    run_command('git commit -m "Manual update: PR analytics data [skip ci]"')
    run_command("git push origin main")
    
    # Step 3: Prepare deployment directory
    print("\n3. Preparing deployment...")
    
    # Ensure deployment directory structure exists
    os.makedirs("deployment/data", exist_ok=True)
    
    # Copy files to deployment directory
    shutil.copy2("data/pr_metrics_all_prs.csv", "deployment/data/")
    shutil.copy2("data/last_update.json", "deployment/data/")
    
    # Copy index.html if it exists in root
    if os.path.exists("index.html"):
        shutil.copy2("index.html", "deployment/index.html")
    
    # Step 4: Deploy to gh-pages
    print("\n4. Deploying to GitHub Pages...")
    
    # Navigate to deployment directory
    os.chdir("deployment")
    
    # Configure git
    run_command('git config user.name "aviv-fathallahelmasri"')
    run_command('git config user.email "your-email@example.com"')  # Replace with your email
    
    # Add and commit changes
    run_command("git add .")
    run_command(f'git commit -m "Manual deployment: Update dashboard {datetime.now().strftime("%Y-%m-%d %H:%M:%S")} [skip ci]"')
    
    # Push to gh-pages
    run_command("git push origin main:gh-pages --force")
    
    # Return to parent directory
    os.chdir("..")
    
    print("\n=== Update Complete ===")
    print(f"Dashboard should be updated at: https://aviv-fathallahelmasri.github.io/pr-analytics-dashboard/")
    print("Note: GitHub Pages may take a few minutes to reflect the changes")
    print(f"Update completed at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")

if __name__ == "__main__":
    main()
