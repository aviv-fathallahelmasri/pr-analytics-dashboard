#!/usr/bin/env python3
"""
Commit and push the updated workflow to ensure automation works correctly
"""

import os
import subprocess

def update_workflow():
    """Commit and push the updated workflow"""
    
    print("📋 Updating GitHub Actions workflow for proper automation...")
    
    try:
        # Git operations
        subprocess.run(['git', 'add', '.github/workflows/daily-update.yml'], check=True)
        subprocess.run(['git', 'commit', '-m', 'fix: Update daily workflow to deploy directly to main branch'], check=True)
        subprocess.run(['git', 'push', 'origin', 'main'], check=True)
        
        print("✅ Workflow updated successfully!")
        print("\n🎯 Automation is now fully configured:")
        print("- Will run daily at 8:00 AM Berlin time")
        print("- Fetches latest PR data automatically")
        print("- Updates analytics without manual intervention")
        print("- Deploys to GitHub Pages automatically")
        print("\n📅 Next automatic run: Tomorrow at 8:00 AM Berlin time")
        
    except subprocess.CalledProcessError as e:
        if "nothing to commit" in str(e):
            print("ℹ️ No changes needed - workflow is already up to date")
        else:
            print(f"❌ Error: {str(e)}")

if __name__ == "__main__":
    os.chdir(r'C:\Users\FElmasri\Desktop\github-pr-analytics')
    update_workflow()
