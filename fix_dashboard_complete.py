#!/usr/bin/env python3
"""
Fix Dashboard Timestamp and Ensure Correct Deployment
=====================================================
"""

import json
import os
import subprocess
import shutil
from datetime import datetime
from pathlib import Path

def run_cmd(cmd):
    print(f"$ {cmd}")
    result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
    if result.stdout:
        print(result.stdout.strip())
    return result.returncode == 0

print("=== Fixing Dashboard Timestamp and Data ===\n")

# Step 1: First ensure we have the latest data in main branch
print("1. Fetching latest PR data...")
os.system(f'"{sys.executable}" src/fetch_pr_data.py')

# Step 2: Read the current data
data_file = Path("data/last_update.json")
with open(data_file, 'r') as f:
    data = json.load(f)

print(f"\nCurrent data shows:")
print(f"- Total PRs: {data['total_prs']}")
print(f"- Last Update: {data['last_update_time']}")

# Step 3: Copy ALL files from main to deployment
print("\n2. Syncing all files to deployment directory...")

# Ensure deployment has latest index.html from main
if Path("index.html").exists():
    shutil.copy2("index.html", "deployment/index.html")
    print("✅ Copied index.html")

# Copy data files
shutil.copy2("data/pr_metrics_all_prs.csv", "deployment/data/pr_metrics_all_prs.csv")
shutil.copy2("data/last_update.json", "deployment/data/last_update.json")
print("✅ Copied data files")

# Step 4: Switch to deployment and push to gh-pages
os.chdir("deployment")
print("\n3. Updating gh-pages branch...")

# Make sure we're on gh-pages
run_cmd("git checkout gh-pages")

# Pull latest
run_cmd("git pull origin gh-pages")

# Add all changes
run_cmd("git add -A")

# Commit with clear message
timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
commit_msg = f"Update dashboard - {data['total_prs']} PRs - {timestamp}"
run_cmd(f'git commit -m "{commit_msg}"')

# Push to gh-pages
run_cmd("git push origin gh-pages")

# Step 5: Also update main branch deployment
print("\n4. Ensuring main branch deployment is in sync...")
run_cmd("git checkout main")
run_cmd("git add -A")
run_cmd(f'git commit -m "Sync deployment directory"')
run_cmd("git push origin main")

# Return to gh-pages
run_cmd("git checkout gh-pages")

os.chdir("..")

print("\n" + "=" * 50)
print("✅ Update Complete!")
print(f"\n📊 Dashboard should show:")
print(f"   - Total PRs: {data['total_prs']} (when 'All PRs' is selected)")
print(f"   - Last Update: {data['last_update_time']}")
print("\n⚠️  IMPORTANT: Make sure to select 'All PRs' in the PR Type filter!")
print("\n🔗 Direct link: https://aviv-fathallahelmasri.github.io/pr-analytics-dashboard/")
print("💡 If timestamp still shows old date, clear browser cache (Ctrl+F5)")

# Create a verification script
with open("verify_deployment.py", "w") as f:
    f.write("""import requests
import json

print("Checking live dashboard data...")
try:
    response = requests.get("https://aviv-fathallahelmasri.github.io/pr-analytics-dashboard/data/last_update.json")
    if response.status_code == 200:
        data = response.json()
        print(f"Live dashboard shows: {data['total_prs']} PRs")
        print(f"Last updated: {data['last_update_time']}")
    else:
        print(f"Error: {response.status_code}")
except Exception as e:
    print(f"Error: {e}")
""")

print("\n📝 Created verify_deployment.py - run it to check live data")
