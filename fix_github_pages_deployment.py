#!/usr/bin/env python3
"""
Fix GitHub Pages Deployment
===========================
This script ensures proper deployment to the gh-pages branch.
"""

import os
import subprocess
import shutil
import json
from datetime import datetime
from pathlib import Path

def run_command(cmd, cwd=None):
    """Execute a command and return the result."""
    print(f"Running: {cmd}")
    result = subprocess.run(cmd, shell=True, capture_output=True, text=True, cwd=cwd)
    print(result.stdout)
    if result.stderr:
        print(f"Error/Warning: {result.stderr}")
    return result.returncode == 0, result.stdout

def main():
    print("=== Fixing GitHub Pages Deployment ===")
    print(f"Started at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
    project_root = Path(__file__).parent
    deployment_dir = project_root / "deployment"
    
    # Step 1: Ensure we have the latest data
    print("\n1. Checking latest data...")
    data_file = project_root / "data" / "last_update.json"
    if data_file.exists():
        with open(data_file, 'r') as f:
            data = json.load(f)
        print(f"Latest data: {data['total_prs']} PRs, updated at {data['last_update_time']}")
    
    # Step 2: Copy fresh data to deployment
    print("\n2. Copying fresh data to deployment directory...")
    deployment_data_dir = deployment_dir / "data"
    deployment_data_dir.mkdir(exist_ok=True)
    
    shutil.copy2(project_root / "data" / "pr_metrics_all_prs.csv", deployment_data_dir)
    shutil.copy2(project_root / "data" / "last_update.json", deployment_data_dir)
    print("✅ Data files copied")
    
    # Step 3: Switch to deployment directory and fix git configuration
    os.chdir(deployment_dir)
    print(f"\n3. Working in deployment directory: {os.getcwd()}")
    
    # Check current branch
    success, branch = run_command("git branch --show-current")
    print(f"Current branch: {branch.strip()}")
    
    # Step 4: Create or switch to gh-pages branch
    print("\n4. Setting up gh-pages branch...")
    
    # Check if gh-pages exists
    success, branches = run_command("git branch -r")
    
    if "origin/gh-pages" in branches:
        print("gh-pages branch exists, checking it out...")
        run_command("git fetch origin gh-pages")
        run_command("git checkout -B gh-pages origin/gh-pages")
    else:
        print("Creating new gh-pages branch...")
        run_command("git checkout --orphan gh-pages")
        # Remove all files and add them back
        run_command("git rm -rf . 2>nul || echo.")
    
    # Step 5: Ensure all files are in place
    print("\n5. Ensuring all deployment files are in place...")
    
    # If we're on a fresh gh-pages branch, we need to add all files back
    os.chdir(project_root)
    
    # Copy deployment files again to ensure they're all there
    if not (deployment_dir / "index.html").exists():
        if (project_root / "index.html").exists():
            shutil.copy2(project_root / "index.html", deployment_dir)
    
    # Copy data files again
    shutil.copy2(project_root / "data" / "pr_metrics_all_prs.csv", deployment_data_dir)
    shutil.copy2(project_root / "data" / "last_update.json", deployment_data_dir)
    
    # Step 6: Commit and push to gh-pages
    os.chdir(deployment_dir)
    print("\n6. Committing and pushing to gh-pages...")
    
    # Configure git
    run_command('git config user.name "aviv-fathallahelmasri"')
    run_command('git config user.email "aviv.fathalla.helmasri@asideas.de"')
    
    # Add all files
    run_command("git add -A")
    
    # Check status
    success, status = run_command("git status --porcelain")
    
    if status.strip():
        # Commit changes
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        commit_msg = f"Fix deployment: Update dashboard {timestamp} [skip ci]"
        run_command(f'git commit -m "{commit_msg}"')
        
        # Push to gh-pages
        print("\nPushing to gh-pages branch...")
        success, output = run_command("git push origin gh-pages --force")
        
        if success:
            print("\n✅ Successfully deployed to GitHub Pages!")
        else:
            print("\n❌ Push failed. Trying alternative method...")
            # Try pushing from current branch to gh-pages
            run_command("git push origin HEAD:gh-pages --force")
    else:
        print("No changes to deploy")
    
    # Step 7: Verify deployment
    print("\n7. Deployment Summary:")
    print("=" * 50)
    
    # Check deployed data
    deployed_update = deployment_data_dir / "last_update.json"
    if deployed_update.exists():
        with open(deployed_update, 'r') as f:
            data = json.load(f)
        print(f"✅ Deployed data: {data['total_prs']} PRs")
        print(f"✅ Update time: {data['last_update_time']}")
    
    print(f"\n📊 Dashboard URL: https://aviv-fathallahelmasri.github.io/pr-analytics-dashboard/")
    print("⏰ Note: GitHub Pages may take 2-10 minutes to update")
    print("🔄 Force refresh with Ctrl+F5 to see changes immediately")
    
    # Return to project root
    os.chdir(project_root)
    
    print(f"\nCompleted at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")

if __name__ == "__main__":
    main()
