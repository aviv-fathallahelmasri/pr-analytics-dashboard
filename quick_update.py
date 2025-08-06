#!/usr/bin/env python3
"""
Quick Update Script - Simplified version to fetch and update PR data
"""

import os
import sys
import json
from datetime import datetime
from pathlib import Path

def check_requirements():
    """Check if required packages are installed"""
    missing = []
    
    try:
        import github
    except ImportError:
        missing.append("PyGithub")
    
    try:
        import pandas
    except ImportError:
        missing.append("pandas")
    
    try:
        import requests
    except ImportError:
        missing.append("requests")
    
    if missing:
        print(f"❌ Missing required packages: {', '.join(missing)}")
        print(f"Please run: pip install {' '.join(missing)}")
        return False
    
    return True

def quick_update():
    """Run a quick update of the PR data"""
    print("="*70)
    print("QUICK PR DATA UPDATE")
    print("="*70)
    
    # Check requirements first
    if not check_requirements():
        return False
    
    # Now import what we need
    from github import Github
    import pandas as pd
    import shutil
    
    # Check for GitHub token
    github_token = os.environ.get('GITHUB_TOKEN')
    if not github_token:
        print("\n❌ GITHUB_TOKEN not set!")
        print("Please set it using:")
        print("  set GITHUB_TOKEN=your_github_token_here")
        return False
    
    print(f"\n✓ GitHub token found")
    
    # Project paths
    project_root = Path.cwd()
    data_dir = project_root / "data"
    deployment_dir = project_root / "deployment"
    deployment_data_dir = deployment_dir / "data"
    
    # Ensure directories exist
    data_dir.mkdir(exist_ok=True)
    deployment_data_dir.mkdir(parents=True, exist_ok=True)
    
    try:
        # Connect to GitHub
        print("\n📥 Fetching PR data from GitHub...")
        g = Github(github_token)
        repo = g.get_repo("axel-springer-kugawana/aviv_data_collection_contracts")
        
        # Fetch PRs
        all_prs = []
        
        # Get open PRs
        print("  Fetching open PRs...")
        open_prs = list(repo.get_pulls(state='open'))
        print(f"  ✓ Found {len(open_prs)} open PRs")
        
        # Get closed PRs (limited to recent ones for speed)
        print("  Fetching closed PRs...")
        closed_prs = list(repo.get_pulls(state='closed', sort='created', direction='desc')[:200])
        print(f"  ✓ Found {len(closed_prs)} closed PRs")
        
        # Process all PRs
        for pr in open_prs + closed_prs:
            pr_data = {
                'number': pr.number,
                'title': pr.title,
                'state': pr.state,
                'created_at': pr.created_at.isoformat() if pr.created_at else None,
                'closed_at': pr.closed_at.isoformat() if pr.closed_at else None,
                'merged_at': pr.merged_at.isoformat() if pr.merged_at else None,
                'author': pr.user.login if pr.user else 'unknown',
                'labels': str([label.name for label in pr.labels]),
                'additions': pr.additions,
                'deletions': pr.deletions,
                'changed_files': pr.changed_files,
                'url': pr.html_url
            }
            all_prs.append(pr_data)
        
        # Save to CSV
        df = pd.DataFrame(all_prs)
        csv_path = data_dir / "pr_metrics_all_prs.csv"
        df.to_csv(csv_path, index=False)
        print(f"\n✓ Saved {len(df)} PRs to CSV")
        
        # Create metadata
        metadata = {
            'last_updated': datetime.now().isoformat(),
            'total_prs': len(df),
            'open_prs': len(open_prs),
            'closed_prs': len(closed_prs),
            'repository': 'axel-springer-kugawana/aviv_data_collection_contracts'
        }
        
        metadata_path = data_dir / "metadata.json"
        with open(metadata_path, 'w') as f:
            json.dump(metadata, f, indent=2)
        print(f"✓ Updated metadata")
        
        # Copy to deployment
        print("\n📤 Syncing to deployment folder...")
        for file in data_dir.glob("*"):
            if file.is_file():
                shutil.copy2(file, deployment_data_dir / file.name)
                print(f"  ✓ Copied {file.name}")
        
        print("\n✅ UPDATE COMPLETE!")
        print(f"Total PRs: {len(df)}")
        print(f"Last updated: {metadata['last_updated']}")
        
        print("\n📋 Next steps:")
        print("1. Commit and push changes:")
        print("   git add -A")
        print("   git commit -m \"Update PR data\"")
        print("   git push")
        print("2. Wait 2-3 minutes for GitHub Pages to update")
        print("3. Check your dashboard at:")
        print("   https://aviv-fathallahelmasri.github.io/pr-analytics-dashboard/")
        
        return True
        
    except Exception as e:
        print(f"\n❌ Error: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    success = quick_update()
    sys.exit(0 if success else 1)
