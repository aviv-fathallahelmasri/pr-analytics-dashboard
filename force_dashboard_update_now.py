#!/usr/bin/env python3
"""
Force Update Dashboard - Ensure GitHub Pages Shows Latest Data
"""

import os
import json
import subprocess
from pathlib import Path
from datetime import datetime

def run_cmd(cmd, cwd=None):
    """Run command and return success status."""
    print(f"→ {cmd}")
    result = subprocess.run(cmd, shell=True, capture_output=True, text=True, cwd=cwd)
    if result.returncode == 0:
        print(f"✓ Success")
        if result.stdout.strip():
            print(f"  {result.stdout.strip()}")
    else:
        print(f"✗ Failed: {result.stderr}")
    return result.returncode == 0

def update_dashboard_now():
    """Force dashboard update with latest data."""
    root = Path(__file__).parent
    deployment = root / "deployment"
    
    print("\n🚀 FORCING DASHBOARD UPDATE")
    print("=" * 50)
    
    # 1. Read the latest data
    with open(root / "data" / "last_update.json", 'r') as f:
        data = json.load(f)
    
    print(f"\n📊 Latest Data:")
    print(f"   Total PRs: {data['total_prs']}")
    print(f"   Last Update: {data['last_update_time']}")
    
    # 2. Update the HTML file to show correct date
    print(f"\n📝 Updating HTML dashboard...")
    
    html_file = deployment / "index.html"
    with open(html_file, 'r', encoding='utf-8') as f:
        html_content = f.read()
    
    # Find and update the updateTime in the JavaScript
    import re
    
    # Update the updateTime variable
    new_update_time = data['last_update_time']
    html_content = re.sub(
        r'const updateTime = "[^"]*"',
        f'const updateTime = "{new_update_time}"',
        html_content
    )
    
    # Also add a cache buster
    timestamp = int(datetime.now().timestamp())
    if '?refresh=' in html_content:
        html_content = re.sub(r'\?refresh=\d+', f'?refresh={timestamp}', html_content)
    else:
        html_content = re.sub(r'(data/pr_metrics_all_prs\.csv)', rf'\1?refresh={timestamp}', html_content)
        html_content = re.sub(r'(data/last_update\.json)', rf'\1?refresh={timestamp}', html_content)
    
    # Write updated HTML
    with open(html_file, 'w', encoding='utf-8') as f:
        f.write(html_content)
    
    print(f"✓ HTML updated with latest timestamp")
    
    # 3. Copy latest data files
    print(f"\n📁 Copying latest data files...")
    os.chdir(root)
    
    if os.name == 'nt':  # Windows
        run_cmd('xcopy /Y /E "data\\*.*" "deployment\\data\\"')
    else:  # Unix/Linux
        run_cmd('cp -r data/* deployment/data/')
    
    # 4. Commit and push to gh-pages
    print(f"\n🔄 Pushing to GitHub Pages...")
    os.chdir(deployment)
    
    # Configure git
    run_cmd('git config user.name "aviv-fathallahelmasri"')
    run_cmd('git config user.email "aviv.fathalla.helmasri@asideas.de"')
    
    # Add all changes
    run_cmd("git add -A")
    
    # Check if there are changes
    result = subprocess.run("git status --porcelain", shell=True, capture_output=True, text=True)
    if result.stdout.strip():
        # Commit changes
        commit_msg = f"Force update: {data['total_prs']} PRs - {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"
        run_cmd(f'git commit -m "{commit_msg}"')
        
        # Push to gh-pages
        run_cmd("git push origin main:gh-pages --force")
        
        print(f"\n✅ SUCCESS! Dashboard updated with {data['total_prs']} PRs")
    else:
        print(f"\n⚠️  No changes detected. Forcing a push anyway...")
        # Create a dummy change to force update
        dummy_file = deployment / ".force_update"
        with open(dummy_file, 'w') as f:
            f.write(str(timestamp))
        
        run_cmd("git add .force_update")
        run_cmd(f'git commit -m "Force cache refresh - {timestamp}"')
        run_cmd("git push origin main:gh-pages --force")
    
    print(f"\n" + "=" * 50)
    print(f"📊 Dashboard: https://aviv-fathallahelmasri.github.io/pr-analytics-dashboard/")
    print(f"⏱️  GitHub Pages usually updates in 1-2 minutes")
    print(f"\n💡 To force browser refresh:")
    print(f"   • Press Ctrl+F5 (Windows) or Cmd+Shift+R (Mac)")
    print(f"   • Or add ?v={timestamp} to the URL")
    print(f"   • Or open in incognito/private mode")

if __name__ == "__main__":
    update_dashboard_now()
