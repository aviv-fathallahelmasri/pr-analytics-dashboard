#!/usr/bin/env python3
"""
Check GitHub Pages Deployment Status
====================================
Verifies the deployment status and provides troubleshooting steps.
"""

import requests
import json
from datetime import datetime
from pathlib import Path

def check_deployment_status():
    """Check the live deployment status."""
    print("=== GitHub Pages Deployment Status Check ===")
    print("=" * 50)
    
    # Check local data first
    print("\n1. Local Data Status:")
    local_update_file = Path("data/last_update.json")
    if local_update_file.exists():
        with open(local_update_file, 'r') as f:
            local_data = json.load(f)
        print(f"   - Total PRs: {local_data['total_prs']}")
        print(f"   - Last Update: {local_data['last_update_time']}")
    else:
        print("   ❌ Local data file not found!")
    
    # Check deployment directory data
    print("\n2. Deployment Directory Status:")
    deployment_update_file = Path("deployment/data/last_update.json")
    if deployment_update_file.exists():
        with open(deployment_update_file, 'r') as f:
            deployment_data = json.load(f)
        print(f"   - Total PRs: {deployment_data['total_prs']}")
        print(f"   - Last Update: {deployment_data['last_update_time']}")
    else:
        print("   ❌ Deployment data file not found!")
    
    # Check live dashboard data
    print("\n3. Live Dashboard Status:")
    try:
        # Try to fetch the live data
        response = requests.get(
            "https://aviv-fathallahelmasri.github.io/pr-analytics-dashboard/data/last_update.json",
            timeout=10
        )
        
        if response.status_code == 200:
            live_data = response.json()
            print(f"   - Total PRs: {live_data['total_prs']}")
            print(f"   - Last Update: {live_data['last_update_time']}")
            
            # Compare with local
            if local_update_file.exists():
                if live_data['total_prs'] == local_data['total_prs']:
                    print("\n   ✅ Live dashboard is up to date!")
                else:
                    print(f"\n   ⚠️  Live dashboard is behind by {local_data['total_prs'] - live_data['total_prs']} PRs")
        else:
            print(f"   ❌ Failed to fetch live data (Status: {response.status_code})")
    except Exception as e:
        print(f"   ❌ Error checking live dashboard: {str(e)}")
    
    # Check GitHub API for deployment status
    print("\n4. GitHub Deployment Status:")
    try:
        # Check repository deployments
        response = requests.get(
            "https://api.github.com/repos/aviv-fathallahelmasri/pr-analytics-dashboard/pages",
            headers={"Accept": "application/vnd.github.v3+json"}
        )
        
        if response.status_code == 200:
            pages_info = response.json()
            print(f"   - Status: {pages_info.get('status', 'Unknown')}")
            print(f"   - URL: {pages_info.get('html_url', 'Not available')}")
            
            if 'source' in pages_info:
                print(f"   - Branch: {pages_info['source'].get('branch', 'Unknown')}")
        else:
            print("   ℹ️  Could not fetch GitHub Pages info (might need authentication)")
    except Exception as e:
        print(f"   ❌ Error checking GitHub API: {str(e)}")
    
    # Provide troubleshooting steps
    print("\n" + "=" * 50)
    print("📋 Troubleshooting Steps:")
    print("\n1. If live dashboard is not updating:")
    print("   - Wait 2-10 minutes (GitHub Pages cache)")
    print("   - Force refresh browser (Ctrl+F5)")
    print("   - Clear browser cache")
    
    print("\n2. To force a new deployment:")
    print("   - Run: python fix_github_pages_deployment.py")
    
    print("\n3. To check GitHub Actions:")
    print("   - Visit: https://github.com/aviv-fathallahelmasri/pr-analytics-dashboard/actions")
    
    print("\n4. To verify gh-pages branch:")
    print("   - Visit: https://github.com/aviv-fathallahelmasri/pr-analytics-dashboard/tree/gh-pages")

if __name__ == "__main__":
    check_deployment_status()
