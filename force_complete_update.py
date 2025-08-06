#!/usr/bin/env python3
"""
Force Complete Update for PR Analytics Dashboard
================================================
This script forces a complete update of your PR Analytics Dashboard,
fetching the latest data and ensuring it's deployed to GitHub Pages.

Author: Assistant for Aviv
Date: 2025-08-06
Purpose: Ensure latest changes are captured and displayed on the dashboard
"""

import os
import sys
import json
import shutil
import subprocess
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional

# Import the GitHub and pandas modules we need
try:
    from github import Github
    import pandas as pd
    import requests
except ImportError as e:
    print(f"Error: Missing required module: {e}")
    print("Please run: pip install PyGithub pandas requests")
    sys.exit(1)

class ForceCompleteUpdate:
    """Handle forced complete update of PR Analytics Dashboard"""
    
    def __init__(self):
        self.project_root = Path("C:/Users/FElmasri/Desktop/github-pr-analytics")
        self.data_dir = self.project_root / "data"
        self.deployment_dir = self.project_root / "deployment"
        self.deployment_data_dir = self.deployment_dir / "data"
        
        # Repository information
        self.target_repo = "axel-springer-kugawana/aviv_data_collection_contracts"
        self.dashboard_repo = "aviv-fathallahelmasri/pr-analytics-dashboard"
        
        # Ensure directories exist
        self.data_dir.mkdir(exist_ok=True)
        self.deployment_data_dir.mkdir(parents=True, exist_ok=True)
        
        print("🚀 Force Complete Update Initialized")
        print(f"📁 Project Root: {self.project_root}")
        print(f"🎯 Target Repo: {self.target_repo}")
        print(f"📊 Dashboard Repo: {self.dashboard_repo}")
        print("="*70)
    
    def fetch_latest_pr_data(self) -> bool:
        """Fetch the latest PR data from GitHub"""
        print("\n📥 FETCHING LATEST PR DATA")
        print("-"*40)
        
        # Check for GitHub token
        github_token = os.environ.get('GITHUB_TOKEN')
        if not github_token:
            print("❌ GITHUB_TOKEN not set!")
            print("Please set it using: set GITHUB_TOKEN=your_token_here")
            return False
        
        try:
            # Initialize GitHub client
            g = Github(github_token)
            repo = g.get_repo(self.target_repo)
            
            print(f"✓ Connected to GitHub repository: {self.target_repo}")
            
            # Fetch all PRs
            all_prs = []
            print("🔍 Fetching PRs...")
            
            # Get both open and closed PRs
            for state in ['open', 'closed']:
                prs = repo.get_pulls(state=state, sort='created', direction='desc')
                count = 0
                for pr in prs:
                    pr_data = {
                        'number': pr.number,
                        'title': pr.title,
                        'state': pr.state,
                        'created_at': pr.created_at.isoformat() if pr.created_at else None,
                        'closed_at': pr.closed_at.isoformat() if pr.closed_at else None,
                        'merged_at': pr.merged_at.isoformat() if pr.merged_at else None,
                        'author': pr.user.login if pr.user else 'unknown',
                        'labels': [label.name for label in pr.labels],
                        'reviewers': [reviewer.login for reviewer in pr.requested_reviewers],
                        'additions': pr.additions,
                        'deletions': pr.deletions,
                        'changed_files': pr.changed_files,
                        'comments': pr.comments,
                        'review_comments': pr.review_comments,
                        'commits': pr.commits,
                        'mergeable': pr.mergeable,
                        'base_branch': pr.base.ref,
                        'head_branch': pr.head.ref if pr.head else 'unknown',
                        'draft': pr.draft,
                        'url': pr.html_url
                    }
                    all_prs.append(pr_data)
                    count += 1
                    
                    # Show progress every 10 PRs
                    if count % 10 == 0:
                        print(f"  Processed {count} {state} PRs...")
                
                print(f"✓ Fetched {count} {state} PRs")
            
            # Convert to DataFrame
            df = pd.DataFrame(all_prs)
            
            # Add calculated metrics
            if not df.empty:
                df['created_at'] = pd.to_datetime(df['created_at'])
                df['closed_at'] = pd.to_datetime(df['closed_at'])
                df['merged_at'] = pd.to_datetime(df['merged_at'])
                
                # Calculate merge time for merged PRs
                df['merge_time_hours'] = None
                merged_mask = df['merged_at'].notna()
                df.loc[merged_mask, 'merge_time_hours'] = (
                    (df.loc[merged_mask, 'merged_at'] - df.loc[merged_mask, 'created_at'])
                    .dt.total_seconds() / 3600
                )
                
                # Add status categories
                df['status'] = df.apply(lambda row: 
                    'merged' if pd.notna(row['merged_at']) else
                    'closed' if row['state'] == 'closed' else
                    'open', axis=1)
                
                # Check for data_contract label
                df['has_data_contract'] = df['labels'].apply(
                    lambda labels: 'data_contract' in [l.lower() for l in labels]
                )
            
            # Save to CSV
            csv_path = self.data_dir / "pr_metrics_all_prs.csv"
            df.to_csv(csv_path, index=False)
            print(f"✓ Saved {len(df)} PRs to {csv_path}")
            
            # Create metadata
            metadata = {
                'last_updated': datetime.now().isoformat(),
                'total_prs': len(df),
                'open_prs': len(df[df['state'] == 'open']) if not df.empty else 0,
                'closed_prs': len(df[df['state'] == 'closed']) if not df.empty else 0,
                'merged_prs': len(df[df['merged_at'].notna()]) if not df.empty else 0,
                'data_contract_prs': len(df[df['has_data_contract'] == True]) if 'has_data_contract' in df.columns else 0,
                'unique_authors': df['author'].nunique() if not df.empty else 0,
                'repository': self.target_repo,
                'update_source': 'force_complete_update.py'
            }
            
            # Save metadata
            metadata_path = self.data_dir / "metadata.json"
            with open(metadata_path, 'w') as f:
                json.dump(metadata, f, indent=2)
            print(f"✓ Updated metadata: {metadata_path}")
            
            # Create summary statistics
            if not df.empty:
                stats = {
                    'total_prs': len(df),
                    'merge_rate': (len(df[df['merged_at'].notna()]) / len(df) * 100) if len(df) > 0 else 0,
                    'avg_merge_time_hours': float(df['merge_time_hours'].mean()) if 'merge_time_hours' in df.columns and df['merge_time_hours'].notna().any() else 0,
                    'median_merge_time_hours': float(df['merge_time_hours'].median()) if 'merge_time_hours' in df.columns and df['merge_time_hours'].notna().any() else 0,
                    'active_contributors': df['author'].nunique(),
                    'most_active_author': df['author'].value_counts().index[0] if not df.empty else 'N/A',
                    'data_contract_percentage': (len(df[df['has_data_contract'] == True]) / len(df) * 100) if 'has_data_contract' in df.columns else 0
                }
                
                stats_path = self.data_dir / "summary_stats.json"
                with open(stats_path, 'w') as f:
                    json.dump(stats, f, indent=2)
                print(f"✓ Generated summary statistics: {stats_path}")
            
            print(f"\n📊 Data Fetch Complete!")
            print(f"  Total PRs: {metadata['total_prs']}")
            print(f"  Open: {metadata['open_prs']}")
            print(f"  Merged: {metadata['merged_prs']}")
            print(f"  Authors: {metadata['unique_authors']}")
            
            return True
            
        except Exception as e:
            print(f"❌ Error fetching PR data: {e}")
            import traceback
            traceback.print_exc()
            return False
    
    def sync_to_deployment(self) -> bool:
        """Sync data files to deployment directory"""
        print("\n📤 SYNCING DATA TO DEPLOYMENT")
        print("-"*40)
        
        try:
            # Ensure deployment data directory exists
            self.deployment_data_dir.mkdir(parents=True, exist_ok=True)
            
            # Copy all data files
            files_copied = 0
            for file_path in self.data_dir.glob("*"):
                if file_path.is_file():
                    dest_path = self.deployment_data_dir / file_path.name
                    shutil.copy2(file_path, dest_path)
                    print(f"✓ Copied: {file_path.name}")
                    files_copied += 1
            
            print(f"\n✓ Synced {files_copied} files to deployment/data/")
            
            # Verify critical files
            critical_files = ['pr_metrics_all_prs.csv', 'metadata.json']
            for filename in critical_files:
                if (self.deployment_data_dir / filename).exists():
                    print(f"✓ Verified: {filename}")
                else:
                    print(f"❌ Missing: {filename}")
                    return False
            
            return True
            
        except Exception as e:
            print(f"❌ Error syncing to deployment: {e}")
            return False
    
    def update_dashboard_timestamp(self) -> bool:
        """Update the dashboard HTML with current timestamp"""
        print("\n🕐 UPDATING DASHBOARD TIMESTAMP")
        print("-"*40)
        
        try:
            index_path = self.deployment_dir / "index.html"
            
            if not index_path.exists():
                print(f"❌ Dashboard file not found: {index_path}")
                return False
            
            # Read current content
            with open(index_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # Update last updated timestamp if it exists in the HTML
            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            
            # Check if there's a last updated element to update
            if 'id="lastUpdated"' in content or 'class="last-updated"' in content:
                # This would need to be done via JavaScript since we're loading data dynamically
                print(f"✓ Dashboard will show latest data timestamp from metadata.json")
            else:
                print("ℹ Dashboard uses dynamic timestamp from metadata")
            
            # Add cache-busting query parameter to data URLs if needed
            cache_buster = f"?v={datetime.now().strftime('%Y%m%d%H%M%S')}"
            
            # Update data file references to include cache buster
            if 'pr_metrics_all_prs.csv' in content and '?v=' not in content:
                content = content.replace(
                    'pr_metrics_all_prs.csv',
                    f'pr_metrics_all_prs.csv{cache_buster}'
                )
                content = content.replace(
                    'metadata.json',
                    f'metadata.json{cache_buster}'
                )
                
                # Save updated content
                with open(index_path, 'w', encoding='utf-8') as f:
                    f.write(content)
                
                print(f"✓ Added cache buster: {cache_buster}")
            else:
                print("ℹ Dashboard already has cache management")
            
            return True
            
        except Exception as e:
            print(f"❌ Error updating dashboard: {e}")
            return False
    
    def commit_and_push(self) -> bool:
        """Commit and push changes to GitHub"""
        print("\n📤 COMMITTING AND PUSHING TO GITHUB")
        print("-"*40)
        
        try:
            os.chdir(self.project_root)
            
            # Configure git
            subprocess.run(['git', 'config', 'user.name', 'Aviv Fathalla Helmasri'], check=True)
            subprocess.run(['git', 'config', 'user.email', 'aviv.fathallahelmasri@axelspringer.com'], check=True)
            
            # Add all changes
            subprocess.run(['git', 'add', 'data/', 'deployment/'], check=True)
            print("✓ Staged changes")
            
            # Check if there are changes to commit
            result = subprocess.run(['git', 'status', '--porcelain'], capture_output=True, text=True)
            
            if result.stdout.strip():
                # Commit changes
                commit_message = f"Force update: Latest PR data - {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"
                subprocess.run(['git', 'commit', '-m', commit_message], check=True)
                print(f"✓ Committed: {commit_message}")
                
                # Push to GitHub
                subprocess.run(['git', 'push', 'origin', 'main'], check=True)
                print("✓ Pushed to GitHub")
                
                return True
            else:
                print("ℹ No changes to commit")
                return True
                
        except subprocess.CalledProcessError as e:
            print(f"❌ Git error: {e}")
            return False
        except Exception as e:
            print(f"❌ Error during commit/push: {e}")
            return False
    
    def verify_deployment(self) -> bool:
        """Verify the deployment is working"""
        print("\n🔍 VERIFYING DEPLOYMENT")
        print("-"*40)
        
        dashboard_url = f"https://aviv-fathallahelmasri.github.io/pr-analytics-dashboard/"
        
        try:
            response = requests.get(dashboard_url, timeout=10)
            
            if response.status_code == 200:
                print(f"✓ Dashboard is accessible: {dashboard_url}")
                
                # Check for data endpoint
                data_url = f"https://aviv-fathallahelmasri.github.io/pr-analytics-dashboard/data/metadata.json"
                data_response = requests.get(data_url, timeout=10)
                
                if data_response.status_code == 200:
                    metadata = data_response.json()
                    print(f"✓ Data endpoint working")
                    print(f"  Last updated: {metadata.get('last_updated', 'Unknown')}")
                    print(f"  Total PRs: {metadata.get('total_prs', 0)}")
                else:
                    print(f"⚠ Data endpoint returned: {data_response.status_code}")
                    print("  Note: GitHub Pages may take a few minutes to update")
                
                return True
            else:
                print(f"❌ Dashboard returned status: {response.status_code}")
                return False
                
        except Exception as e:
            print(f"❌ Error verifying deployment: {e}")
            return False
    
    def run_complete_update(self) -> bool:
        """Run the complete update process"""
        print("\n" + "="*70)
        print("STARTING FORCE COMPLETE UPDATE")
        print("="*70)
        
        steps = [
            ("Fetch Latest PR Data", self.fetch_latest_pr_data),
            ("Sync to Deployment", self.sync_to_deployment),
            ("Update Dashboard", self.update_dashboard_timestamp),
            ("Commit and Push", self.commit_and_push),
            ("Verify Deployment", self.verify_deployment)
        ]
        
        success = True
        for step_name, step_func in steps:
            print(f"\n🔄 Step: {step_name}")
            if not step_func():
                print(f"❌ Failed at step: {step_name}")
                success = False
                break
        
        print("\n" + "="*70)
        if success:
            print("✅ FORCE UPDATE COMPLETED SUCCESSFULLY!")
            print("\n📊 Next Steps:")
            print("1. Wait 2-3 minutes for GitHub Pages to update")
            print("2. Check your dashboard at:")
            print(f"   https://aviv-fathallahelmasri.github.io/pr-analytics-dashboard/")
            print("3. Verify the data is current by checking the 'Last Updated' timestamp")
        else:
            print("❌ FORCE UPDATE FAILED")
            print("\nTroubleshooting:")
            print("1. Ensure GITHUB_TOKEN is set correctly")
            print("2. Check your internet connection")
            print("3. Verify git credentials are configured")
            print("4. Check the error messages above for details")
        
        print("="*70)
        
        return success

def main():
    """Main execution"""
    try:
        # Ensure we're in the correct directory
        current_dir = os.getcwd()
        project_dir = "C:/Users/FElmasri/Desktop/github-pr-analytics"
        
        # Only change directory if needed
        if not current_dir.replace('\\', '/').endswith('github-pr-analytics'):
            if os.path.exists(project_dir):
                os.chdir(project_dir)
                print(f"Changed to project directory: {project_dir}")
            else:
                print(f"Error: Project directory not found: {project_dir}")
                return 1
        
        # Run the update
        updater = ForceCompleteUpdate()
        success = updater.run_complete_update()
        
        return 0 if success else 1
        
    except Exception as e:
        print(f"\n❌ Unexpected error: {e}")
        import traceback
        traceback.print_exc()
        return 1

if __name__ == "__main__":
    sys.exit(main())
