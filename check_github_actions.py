#!/usr/bin/env python3
"""
GitHub Actions Diagnostic Script
Checks the status of GitHub Actions workflows and recent runs.
"""

import os
import json
import requests
from datetime import datetime, timezone
from dotenv import load_dotenv

# Load environment variables
load_dotenv('config/.env')

def check_workflow_status():
    """Check the status of GitHub Actions workflows."""
    token = os.getenv('GITHUB_TOKEN')
    owner, repo = 'aviv-fathallahelmasri', 'pr-analytics-dashboard'
    
    headers = {
        'Authorization': f'token {token}',
        'Accept': 'application/vnd.github.v3+json'
    }
    
    print("=== GitHub Actions Workflow Status ===")
    print(f"Repository: {owner}/{repo}")
    print(f"Current time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')} (local)")
    print(f"UTC time: {datetime.now(timezone.utc).strftime('%Y-%m-%d %H:%M:%S')} (UTC)")
    
    # Check workflows
    print("\n1. Checking available workflows...")
    url = f"https://api.github.com/repos/{owner}/{repo}/actions/workflows"
    response = requests.get(url, headers=headers)
    
    if response.status_code == 200:
        workflows = response.json()
        if workflows['total_count'] == 0:
            print("❌ No workflows found in the repository")
            print("   The daily-update.yml workflow needs to be pushed to GitHub")
        else:
            for workflow in workflows['workflows']:
                print(f"   ✓ {workflow['name']} ({workflow['state']})")
                print(f"     Path: {workflow['path']}")
                print(f"     ID: {workflow['id']}")
                
                # Check recent runs
                runs_url = f"https://api.github.com/repos/{owner}/{repo}/actions/workflows/{workflow['id']}/runs?per_page=5"
                runs_response = requests.get(runs_url, headers=headers)
                if runs_response.status_code == 200:
                    runs = runs_response.json()
                    print(f"     Recent runs:")
                    if runs['total_count'] == 0:
                        print(f"       No runs found")
                    else:
                        for run in runs['workflow_runs'][:3]:
                            run_time = datetime.fromisoformat(run['created_at'].replace('Z', '+00:00'))
                            print(f"       - {run_time.strftime('%Y-%m-%d %H:%M:%S')} UTC: {run['status']} ({run['conclusion'] or 'in progress'})")
    else:
        print(f"❌ Failed to fetch workflows: {response.status_code}")
        print(f"   Response: {response.text}")
    
    # Check if the workflow file exists locally
    print("\n2. Checking local workflow file...")
    workflow_path = ".github/workflows/daily-update.yml"
    if os.path.exists(workflow_path):
        print(f"   ✓ Workflow file exists locally: {workflow_path}")
        print("   ⚠️  Remember to push this file to GitHub for it to work!")
    else:
        print(f"   ❌ Workflow file not found locally: {workflow_path}")
    
    # Check last data update
    print("\n3. Checking last data update...")
    if os.path.exists("data/last_update.json"):
        with open("data/last_update.json", "r") as f:
            last_update = json.load(f)
        update_time = datetime.fromisoformat(last_update['last_update_time'])
        time_diff = datetime.now(timezone.utc) - update_time.astimezone(timezone.utc)
        hours_ago = time_diff.total_seconds() / 3600
        print(f"   Last update: {update_time.strftime('%Y-%m-%d %H:%M:%S')} ({update_time.tzinfo})")
        print(f"   Time since last update: {hours_ago:.1f} hours")
        if hours_ago > 25:
            print(f"   ⚠️  Dashboard hasn't been updated in over 24 hours!")
    else:
        print(f"   ❌ No last_update.json file found")
    
    print("\n=== Recommendations ===")
    print("1. Push the workflow file to GitHub:")
    print("   git add .github/workflows/daily-update.yml")
    print("   git commit -m 'Add daily update workflow'")
    print("   git push origin main")
    print("\n2. Ensure the PERSONAL_ACCESS_TOKEN secret is set in GitHub:")
    print("   Go to Settings → Secrets and variables → Actions")
    print("   Add a secret named PERSONAL_ACCESS_TOKEN with your GitHub token")
    print("\n3. To test the workflow manually:")
    print("   Go to Actions tab → Daily PR Analytics Update → Run workflow")
    print("\n4. For immediate update, run:")
    print("   python manual_update.py")

if __name__ == "__main__":
    check_workflow_status()
