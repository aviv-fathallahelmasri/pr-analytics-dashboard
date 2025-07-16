"""
GitHub PR Analytics - Core Data Fetching Module
==============================================

This is where the magic happens! This module handles all the heavy lifting
of fetching PR data from GitHub's API and transforming it into beautiful,
analyzable data.

Author: Aviv
Created: 2025
Purpose: Complete automation of PR analytics - because who has time for manual work?
"""

import os
import json
import time
from datetime import datetime, timezone
from typing import List, Dict, Any, Optional
import pandas as pd
from github import Github, GithubException
from dotenv import load_dotenv
import logging
from pathlib import Path

# Load environment variables - keeping secrets secret!
load_dotenv()

# Set up logging - I like to know what's happening
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


class PRAnalyticsFetcher:
    """
    The main workhorse for fetching and processing PR data.
    
    This class handles everything from API authentication to data transformation.
    Built with love and a strong desire to never manually collect PR data again!
    """
    
    def __init__(self, github_token: str, target_repo: str):
        """
        Initialize the PR fetcher with credentials and config.
        
        Args:
            github_token: Your precious GitHub token (keep it secret!)
            target_repo: The repo to analyze (format: 'owner/repo')
        
        Why these params?
        - Token: Because GitHub API without auth = 60 requests/hour = sadness
        - Repo: We need to know what to analyze, right?
        """
        self.github = Github(github_token)
        self.target_repo = target_repo
        self.repo = None
        self._validate_setup()
        
    def _validate_setup(self) -> None:
        """
        Make sure everything is configured correctly before we start.
        
        Better to fail fast than waste time on a broken setup!
        This checks:
        - Token validity
        - Repository access
        - API rate limits
        """
        try:
            # Test the connection and access
            self.repo = self.github.get_repo(self.target_repo)
            rate_limit = self.github.get_rate_limit()
            
            logger.info(f"✅ Connected to GitHub API successfully!")
            logger.info(f"📂 Repository: {self.repo.full_name}")
            logger.info(f"🔑 API calls remaining: {rate_limit.core.remaining}")
            
            # Warn if we're running low on API calls
            if rate_limit.core.remaining < 100:
                logger.warning(f"⚠️  Low API rate limit: {rate_limit.core.remaining} calls left!")
                
        except GithubException as e:
            logger.error(f"❌ GitHub API error: {str(e)}")
            raise
        except Exception as e:
            logger.error(f"❌ Unexpected error during setup: {str(e)}")
            raise
    
    def fetch_all_prs(self) -> List[Dict[str, Any]]:
        """
        Fetch ALL pull requests from the repository.
        
        This is the main method that does all the work. It:
        1. Fetches PRs in batches (pagination)
        2. Extracts all the juicy details
        3. Handles rate limiting gracefully
        4. Returns everything in a nice, clean format
        
        Returns:
            List of PR dictionaries with all the metrics we care about
            
        Why fetch everything?
        - Historical data is valuable
        - Trends need complete data
        - Storage is cheap, insights are priceless
        """
        logger.info(f"🚀 Starting PR data fetch for {self.target_repo}")
        
        all_prs = []
        page = 0
        
        try:
            # Get all PRs - both open and closed
            # We want EVERYTHING for complete analytics
            pulls = self.repo.get_pulls(state='all', sort='created', direction='desc')
            
            for pr in pulls:
                page += 1
                
                # Show progress every 10 PRs so we know it's working
                if page % 10 == 0:
                    logger.info(f"  📊 Processed {page} PRs...")
                
                # Extract all the data we need
                pr_data = self._extract_pr_data(pr)
                all_prs.append(pr_data)
                
                # Be nice to GitHub's API - rate limiting is real!
                if page % 100 == 0:
                    self._check_rate_limit()
            
            logger.info(f"✅ Successfully fetched {len(all_prs)} PRs!")
            return all_prs
            
        except GithubException as e:
            logger.error(f"❌ Error fetching PRs: {str(e)}")
            raise
        except Exception as e:
            logger.error(f"❌ Unexpected error: {str(e)}")
            raise
    
    def _extract_pr_data(self, pr) -> Dict[str, Any]:
        """
        Extract all the meaningful data from a PR object.
        
        This is where we transform GitHub's PR object into our
        beautiful, flat dictionary with all the metrics we need.
        
        Args:
            pr: PyGithub PR object
            
        Returns:
            Dictionary with all PR data we care about
            
        Why these specific fields?
        - Number & Title: Basic identification
        - Author: Who's doing the work?
        - Timestamps: When things happened
        - State & Merge status: What happened to it?
        - File changes: How big was it?
        - Reviews: Was it properly reviewed?
        """
        # Calculate merge time if PR was merged
        merge_time_hours = None
        if pr.merged_at:
            # I love timedelta math - it just works!
            time_to_merge = pr.merged_at - pr.created_at
            merge_time_hours = round(time_to_merge.total_seconds() / 3600, 2)
        
        # Get review information - this is where quality lives
        reviews = list(pr.get_reviews())
        review_comments = list(pr.get_review_comments())
        
        # Count different types of reviews
        approvals = sum(1 for r in reviews if r.state == 'APPROVED')
        change_requests = sum(1 for r in reviews if r.state == 'CHANGES_REQUESTED')
        
        # Build our beautiful data dictionary
        return {
            # Basic info
            'PR_Number': pr.number,
            'Title': pr.title,
            'Author': pr.user.login,
            
            # Timestamps - everything is better with timestamps
            'Created_At': pr.created_at.isoformat(),
            'Merged_At': pr.merged_at.isoformat() if pr.merged_at else '',
            'Updated_At': pr.updated_at.isoformat(),
            
            # Status info
            'State': pr.state,
            'Is_Merged': pr.merged,
            
            # Size metrics - smaller PRs = happier reviewers
            'Changed_Files': pr.changed_files,
            'Additions': pr.additions,
            'Deletions': pr.deletions,
            
            # Time metrics
            'Time_To_Merge_Hours': merge_time_hours if merge_time_hours else '',
            
            # Labels - for the organized folks
            'Labels': ','.join([label.name for label in pr.labels]),
            
            # Review metrics - where collaboration happens
            'Requested_Reviewers': ','.join([r.login for r in pr.requested_reviewers]),
            'Final_Reviewers': ','.join(list(set([r.user.login for r in reviews]))),
            'Total_Reviews': len(reviews),
            'Approvals': approvals,
            'Change_Requests': change_requests,
            'Review_Comments': ', '.join([f"{c.user.login}: {c.body[:50]}..." 
                                         for c in review_comments[:3]])  # First 3 comments
        }
    
    def _check_rate_limit(self) -> None:
        """
        Check GitHub API rate limit and pause if needed.
        
        GitHub gives us 5000 requests/hour with authentication.
        This method makes sure we don't hit that limit and get
        temporarily banned. Because getting banned is no fun!
        """
        rate_limit = self.github.get_rate_limit()
        remaining = rate_limit.core.remaining
        
        if remaining < 50:
            # We're running low - time to take a break
            reset_time = rate_limit.core.reset
            wait_time = (reset_time - datetime.now(timezone.utc)).total_seconds()
            
            logger.warning(f"⏸️  Rate limit low ({remaining} left). Waiting {wait_time:.0f} seconds...")
            time.sleep(wait_time + 5)  # Add 5 seconds buffer
            logger.info("▶️  Resuming data fetch...")
    
    def save_to_csv(self, pr_data: List[Dict[str, Any]], output_path: str = 'data/pr_metrics_all_prs.csv') -> None:
        """
        Save PR data to a beautiful CSV file.
        
        Args:
            pr_data: List of PR dictionaries
            output_path: Where to save the CSV
            
        Why CSV?
        - Human readable (can open in Excel)
        - Git-friendly (text diffs work)
        - Universal (everything can read CSV)
        - Fast (for our data size)
        """
        # Make sure the directory exists
        Path(output_path).parent.mkdir(parents=True, exist_ok=True)
        
        # Convert to DataFrame - pandas makes this so easy
        df = pd.DataFrame(pr_data)
        
        # Sort by PR number descending (newest first)
        df = df.sort_values('PR_Number', ascending=False)
        
        # Save to CSV with nice formatting
        df.to_csv(output_path, index=False, encoding='utf-8')
        logger.info(f"💾 Saved {len(df)} PRs to {output_path}")
        
        # Also save metadata for the dashboard
        self._save_metadata(len(pr_data))
    
    def _save_metadata(self, total_prs: int) -> None:
        """
        Save metadata about the last update.
        
        This helps the dashboard know when data was last refreshed
        and provides quick stats without parsing the entire CSV.
        
        Args:
            total_prs: Number of PRs processed
            
        Why metadata?
        - Quick dashboard loading (no need to parse CSV for basic info)
        - Update tracking (when did we last update?)
        - Debugging (what happened during last run?)
        """
        metadata = {
            'last_update_time': datetime.now(timezone.utc).isoformat(),
            'total_prs': total_prs,
            'repository': self.target_repo,
            'update_type': 'full'  # Could be 'incremental' in future
        }
        
        metadata_path = 'data/last_update.json'
        Path(metadata_path).parent.mkdir(parents=True, exist_ok=True)
        
        with open(metadata_path, 'w', encoding='utf-8') as f:
            json.dump(metadata, f, indent=2)
        
        logger.info(f"📋 Saved metadata to {metadata_path}")


