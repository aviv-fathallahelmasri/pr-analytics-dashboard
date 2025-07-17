#!/usr/bin/env python3
"""
Fix deployment structure and push to GitHub Pages
"""

import os
import subprocess
import shutil
from datetime import datetime

def fix_deployment():
    """Fix the deployment directory structure and push to GitHub Pages"""
    
    print("🔧 Fixing deployment structure...")
    
    # Change to deployment directory
    os.chdir('deployment')
    
    try:
        # Remove the problematic subdirectory
        if os.path.exists('pr-analytics-dashboard'):
            print("📁 Removing nested pr-analytics-dashboard directory...")
            # First, remove it from git if tracked
            subprocess.run(['git', 'rm', '-r', '--cached', 'pr-analytics-dashboard'], 
                          capture_output=True)
            # Then remove the actual directory
            shutil.rmtree('pr-analytics-dashboard', ignore_errors=True)
        
        # Check current branch
        result = subprocess.run(['git', 'branch', '--show-current'], 
                              capture_output=True, text=True)
        current_branch = result.stdout.strip()
        print(f"📌 Current branch: {current_branch}")
        
        # If we're not on main, switch to it
        if current_branch != 'main':
            print("🔄 Switching to main branch...")
            subprocess.run(['git', 'checkout', '-b', 'main'], capture_output=True)
        
        # Stage all changes
        print("📝 Staging changes...")
        subprocess.run(['git', 'add', '.'], check=True)
        
        # Create commit
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        commit_msg = f"Update PR analytics data - {timestamp} (214 PRs)"
        
        print(f"💾 Creating commit: {commit_msg}")
        result = subprocess.run(['git', 'commit', '-m', commit_msg], 
                              capture_output=True, text=True)
        
        if result.returncode != 0 and "nothing to commit" not in result.stdout:
            print(f"⚠️ Commit output: {result.stdout}")
        
        # Force push to main branch
        print("🚀 Pushing to GitHub Pages (main branch)...")
        result = subprocess.run(['git', 'push', 'origin', 'main', '--force'], 
                              capture_output=True, text=True)
        
        if result.returncode == 0:
            print("✅ Successfully deployed to GitHub Pages!")
            print("🌐 Dashboard: https://aviv-fathallahelmasri.github.io/pr-analytics-dashboard/")
            return True
        else:
            print(f"❌ Push failed: {result.stderr}")
            
            # Try creating gh-pages branch
            print("🔄 Trying gh-pages branch...")
            subprocess.run(['git', 'checkout', '-b', 'gh-pages'], capture_output=True)
            result = subprocess.run(['git', 'push', 'origin', 'gh-pages', '--force'], 
                                  capture_output=True, text=True)
            
            if result.returncode == 0:
                print("✅ Successfully deployed to GitHub Pages (gh-pages branch)!")
                print("🌐 Dashboard: https://aviv-fathallahelmasri.github.io/pr-analytics-dashboard/")
                print("📌 Note: You may need to set gh-pages as the deployment branch in GitHub settings")
                return True
            else:
                print(f"❌ gh-pages push also failed: {result.stderr}")
                return False
                
    except Exception as e:
        print(f"❌ Error: {str(e)}")
        return False
    finally:
        # Return to parent directory
        os.chdir('..')

if __name__ == "__main__":
    # Change to project directory
    os.chdir(r'C:\Users\FElmasri\Desktop\github-pr-analytics')
    
    # Verify we have updated data
    if os.path.exists('data/last_update.json'):
        import json
        with open('data/last_update.json', 'r') as f:
            info = json.load(f)
        print(f"📊 Current data: {info['total_prs']} PRs (last updated: {info['last_update_time']})")
    
    # Fix and deploy
    if fix_deployment():
        print("\n🎉 Deployment completed successfully!")
    else:
        print("\n❌ Deployment failed. Please check the error messages above.")
