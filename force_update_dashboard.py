#!/usr/bin/env python3
"""
Force GitHub Pages Update - Aggressive Fix
==========================================
This script forces a complete refresh of the GitHub Pages deployment.
Based on lessons learned from previous fixes.
"""

import os
import subprocess
import shutil
import json
from datetime import datetime
from pathlib import Path
import time

def run_command(cmd, cwd=None):
    """Execute a command and return the result."""
    print(f"Running: {cmd}")
    result = subprocess.run(cmd, shell=True, capture_output=True, text=True, cwd=cwd)
    if result.stdout:
        print(result.stdout)
    if result.stderr:
        print(f"Error/Warning: {result.stderr}")
    return result.returncode == 0

def main():
    print("=== FORCE GitHub Pages Update ===")
    print(f"Started at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("This will aggressively update the deployment!")
    print("=" * 50)
    
    project_root = Path(__file__).parent
    deployment_dir = project_root / "deployment"
    
    # Step 1: Verify we have updated data
    print("\n1. Verifying local data is updated...")
    data_file = project_root / "data" / "last_update.json"
    if data_file.exists():
        with open(data_file, 'r') as f:
            data = json.load(f)
        print(f"✅ Local data: {data['total_prs']} PRs, updated at {data['last_update_time']}")
    
    # Step 2: Create a temporary deployment directory
    print("\n2. Creating fresh deployment directory...")
    temp_deploy = project_root / "temp_deployment"
    
    # Remove temp directory if it exists
    if temp_deploy.exists():
        shutil.rmtree(temp_deploy)
    
    # Create fresh directory
    temp_deploy.mkdir()
    
    # Step 3: Copy all necessary files to temp deployment
    print("\n3. Copying files to temporary deployment...")
    
    # Copy deployment files
    if (deployment_dir / "index.html").exists():
        shutil.copy2(deployment_dir / "index.html", temp_deploy / "index.html")
    elif (project_root / "index.html").exists():
        shutil.copy2(project_root / "index.html", temp_deploy / "index.html")
    
    # Copy CSS and JS directories
    if (deployment_dir / "css").exists():
        shutil.copytree(deployment_dir / "css", temp_deploy / "css")
    if (deployment_dir / "js").exists():
        shutil.copytree(deployment_dir / "js", temp_deploy / "js")
    
    # Copy fresh data
    (temp_deploy / "data").mkdir()
    shutil.copy2(project_root / "data" / "pr_metrics_all_prs.csv", temp_deploy / "data")
    shutil.copy2(project_root / "data" / "last_update.json", temp_deploy / "data")
    
    print("✅ Files copied to temporary deployment")
    
    # Step 4: Initialize git in temp directory and push to gh-pages
    os.chdir(temp_deploy)
    print(f"\n4. Working in: {os.getcwd()}")
    
    # Initialize git
    run_command("git init")
    run_command('git config user.name "aviv-fathallahelmasri"')
    run_command('git config user.email "aviv.fathalla.helmasri@asideas.de"')
    
    # Add remote
    run_command("git remote add origin https://github.com/aviv-fathallahelmasri/pr-analytics-dashboard")
    
    # Create initial commit
    run_command("git add -A")
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    run_command(f'git commit -m "Force update: Dashboard deployment {timestamp}"')
    
    # Force push to gh-pages
    print("\n5. Force pushing to gh-pages branch...")
    success = run_command("git push origin master:gh-pages --force")
    
    if not success:
        print("Trying alternative branch name...")
        run_command("git branch -m main")
        success = run_command("git push origin main:gh-pages --force")
    
    # Step 6: Clean up and update deployment directory
    os.chdir(project_root)
    print("\n6. Updating deployment directory...")
    
    # Remove old deployment git directory
    deployment_git = deployment_dir / ".git"
    if deployment_git.exists():
        # Save git config first
        git_config = deployment_git / "config"
        config_content = ""
        if git_config.exists():
            with open(git_config, 'r') as f:
                config_content = f.read()
        
        # Remove git directory
        shutil.rmtree(deployment_git)
        
        # Copy temp deployment git to deployment
        shutil.copytree(temp_deploy / ".git", deployment_git)
        
        # Restore config if needed
        if config_content and "[remote" in config_content:
            with open(git_config, 'w') as f:
                f.write(config_content)
    
    # Copy updated files back to deployment
    shutil.copy2(temp_deploy / "data" / "pr_metrics_all_prs.csv", 
                deployment_dir / "data" / "pr_metrics_all_prs.csv")
    shutil.copy2(temp_deploy / "data" / "last_update.json", 
                deployment_dir / "data" / "last_update.json")
    
    # Clean up temp directory
    shutil.rmtree(temp_deploy)
    
    # Step 7: Verify deployment
    print("\n7. Deployment Summary:")
    print("=" * 50)
    
    if success:
        print("✅ Successfully force-pushed to gh-pages!")
        print("\n📊 Dashboard URL: https://aviv-fathallahelmasri.github.io/pr-analytics-dashboard/")
        print("⏰ GitHub Pages will update in 2-10 minutes")
        print("\n🔄 To check immediately:")
        print("1. Open the dashboard in an incognito/private window")
        print("2. Or clear your browser cache and refresh")
        print("3. Or add ?v=" + str(int(time.time())) + " to the URL")
        
        # Also update main branch deployment directory
        os.chdir(deployment_dir)
        run_command("git add -A")
        run_command(f'git commit -m "Sync deployment directory {timestamp}"')
        run_command("git push origin main")
        os.chdir(project_root)
    else:
        print("❌ Failed to push to gh-pages")
        print("Please check your GitHub credentials and try again")
    
    print(f"\nCompleted at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")

if __name__ == "__main__":
    main()
