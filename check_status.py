#!/usr/bin/env python3
"""
Quick status check for GitHub PR Analytics Dashboard
"""

import json
import os
from datetime import datetime, timezone
from pathlib import Path

def check_status():
    """Check the current status of the dashboard data"""
    
    print("=== GitHub PR Analytics Dashboard Status Check ===\n")
    
    # Check if data directory exists
    if not os.path.exists('data'):
        print("❌ Data directory not found!")
        return
    
    # Check last update
    if os.path.exists('data/last_update.json'):
        with open('data/last_update.json', 'r') as f:
            update_info = json.load(f)
        
        print("📊 Last Update Information:")
        print(f"   Time: {update_info['last_update_time']}")
        print(f"   Total PRs: {update_info['total_prs']}")
        print(f"   Repository: {update_info['repository']}")
        print(f"   Update Type: {update_info['update_type']}")
        
        # Calculate time since update
        last_update_str = update_info['last_update_time']
        if last_update_str.endswith('Z'):
            last_update_str = last_update_str[:-1] + '+00:00'
        
        last_update_time = datetime.fromisoformat(last_update_str)
        current_time = datetime.now(timezone.utc)
        time_diff = current_time - last_update_time
        hours_ago = time_diff.total_seconds() / 3600
        
        print(f"\n⏰ Time since last update: {hours_ago:.1f} hours")
        
        if hours_ago > 24:
            print("⚠️  Data is more than 24 hours old - update recommended!")
        else:
            print("✅ Data is up to date")
    else:
        print("❌ No update information found!")
    
    # Check CSV file
    csv_path = 'data/pr_metrics_all_prs.csv'
    if os.path.exists(csv_path):
        file_size = os.path.getsize(csv_path) / 1024  # KB
        print(f"\n📁 Data file size: {file_size:.1f} KB")
        
        # Count lines (PRs)
        with open(csv_path, 'r', encoding='utf-8') as f:
            line_count = sum(1 for line in f) - 1  # Subtract header
        print(f"   Number of PRs in CSV: {line_count}")
    else:
        print("\n❌ CSV data file not found!")
    
    # Check deployment directory
    if os.path.exists('deployment/data/pr_metrics_all_prs.csv'):
        print("\n✅ Deployment data exists")
        
        # Check if deployment is in sync
        if os.path.exists('deployment/data/last_update.json'):
            with open('deployment/data/last_update.json', 'r') as f:
                deploy_info = json.load(f)
            
            if deploy_info['last_update_time'] == update_info['last_update_time']:
                print("✅ Deployment is in sync with source data")
            else:
                print("⚠️  Deployment data is out of sync!")
    else:
        print("\n⚠️  Deployment data not found")
    
    # Check environment file
    if os.path.exists('.env'):
        print("\n✅ Environment file exists")
    else:
        print("\n⚠️  No .env file found - GitHub token may not be configured")
    
    print("\n=== End of Status Check ===")

if __name__ == "__main__":
    check_status()