def main():
    """
    Main entry point for the script.
    
    This is what runs when you execute the script directly.
    It handles all the setup, execution, and error handling.
    
    Why a main function?
    - Clean entry point
    - Easy to test
    - Clear flow
    """
    logger.info("=" * 50)
    logger.info("🚀 GitHub PR Analytics - Data Fetcher")
    logger.info("=" * 50)
    
    # Get configuration from environment
    github_token = os.getenv('GITHUB_TOKEN')
    target_repo = os.getenv('GITHUB_REPO')
    
    # Validate we have what we need
    if not github_token:
        logger.error("❌ GITHUB_TOKEN not found in environment variables!")
        logger.error("💡 Create a .env file with GITHUB_TOKEN=your_token_here")
        return 1
    
    if not target_repo:
        logger.error("❌ GITHUB_REPO not found in environment variables!")
        logger.error("💡 Add GITHUB_REPO=owner/repo to your .env file")
        return 1
    
    try:
        # Create fetcher and do the work
        fetcher = PRAnalyticsFetcher(github_token, target_repo)
        pr_data = fetcher.fetch_all_prs()
        fetcher.save_to_csv(pr_data)
        
        # Quick summary of what we got
        logger.info("\n📊 Summary:")
        logger.info(f"  Total PRs: {len(pr_data)}")
        
        if pr_data:
            merged_prs = [pr for pr in pr_data if pr['Is_Merged']]
            merge_rate = (len(merged_prs) / len(pr_data)) * 100
            logger.info(f"  Merged: {len(merged_prs)} ({merge_rate:.1f}%)")
            
            open_prs = [pr for pr in pr_data if pr['State'] == 'open']
            logger.info(f"  Currently Open: {len(open_prs)}")
        
        logger.info("\n✅ Data fetch completed successfully!")
        return 0
        
    except Exception as e:
        logger.error(f"\n❌ Fatal error: {str(e)}")
        logger.error("💡 Check your token permissions and repository access")
        return 1


if __name__ == "__main__":
    # This only runs when script is executed directly
    # Not when imported as a module - clever Python!
    exit(main())
