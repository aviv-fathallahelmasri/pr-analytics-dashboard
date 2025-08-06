#!/usr/bin/env python3
"""
GitHub PR Analytics - Simple Data Fetching Module
=================================================
Fetches PR data from GitHub API for analytics dashboard.
"""

import os
import json
import sys
from datetime import datetime
from pathlib import Path
from typing import List, Dict, Any

# Try to import required libraries
try:
    from github import Github
    import pandas as pd
except ImportError as e:
    print(f"Error: Missing required library: {e}")
    print("Installing required packages...")
    os.system("pip install PyGithub pandas python-dotenv")
    from github import Github
    import pandas as pd

def load_config():
    """Load configuration from environment or .env file"""
    # Try to load from .env file first
    env_file = Path(__file__).parent.parent / '.env'
    if env_file.exists():
        with open(env_file, 'r') as f:
            for line in f:
                if '=' in line and not line.startswith('#'):
                    key, value = line.strip().split('=', 1)
                    os.environ[key] = value
    
    # Get configuration
    config = {
        'github_token': os.environ.get('GITHUB_TOKEN'),
        'target_repo': os.environ.get('GITHUB_REPO', 'axel-springer-kugawana/aviv_data_collection_contracts')
    }
    
    return config

def fetch_pr_data(repo_name: str, github_token: str) -> pd.DataFrame:
    """Fetch all PR data from the repository"""
    print(f"Connecting to GitHub repository: {repo_name}")
    
    # Initialize GitHub client
    g = Github(github_token)
    repo = g.get_repo(repo_name)
    
    all_prs = []
    
    # Fetch open PRs
    print("Fetching open PRs...")
    open_count = 0
    for pr in repo.get_pulls(state='open'):
        pr_data = extract_pr_data(pr)
        all_prs.append(pr_data)
        open_count += 1
    print(f"  Found {open_count} open PRs")
    
    # Fetch closed PRs
    print("Fetching closed PRs...")
    closed_count = 0
    for pr in repo.get_pulls(state='closed', sort='created', direction='desc'):
        pr_data = extract_pr_data(pr)
        all_prs.append(pr_data)
        closed_count += 1
        if closed_count % 50 == 0:
            print(f"  Processed {closed_count} closed PRs...")
    print(f"  Found {closed_count} closed PRs")
    
    # Convert to DataFrame
    df = pd.DataFrame(all_prs)
    
    # Process dates and calculate metrics
    if not df.empty:
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
    
    print(f"Total PRs fetched: {len(df)}")
    return df

def extract_pr_data(pr) -> Dict[str, Any]:
    """Extract relevant data from a PR object"""
    return {
        'number': pr.number,
        'title': pr.title,
        'state': pr.state,
        'created_at': pr.created_at.isoformat() if pr.created_at else None,
        'closed_at': pr.closed_at.isoformat() if pr.closed_at else None,
        'merged_at': pr.merged_at.isoformat() if pr.merged_at else None,
        'author': pr.user.login if pr.user else 'unknown',
        'labels': ','.join([label.name for label in pr.labels]),
        'additions': pr.additions,
        'deletions': pr.deletions,
        'changed_files': pr.changed_files,
        'comments': pr.comments,
        'review_comments': pr.review_comments,
        'commits': pr.commits,
        'draft': pr.draft,
        'base_branch': pr.base.ref,
        'head_branch': pr.head.ref if pr.head else 'unknown',
        'url': pr.html_url
    }

def save_data(df: pd.DataFrame, output_dir: Path):
    """Save PR data and metadata"""
    # Ensure output directory exists
    output_dir.mkdir(parents=True, exist_ok=True)
    
    # Save CSV
    csv_path = output_dir / 'pr_metrics_all_prs.csv'
    df.to_csv(csv_path, index=False)
    print(f"Saved data to {csv_path}")
    
    # Create metadata
    metadata = {
        'last_updated': datetime.now().isoformat(),
        'total_prs': len(df),
        'open_prs': len(df[df['state'] == 'open']) if not df.empty else 0,
        'closed_prs': len(df[df['state'] == 'closed']) if not df.empty else 0,
        'merged_prs': len(df[df['merged_at'].notna()]) if not df.empty else 0,
        'unique_authors': df['author'].nunique() if not df.empty else 0,
        'fetch_timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    }
    
    # Save metadata
    metadata_path = output_dir / 'metadata.json'
    with open(metadata_path, 'w') as f:
        json.dump(metadata, f, indent=2)
    print(f"Saved metadata to {metadata_path}")
    
    # Save update timestamp
    update_path = output_dir / 'last_update.json'
    with open(update_path, 'w') as f:
        json.dump({
            'timestamp': datetime.now().isoformat(),
            'pr_count': len(df)
        }, f, indent=2)

def main():
    """Main execution function"""
    print("="*60)
    print("GitHub PR Analytics - Data Fetch")
    print("="*60)
    
    # Load configuration
    config = load_config()
    
    if not config['github_token']:
        print("ERROR: GitHub token not found!")
        print("Please set GITHUB_TOKEN environment variable or add it to .env file")
        sys.exit(1)
    
    try:
        # Fetch PR data
        df = fetch_pr_data(config['target_repo'], config['github_token'])
        
        # Save to data directory
        project_root = Path(__file__).parent.parent
        data_dir = project_root / 'data'
        save_data(df, data_dir)
        
        print("="*60)
        print("✅ Data fetch completed successfully!")
        print(f"Total PRs: {len(df)}")
        print("="*60)
        
        return 0
        
    except Exception as e:
        print(f"ERROR: Failed to fetch data: {e}")
        import traceback
        traceback.print_exc()
        return 1

if __name__ == "__main__":
    sys.exit(main())
