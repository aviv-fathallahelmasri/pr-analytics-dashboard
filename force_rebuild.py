#!/usr/bin/env python3
"""
Force GitHub Pages to rebuild by making a trivial change
"""

import os
import subprocess
from datetime import datetime

def force_pages_rebuild():
    """Force GitHub Pages to rebuild by updating index.html"""
    
    print("🔧 Forcing GitHub Pages rebuild...")
    
    # Change to deployment directory
    os.chdir('deployment')
    
    try:
        # Read index.html
        with open('index.html', 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Add/update a comment with timestamp to force change
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        rebuild_comment = f"<!-- GitHub Pages Rebuild: {timestamp} -->"
        
        # Remove old rebuild comment if exists
        import re
        content = re.sub(r'<!-- GitHub Pages Rebuild:.*?-->', '', content)
        
        # Add new comment at the beginning
        content = f"{rebuild_comment}\n{content}"
        
        # Write back
        with open('index.html', 'w', encoding='utf-8') as f:
            f.write(content)
        
        print("📝 Updated index.html with rebuild timestamp")
        
        # Git operations
        subprocess.run(['git', 'add', 'index.html'], check=True)
        subprocess.run(['git', 'commit', '-m', f'Force GitHub Pages rebuild - {timestamp}'], check=True)
        subprocess.run(['git', 'push', 'origin', 'main'], check=True)
        
        print("✅ Pushed rebuild trigger to GitHub")
        print("⏳ GitHub Pages should rebuild within 2-5 minutes")
        
        # Return to parent directory
        os.chdir('..')
        
        print("\n📋 Next steps:")
        print("1. Go to: https://github.com/aviv-fathallahelmasri/pr-analytics-dashboard/actions")
        print("2. Look for 'pages-build-deployment' workflow")
        print("3. Wait for it to complete (usually 2-5 minutes)")
        print("4. Check your dashboard again")
        
    except Exception as e:
        print(f"❌ Error: {str(e)}")
        os.chdir('..')

if __name__ == "__main__":
    force_pages_rebuild()
