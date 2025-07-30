#!/usr/bin/env python3
"""
Direct GitHub Pages Update
==========================
Directly updates the gh-pages branch with the latest data.
"""

import os
import subprocess
import shutil
from datetime import datetime
from pathlib import Path

def run_command(cmd):
    """Execute a command and show output."""
    print(f"$ {cmd}")
    result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
    if result.stdout:
        print(result.stdout)
    if result.stderr:
        print(f"Error: {result.stderr}")
    return result.returncode == 0

def main():
    print("=== Direct GitHub Pages Update ===")
    print("=" * 50)
    
    # Step 1: Save current branch
    print("\n1. Saving current state...")
    run_command("git stash")
    
    # Step 2: Switch to gh-pages branch
    print("\n2. Switching to gh-pages branch...")
    success = run_command("git checkout gh-pages")
    
    if not success:
        print("Creating gh-pages branch...")
        run_command("git checkout -b gh-pages")
    
    # Step 3: Pull latest from gh-pages
    print("\n3. Getting latest gh-pages...")
    run_command("git pull origin gh-pages")
    
    # Step 4: Copy updated data files
    print("\n4. Copying updated data files...")
    project_root = Path.cwd()
    
    # Ensure data directory exists
    Path("data").mkdir(exist_ok=True)
    
    # Switch back to main temporarily to get files
    run_command("git checkout main -- data/pr_metrics_all_prs.csv")
    run_command("git checkout main -- data/last_update.json")
    
    # Step 5: Commit and push
    print("\n5. Committing updates...")
    run_command("git add data/")
    
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    commit_success = run_command(f'git commit -m "Update dashboard data - {timestamp}"')
    
    if commit_success:
        print("\n6. Pushing to gh-pages...")
        push_success = run_command("git push origin gh-pages")
        
        if push_success:
            print("\n✅ Successfully updated gh-pages branch!")
        else:
            print("\n❌ Push failed - trying force push...")
            run_command("git push origin gh-pages --force")
    else:
        print("\nNo changes to commit - data might be up to date")
    
    # Step 7: Return to main branch
    print("\n7. Returning to main branch...")
    run_command("git checkout main")
    run_command("git stash pop")
    
    print("\n" + "=" * 50)
    print("📊 Dashboard URL: https://aviv-fathallahelmasri.github.io/pr-analytics-dashboard/")
    print("⏰ Changes should appear within 2-10 minutes")
    print("💡 Tip: Open in incognito mode or clear cache to see changes immediately")

if __name__ == "__main__":
    main()
