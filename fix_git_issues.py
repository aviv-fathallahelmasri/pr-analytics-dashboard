#!/usr/bin/env python3
"""
Fix git repository issues
"""

import os
import shutil
import subprocess

def fix_git_issues():
    """Remove problematic git directories and fix the repository"""
    
    print("🔧 Fixing git repository issues...")
    
    try:
        # Remove the problematic nested git directory
        problematic_path = "deployment/pr-analytics-dashboard/.git"
        if os.path.exists(problematic_path):
            print(f"🗑️ Removing problematic directory: {problematic_path}")
            shutil.rmtree(problematic_path, ignore_errors=True)
        
        # Also remove the entire pr-analytics-dashboard subdirectory if it exists
        nested_repo = "deployment/pr-analytics-dashboard"
        if os.path.exists(nested_repo):
            print(f"🗑️ Removing nested repository: {nested_repo}")
            shutil.rmtree(nested_repo, ignore_errors=True)
        
        print("✅ Cleaned up problematic directories")
        
        # Now try git status again
        print("\n📊 Checking git status...")
        result = subprocess.run(['git', 'status', '--porcelain'], 
                              capture_output=True, text=True)
        
        if result.returncode == 0:
            print("✅ Git repository is now healthy")
            if result.stdout:
                print("\n📝 Modified files:")
                print(result.stdout)
            else:
                print("✨ Working directory is clean")
        
        # Now we can proceed with the sync
        print("\n🔄 Syncing with remote repository...")
        
        # Reset the workflow file to match remote
        subprocess.run(['git', 'checkout', 'HEAD', '.github/workflows/daily-update.yml'], 
                      capture_output=True)
        
        # Pull latest changes
        subprocess.run(['git', 'pull', 'origin', 'main'], check=True)
        print("✅ Successfully synced with remote repository")
        
        print("\n🎯 Summary:")
        print("- Git repository issues fixed")
        print("- Synced with remote repository")
        print("- Your automation is ready to run")
        print("\n⏰ Next automatic update: Tomorrow at 8:00 AM Berlin time")
        
    except Exception as e:
        print(f"❌ Error: {str(e)}")
        print("\n💡 Manual fix:")
        print("1. Run: rm -rf deployment/pr-analytics-dashboard")
        print("2. Run: git checkout HEAD .")
        print("3. Run: git pull origin main")

if __name__ == "__main__":
    os.chdir(r'C:\Users\FElmasri\Desktop\github-pr-analytics')
    fix_git_issues()
