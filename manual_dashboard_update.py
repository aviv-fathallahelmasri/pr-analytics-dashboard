#!/usr/bin/env python3
"""
Manual Dashboard Update Script for GitHub PR Analytics
======================================================

This script provides a complete manual update process for the GitHub PR Analytics Dashboard.
It fetches the latest data, processes it, and deploys the updated dashboard to GitHub Pages.

Author: Aviv
Date: 2025-01-24
Purpose: Manual trigger for dashboard updates with comprehensive logging and error handling
"""

import os
import sys
import subprocess
import shutil
import json
from datetime import datetime, timezone
from pathlib import Path
import logging

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('manual_update.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)


class DashboardUpdater:
    """
    Handles the complete dashboard update process.
    """
    
    def __init__(self):
        """Initialize the updater with project paths."""
        self.project_root = Path(__file__).parent
        self.data_dir = self.project_root / "data"
        self.deployment_dir = self.project_root / "deployment"
        self.src_dir = self.project_root / "src"
        
    def run_command(self, cmd: str, cwd: Path = None) -> tuple[bool, str]:
        """
        Execute a command and return success status and output.
        
        Args:
            cmd: Command to execute
            cwd: Working directory (defaults to project root)
            
        Returns:
            Tuple of (success: bool, output: str)
        """
        if cwd is None:
            cwd = self.project_root
            
        logger.info(f"Executing: {cmd}")
        try:
            result = subprocess.run(
                cmd, 
                shell=True, 
                capture_output=True, 
                text=True, 
                cwd=str(cwd)
            )
            
            if result.returncode == 0:
                logger.info("Command succeeded")
                return True, result.stdout
            else:
                logger.error(f"Command failed: {result.stderr}")
                return False, result.stderr
        except Exception as e:
            logger.error(f"Exception running command: {str(e)}")
            return False, str(e)
    
    def fetch_latest_data(self) -> bool:
        """
        Fetch the latest PR data from GitHub API.
        
        Returns:
            bool: Success status
        """
        logger.info("=" * 60)
        logger.info("STEP 1: Fetching latest PR data from GitHub")
        logger.info("=" * 60)
        
        # Check if fetch script exists
        fetch_script = self.src_dir / "fetch_pr_data.py"
        if not fetch_script.exists():
            logger.error(f"Fetch script not found: {fetch_script}")
            return False
        
        # Run the fetch script
        success, output = self.run_command(f'"{sys.executable}" "{fetch_script}"')
        
        if success:
            logger.info("✅ Successfully fetched latest PR data")
            
            # Check if data files were created
            metrics_file = self.data_dir / "pr_metrics_all_prs.csv"
            update_file = self.data_dir / "last_update.json"
            
            if metrics_file.exists() and update_file.exists():
                # Log update summary
                with open(update_file, 'r') as f:
                    update_info = json.load(f)
                logger.info(f"Total PRs: {update_info.get('total_prs', 'Unknown')}")
                logger.info(f"Last update: {update_info.get('last_update_time', 'Unknown')}")
                return True
            else:
                logger.error("Data files not created after fetch")
                return False
        else:
            logger.error("Failed to fetch PR data")
            return False
    
    def prepare_deployment_files(self) -> bool:
        """
        Prepare files for deployment by copying them to the deployment directory.
        
        Returns:
            bool: Success status
        """
        logger.info("=" * 60)
        logger.info("STEP 2: Preparing deployment files")
        logger.info("=" * 60)
        
        try:
            # Ensure deployment data directory exists
            deployment_data_dir = self.deployment_dir / "data"
            deployment_data_dir.mkdir(parents=True, exist_ok=True)
            
            # Copy data files
            files_to_copy = [
                ("data/pr_metrics_all_prs.csv", "deployment/data/pr_metrics_all_prs.csv"),
                ("data/last_update.json", "deployment/data/last_update.json")
            ]
            
            for src, dst in files_to_copy:
                src_path = self.project_root / src
                dst_path = self.project_root / dst
                
                if src_path.exists():
                    shutil.copy2(src_path, dst_path)
                    logger.info(f"✅ Copied: {src} -> {dst}")
                else:
                    logger.error(f"Source file not found: {src}")
                    return False
            
            # Check if index.html needs to be copied from root
            root_index = self.project_root / "index.html"
            deployment_index = self.deployment_dir / "index.html"
            
            if root_index.exists() and root_index.stat().st_mtime > deployment_index.stat().st_mtime:
                shutil.copy2(root_index, deployment_index)
                logger.info("✅ Updated index.html in deployment directory")
            
            return True
            
        except Exception as e:
            logger.error(f"Error preparing deployment files: {str(e)}")
            return False
    
    def commit_data_updates(self) -> bool:
        """
        Commit updated data files to the main branch.
        
        Returns:
            bool: Success status
        """
        logger.info("=" * 60)
        logger.info("STEP 3: Committing data updates to main branch")
        logger.info("=" * 60)
        
        # Check git status
        success, output = self.run_command("git status --porcelain data/")
        
        if success and output.strip():
            logger.info("Changes detected in data directory")
            
            # Add data files
            success, _ = self.run_command("git add data/")
            if not success:
                logger.error("Failed to add data files")
                return False
            
            # Commit with timestamp
            commit_msg = f"Manual update: PR analytics data [{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] [skip ci]"
            success, _ = self.run_command(f'git commit -m "{commit_msg}"')
            
            if success:
                logger.info("✅ Committed data updates")
                
                # Push to main branch
                success, _ = self.run_command("git push origin main")
                if success:
                    logger.info("✅ Pushed updates to main branch")
                    return True
                else:
                    logger.error("Failed to push to main branch")
                    return False
            else:
                logger.warning("No changes to commit (data might be up to date)")
                return True
        else:
            logger.info("No changes detected in data directory")
            return True
    
    def deploy_to_github_pages(self) -> bool:
        """
        Deploy the updated dashboard to GitHub Pages.
        
        Returns:
            bool: Success status
        """
        logger.info("=" * 60)
        logger.info("STEP 4: Deploying to GitHub Pages")
        logger.info("=" * 60)
        
        try:
            # Navigate to deployment directory
            os.chdir(self.deployment_dir)
            logger.info(f"Changed to deployment directory: {os.getcwd()}")
            
            # Configure git
            self.run_command('git config user.name "aviv-fathallahelmasri"')
            self.run_command('git config user.email "aviv.fathalla.helmasri@asideas.de"')
            
            # Check current branch
            success, branch = self.run_command("git rev-parse --abbrev-ref HEAD")
            logger.info(f"Current branch: {branch.strip()}")
            
            # Add all changes
            success, _ = self.run_command("git add -A")
            if not success:
                logger.error("Failed to add files for deployment")
                return False
            
            # Check if there are changes
            success, status = self.run_command("git status --porcelain")
            
            if success and status.strip():
                # Commit changes
                timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                commit_msg = f"Manual deployment: Update dashboard {timestamp} [skip ci]"
                success, _ = self.run_command(f'git commit -m "{commit_msg}"')
                
                if success:
                    logger.info("✅ Created deployment commit")
                    
                    # Push to gh-pages
                    success, _ = self.run_command("git push origin main:gh-pages --force")
                    
                    if success:
                        logger.info("✅ Successfully deployed to GitHub Pages")
                        return True
                    else:
                        logger.error("Failed to push to gh-pages branch")
                        return False
                else:
                    logger.error("Failed to commit deployment changes")
                    return False
            else:
                logger.info("No changes to deploy")
                return True
                
        except Exception as e:
            logger.error(f"Deployment error: {str(e)}")
            return False
        finally:
            # Return to project root
            os.chdir(self.project_root)
            logger.info("Returned to project root")
    
    def verify_update(self) -> None:
        """Verify the update was successful and provide summary."""
        logger.info("=" * 60)
        logger.info("VERIFICATION & SUMMARY")
        logger.info("=" * 60)
        
        # Check last update time
        update_file = self.data_dir / "last_update.json"
        if update_file.exists():
            with open(update_file, 'r') as f:
                update_info = json.load(f)
            
            logger.info(f"✅ Last update: {update_info.get('last_update_time', 'Unknown')}")
            logger.info(f"✅ Total PRs: {update_info.get('total_prs', 'Unknown')}")
            logger.info(f"✅ Repository: {update_info.get('repository', 'Unknown')}")
        
        logger.info("\n📊 Dashboard URL: https://aviv-fathallahelmasri.github.io/pr-analytics-dashboard/")
        logger.info("⏰ Note: GitHub Pages may take 2-5 minutes to reflect changes")
        logger.info("🔄 You can check deployment status at: https://github.com/aviv-fathallahelmasri/pr-analytics-dashboard/actions")
    
    def run_full_update(self) -> bool:
        """
        Execute the complete update process.
        
        Returns:
            bool: Overall success status
        """
        logger.info("🚀 Starting Manual Dashboard Update")
        logger.info(f"Time: {datetime.now(timezone.utc).strftime('%Y-%m-%d %H:%M:%S UTC')}")
        logger.info("=" * 60)
        
        # Step 1: Fetch latest data
        if not self.fetch_latest_data():
            logger.error("❌ Failed at Step 1: Fetching data")
            return False
        
        # Step 2: Prepare deployment files
        if not self.prepare_deployment_files():
            logger.error("❌ Failed at Step 2: Preparing deployment files")
            return False
        
        # Step 3: Commit data updates
        if not self.commit_data_updates():
            logger.error("❌ Failed at Step 3: Committing data updates")
            return False
        
        # Step 4: Deploy to GitHub Pages
        if not self.deploy_to_github_pages():
            logger.error("❌ Failed at Step 4: Deploying to GitHub Pages")
            return False
        
        # Verify and summarize
        self.verify_update()
        
        logger.info("\n✅ Manual update completed successfully!")
        return True


def main():
    """Main entry point for the manual update script."""
    updater = DashboardUpdater()
    
    try:
        success = updater.run_full_update()
        sys.exit(0 if success else 1)
    except KeyboardInterrupt:
        logger.warning("\n⚠️  Update interrupted by user")
        sys.exit(1)
    except Exception as e:
        logger.error(f"\n❌ Unexpected error: {str(e)}")
        sys.exit(1)


if __name__ == "__main__":
    main()
