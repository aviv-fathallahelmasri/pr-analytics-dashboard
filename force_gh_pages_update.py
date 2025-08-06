#!/usr/bin/env python3
"""
Force GitHub Pages Update - Ensure Dashboard Reflects Latest Changes
"""

import os
import subprocess
import time
from pathlib import Path
from datetime import datetime

def run_command(cmd, cwd=None):
    """Execute a command and return output."""
    print(f"Executing: {cmd}")
    result = subprocess.run(cmd, shell=True, capture_output=True, text=True, cwd=cwd)
    if result.returncode != 0:
        print(f"Error: {result.stderr}")
    else:
        print(f"Success: {result.stdout}")
    return result.returncode == 0

def force_update():
    """Force GitHub Pages to update with latest data."""
    project_root = Path(__file__).parent
    deployment_dir = project_root / "deployment"
    
    print("=" * 60)
    print("FORCING GITHUB PAGES UPDATE")
    print("=" * 60)
    
    # Step 1: Switch to deployment directory
    os.chdir(deployment_dir)
    print(f"\nWorking in: {os.getcwd()}")
    
    # Step 2: Check current branch
    run_command("git branch")
    
    # Step 3: Fetch latest
    print("\nFetching latest from remote...")
    run_command("git fetch origin")
    
    # Step 4: Check if we need to switch to gh-pages branch
    current_branch = subprocess.run("git rev-parse --abbrev-ref HEAD", 
                                   shell=True, capture_output=True, text=True).stdout.strip()
    
    if current_branch != "gh-pages":
        print(f"\nCurrent branch is {current_branch}, switching to gh-pages...")
        if not run_command("git checkout gh-pages"):
            print("Creating gh-pages branch...")
            run_command("git checkout -b gh-pages")
    
    # Step 5: Pull latest changes
    print("\nPulling latest changes...")
    run_command("git pull origin gh-pages")
    
    # Step 6: Copy fresh data from main branch
    print("\nCopying fresh data files...")
    os.chdir(project_root)
    
    # Copy data files
    run_command("xcopy /Y /E data\\*.* deployment\\data\\")
    
    # Step 7: Go back to deployment and commit
    os.chdir(deployment_dir)
    
    # Add a cache-busting timestamp to index.html
    print("\nAdding cache buster to force reload...")
    index_path = deployment_dir / "index.html"
    if index_path.exists():
        with open(index_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Update the refresh parameter
        import re
        timestamp = int(time.time())
        content = re.sub(r'refresh=\d+', f'refresh={timestamp}', content)
        
        # Also update the last updated date if it exists
        current_date = datetime.now().strftime("%m/%d/%Y, %I:%M:%S %p")
        content = re.sub(r'Last Updated: [^<]+', f'Last Updated: {current_date}', content)
        
        with open(index_path, 'w', encoding='utf-8') as f:
            f.write(content)
    
    # Step 8: Commit everything
    print("\nCommitting all changes...")
    run_command("git add -A")
    run_command(f'git commit -m "Force update: Dashboard refresh {datetime.now().isoformat()}"')
    
    # Step 9: Force push to gh-pages
    print("\nForce pushing to gh-pages...")
    run_command("git push origin gh-pages --force")
    
    # Step 10: Also update main branch to keep in sync
    print("\nSyncing with main branch...")
    run_command("git checkout main")
    run_command("git add -A")
    run_command(f'git commit -m "Sync deployment files {datetime.now().isoformat()}"')
    run_command("git push origin main")
    
    # Step 11: Push main to gh-pages again for good measure
    print("\nFinal push from main to gh-pages...")
    run_command("git push origin main:gh-pages --force")
    
    print("\n" + "=" * 60)
    print("FORCE UPDATE COMPLETE!")
    print("=" * 60)
    print("\nGitHub Pages should update within 1-2 minutes.")
    print("Dashboard URL: https://aviv-fathallahelmasri.github.io/pr-analytics-dashboard/")
    print("\nIf it still shows old data, try:")
    print("1. Hard refresh: Ctrl+F5 or Cmd+Shift+R")
    print("2. Clear browser cache")
    print("3. Open in incognito/private mode")
    print("4. Add ?v=new to the URL")

if __name__ == "__main__":
    force_update()
