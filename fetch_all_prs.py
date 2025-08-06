#!/usr/bin/env python3
"""
Complete PR Fetch - Gets ALL PRs from the repository without limits
Automatically loads GitHub token from .env file
"""

import os
import sys
import json
from datetime import datetime
from pathlib import Path

def load_github_token():
    """Load GitHub token from .env file or environment"""
    # First, try to load from .env file
    env_file = Path(".env")
    if env_file.exists():
        with open(env_file, 'r') as f:
            for line in f:
                if line.startswith('GITHUB_TOKEN='):
                    token = line.strip().split('=', 1)[1]
                    os.environ['GITHUB_TOKEN'] = token
                    print("✓ Loaded GitHub token from .env file")
                    return token
    
    # If not in .env, check environment variable
    token = os.environ.get('GITHUB_TOKEN')
    if token:
        print("✓ Using GitHub token from environment")
        return token
    
    return None

def fetch_all_prs():
    """Fetch ALL PRs from the repository"""
    print("="*70)
    print("FETCHING ALL PR DATA - NO LIMITS")
    print("="*70)
    
    # Check requirements
    try:
        from github import Github
        import pandas as pd
        import shutil
    except ImportError as e:
        print(f"❌ Missing required package: {e}")
        print("Please run: pip install PyGithub pandas")
        return False
    
    # Load GitHub token
    github_token = load_github_token()
    if not github_token:
        print("\n❌ GITHUB_TOKEN not found!")
        print("Token should be in .env file or set as environment variable")
        return False
    
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
        print("\n📥 Connecting to GitHub...")
        g = Github(github_token)
        repo = g.get_repo("axel-springer-kugawana/aviv_data_collection_contracts")
        print(f"✓ Connected to repository")
        
        all_prs = []
        
        # Fetch ALL open PRs
        print("\n🔍 Fetching ALL open PRs...")
        open_count = 0
        for pr in repo.get_pulls(state='open'):
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
                'draft': pr.draft,
                'base_branch': pr.base.ref,
                'head_branch': pr.head.ref if pr.head else 'unknown',
                'url': pr.html_url
            }
            all_prs.append(pr_data)
            open_count += 1
            
            # Show progress
            if open_count % 10 == 0:
                print(f"  Processed {open_count} open PRs...")
        
        print(f"✓ Found {open_count} open PRs")
        
        # Fetch ALL closed PRs
        print("\n🔍 Fetching ALL closed PRs (this may take a minute)...")
        closed_count = 0
        for pr in repo.get_pulls(state='closed', sort='created', direction='desc'):
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
                'draft': pr.draft,
                'base_branch': pr.base.ref,
                'head_branch': pr.head.ref if pr.head else 'unknown',
                'url': pr.html_url
            }
            all_prs.append(pr_data)
            closed_count += 1
            
            # Show progress every 25 PRs
            if closed_count % 25 == 0:
                print(f"  Processed {closed_count} closed PRs...")
        
        print(f"✓ Found {closed_count} closed PRs")
        
        # Create DataFrame
        df = pd.DataFrame(all_prs)
        
        # Add calculated fields
        if not df.empty:
            # Convert date columns
            df['created_at'] = pd.to_datetime(df['created_at'])
            df['closed_at'] = pd.to_datetime(df['closed_at'])
            df['merged_at'] = pd.to_datetime(df['merged_at'])
            
            # Calculate merge time
            df['merge_time_hours'] = None
            merged_mask = df['merged_at'].notna()
            if merged_mask.any():
                df.loc[merged_mask, 'merge_time_hours'] = (
                    (df.loc[merged_mask, 'merged_at'] - df.loc[merged_mask, 'created_at'])
                    .dt.total_seconds() / 3600
                )
            
            # Add status field
            df['status'] = df.apply(lambda row: 
                'merged' if pd.notna(row['merged_at']) else
                'closed' if row['state'] == 'closed' else
                'open', axis=1)
            
            # Check for data_contract label
            df['has_data_contract'] = df['labels'].apply(
                lambda labels: 'data_contract' in labels.lower() if isinstance(labels, str) else False
            )
        
        # Save to CSV
        csv_path = data_dir / "pr_metrics_all_prs.csv"
        df.to_csv(csv_path, index=False)
        print(f"\n✓ Saved {len(df)} PRs to {csv_path}")
        
        # Calculate statistics
        merged_count = len(df[df['merged_at'].notna()]) if not df.empty else 0
        
        # Create comprehensive metadata
        metadata = {
            'last_updated': datetime.now().isoformat(),
            'total_prs': len(df),
            'open_prs': open_count,
            'closed_prs': closed_count,
            'merged_prs': merged_count,
            'unique_authors': df['author'].nunique() if not df.empty else 0,
            'repository': 'axel-springer-kugawana/aviv_data_collection_contracts',
            'fetch_complete': True,
            'fetch_timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        }
        
        # Save metadata
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
        
        # Summary
        print("\n" + "="*70)
        print("✅ COMPLETE FETCH SUCCESSFUL!")
        print("="*70)
        print(f"📊 Total PRs fetched: {len(df)}")
        print(f"   • Open: {open_count}")
        print(f"   • Closed: {closed_count}")
        print(f"   • Merged: {merged_count}")
        print(f"   • Unique authors: {metadata['unique_authors']}")
        print(f"📅 Last updated: {metadata['fetch_timestamp']}")
        
        # Calculate some quick stats
        if merged_count > 0:
            merge_rate = (merged_count / closed_count * 100) if closed_count > 0 else 0
            avg_merge_time = df.loc[df['merge_time_hours'].notna(), 'merge_time_hours'].mean()
            print(f"\n📈 Quick Stats:")
            print(f"   • Merge rate: {merge_rate:.1f}%")
            print(f"   • Avg merge time: {avg_merge_time:.1f} hours")
        
        print("\n📋 Next steps to deploy:")
        print("1. Commit and push changes:")
        print("   git add -A")
        print('   git commit -m "Update: Complete PR data fetch - %d PRs"' % len(df))
        print("   git push")
        print("\n2. Wait 2-3 minutes for GitHub Pages to update")
        print("\n3. Check your dashboard at:")
        print("   https://aviv-fathallahelmasri.github.io/pr-analytics-dashboard/")
        
        return True
        
    except Exception as e:
        print(f"\n❌ Error: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    success = fetch_all_prs()
    sys.exit(0 if success else 1)
