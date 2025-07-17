#!/usr/bin/env python3
"""
Verify GitHub Pages deployment status
"""

import json
import requests
import time
from datetime import datetime

def check_deployment():
    """Check if GitHub Pages has the latest data"""
    
    print("🔍 Checking GitHub Pages deployment status...\n")
    
    # Add timestamp to bypass cache
    timestamp = int(time.time())
    
    # URLs to check
    urls = {
        'dashboard': f'https://aviv-fathallahelmasri.github.io/pr-analytics-dashboard/?t={timestamp}',
        'csv_data': f'https://aviv-fathallahelmasri.github.io/pr-analytics-dashboard/data/pr_metrics_all_prs.csv?t={timestamp}',
        'json_data': f'https://aviv-fathallahelmasri.github.io/pr-analytics-dashboard/data/last_update.json?t={timestamp}'
    }
    
    # Check JSON metadata
    try:
        response = requests.get(urls['json_data'], headers={'Cache-Control': 'no-cache'})
        if response.status_code == 200:
            data = response.json()
            print(f"✅ JSON Data accessible")
            print(f"   Total PRs: {data['total_prs']}")
            print(f"   Last Update: {data['last_update_time']}")
            
            # Parse update time
            update_time = datetime.fromisoformat(data['last_update_time'].replace('Z', '+00:00'))
            current_time = datetime.now(update_time.tzinfo)
            time_diff = current_time - update_time
            
            print(f"   Time since update: {time_diff.total_seconds() / 60:.1f} minutes ago")
            
            if data['total_prs'] == 214:
                print("\n✅ GitHub Pages has the LATEST data (214 PRs)!")
                print("   If your browser still shows old data, it's a browser cache issue.")
                print("   Solution: Press Ctrl+F5 or Cmd+Shift+R to force refresh")
            else:
                print(f"\n⚠️  GitHub Pages still shows old data ({data['total_prs']} PRs)")
                print("   The deployment might still be propagating...")
        else:
            print(f"❌ Could not fetch JSON data: HTTP {response.status_code}")
    except Exception as e:
        print(f"❌ Error checking deployment: {str(e)}")
    
    # Check CSV data
    try:
        response = requests.get(urls['csv_data'], headers={'Cache-Control': 'no-cache'})
        if response.status_code == 200:
            lines = response.text.strip().split('\n')
            pr_count = len(lines) - 1  # Subtract header
            print(f"\n📊 CSV Data Check:")
            print(f"   PR count in CSV: {pr_count}")
            
            # Get the first few lines to check latest PRs
            if len(lines) > 2:
                print(f"   Latest PR in CSV: {lines[1].split(',')[0]}")
    except Exception as e:
        print(f"❌ Error checking CSV: {str(e)}")
    
    print("\n💡 Direct Links (with cache bypass):")
    print(f"   Dashboard: {urls['dashboard']}")
    print(f"   CSV Data: {urls['csv_data']}")
    print(f"   JSON Data: {urls['json_data']}")
    
    print("\n📝 Instructions:")
    print("1. Click the dashboard link above")
    print("2. If it still shows old data, clear your browser cache")
    print("3. Or open in an incognito/private window")
    print("4. GitHub Pages can take up to 10 minutes to fully propagate")

if __name__ == "__main__":
    check_deployment()
