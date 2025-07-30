#!/usr/bin/env python3
"""
Force GitHub Pages Rebuild with Guaranteed Changes
=================================================
This script ensures GitHub Pages gets updated by making actual changes.
"""

import os
import json
import subprocess
from datetime import datetime
from pathlib import Path

def run_command(cmd):
    """Execute a command and return success status."""
    print(f"$ {cmd}")
    result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
    if result.stdout:
        print(result.stdout.strip())
    if result.stderr and result.returncode != 0:
        print(f"Error: {result.stderr.strip()}")
    return result.returncode == 0

def main():
    print("=== FORCE GitHub Pages Rebuild ===")
    print("This will guarantee an update by modifying metadata")
    print("=" * 50)
    
    # Save current directory
    original_dir = os.getcwd()
    
    try:
        # Change to deployment directory
        os.chdir("deployment")
        print(f"\nWorking in: {os.getcwd()}")
        
        # Ensure we're on gh-pages branch
        print("\n1. Checking branch...")
        run_command("git checkout gh-pages")
        
        # Update the last_update.json with force update timestamp
        print("\n2. Modifying metadata to force update...")
        update_file = Path("data/last_update.json")
        
        if update_file.exists():
            with open(update_file, 'r') as f:
                data = json.load(f)
            
            # Add force update timestamp
            data['force_update'] = datetime.now().isoformat()
            data['update_method'] = 'manual_force'
            
            with open(update_file, 'w') as f:
                json.dump(data, f, indent=2)
            
            print(f"✅ Modified last_update.json with force update timestamp")
        
        # Create a deployment timestamp file
        print("\n3. Creating deployment marker...")
        with open(".deployment_timestamp", "w") as f:
            f.write(f"Last deployment: {datetime.now().isoformat()}\n")
            f.write(f"Method: Manual force update\n")
        
        # Now git should see changes
        print("\n4. Checking for changes...")
        run_command("git status --short")
        
        # Add and commit
        print("\n5. Committing changes...")
        run_command("git add -A")
        
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        commit_msg = f"Force update: Dashboard data {timestamp}"
        
        if run_command(f'git commit -m "{commit_msg}"'):
            print("\n6. Pushing to GitHub Pages...")
            
            if run_command("git push origin gh-pages --force"):
                print("\n✅ Successfully forced update to GitHub Pages!")
                
                # Also update the index.html to bust cache
                index_file = Path("index.html")
                if index_file.exists():
                    print("\n7. Adding cache buster to index.html...")
                    
                    with open(index_file, 'r', encoding='utf-8') as f:
                        content = f.read()
                    
                    # Update the last updated timestamp in the HTML
                    import re
                    pattern = r'Last Updated: [^<]+'
                    replacement = f'Last Updated: {datetime.now().strftime("%m/%d/%Y, %I:%M:%S %p")}'
                    
                    new_content = re.sub(pattern, replacement, content)
                    
                    if new_content != content:
                        with open(index_file, 'w', encoding='utf-8') as f:
                            f.write(new_content)
                        
                        run_command("git add index.html")
                        run_command(f'git commit -m "Update timestamp in HTML"')
                        run_command("git push origin gh-pages")
                        print("✅ Updated HTML timestamp")
            else:
                print("\n❌ Push failed!")
        else:
            print("\n⚠️  No changes to commit")
            
            # Try a different approach - modify the HTML directly
            print("\n8. Trying alternative approach - modifying HTML...")
            index_file = Path("index.html")
            if index_file.exists():
                with open(index_file, 'r', encoding='utf-8') as f:
                    content = f.read()
                
                # Add a comment with timestamp to force a change
                timestamp_comment = f"\n<!-- Force update: {datetime.now().isoformat()} -->\n"
                
                # Add before closing body tag
                new_content = content.replace("</body>", f"{timestamp_comment}</body>")
                
                with open(index_file, 'w', encoding='utf-8') as f:
                    f.write(new_content)
                
                run_command("git add index.html")
                run_command(f'git commit -m "Force cache refresh - {timestamp}"')
                run_command("git push origin gh-pages --force")
                print("✅ Forced update via HTML modification")
        
    finally:
        # Return to original directory
        os.chdir(original_dir)
    
    print("\n" + "=" * 50)
    print("📊 Dashboard: https://aviv-fathallahelmasri.github.io/pr-analytics-dashboard/")
    print("\n🔄 To see changes immediately:")
    print("1. Wait 2-5 minutes for GitHub Pages to rebuild")
    print("2. Open in incognito/private browsing mode")
    print("3. Or append ?v=" + str(int(datetime.now().timestamp())) + " to the URL")
    print("4. Or clear your browser cache completely")
    
    # Check deployment branch directly
    print("\n💡 Check deployment directly at:")
    print("https://github.com/aviv-fathallahelmasri/pr-analytics-dashboard/tree/gh-pages/data")

if __name__ == "__main__":
    main()
