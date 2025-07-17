#!/usr/bin/env python3
"""
GitHub PR Analytics - Complete System Verification Script
========================================================

This script performs a comprehensive end-to-end verification of your 
GitHub PR Analytics system to ensure everything is working correctly.

Features:
- Validates all system components and dependencies
- Tests data fetching and processing
- Checks automation scheduling
- Verifies dashboard functionality
- Tests deployment pipeline
- Provides detailed health report

Usage:
    python verify_system.py [--verbose] [--fix] [--test-fetch]

Options:
    --verbose       Enable detailed logging
    --fix          Attempt to fix common issues
    --test-fetch   Test data fetching from GitHub API
"""

import os
import sys
import json
import requests
import subprocess
import csv
from datetime import datetime, timezone
from pathlib import Path
from typing import Dict, List, Tuple, Optional
import argparse

# Add project root to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

class PRAnalyticsVerifier:
    """Complete system verification for GitHub PR Analytics"""
    
    def __init__(self, verbose: bool = False, fix_issues: bool = False):
        self.verbose = verbose
        self.fix_issues = fix_issues
        self.issues_found = []
        self.checks_passed = []
        
    def log(self, message: str, level: str = "INFO") -> None:
        """Log a message with timestamp"""
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        if level == "ERROR":
            print(f"[{timestamp}] ❌ {message}")
            self.issues_found.append(message)
        elif level == "WARNING":
            print(f"[{timestamp}] ⚠️ {message}")
        elif level == "SUCCESS":
            print(f"[{timestamp}] ✅ {message}")
            self.checks_passed.append(message)
        else:
            if self.verbose:
                print(f"[{timestamp}] ℹ️ {message}")
    
    def check_file_structure(self) -> bool:
        """Verify all required files and directories exist"""
        self.log("Checking file structure...")
        
        required_files = [
            "src/fetch_pr_data.py",
            "src/update_and_deploy.py",
            "deployment/index.html",
            "deployment/css/style.css",
            "deployment/js/dashboard.js",
            "config/requirements.txt",
            ".github/workflows/daily-update.yml",
            "docs/README.md",
            "docs/SETUP.md"
        ]
        
        required_dirs = [
            "src/",
            "deployment/",
            "deployment/data/",
            "deployment/css/",
            "deployment/js/",
            "data/",
            "config/",
            ".github/workflows/",
            "docs/"
        ]
        
        # Check directories
        for dir_path in required_dirs:
            if not os.path.exists(dir_path):
                self.log(f"Missing directory: {dir_path}", "ERROR")
                if self.fix_issues:
                    os.makedirs(dir_path, exist_ok=True)
                    self.log(f"Created directory: {dir_path}", "SUCCESS")
        
        # Check files
        missing_files = []
        for file_path in required_files:
            if not os.path.exists(file_path):
                missing_files.append(file_path)
                self.log(f"Missing file: {file_path}", "ERROR")
        
        if not missing_files:
            self.log("File structure check passed", "SUCCESS")
            return True
        else:
            self.log(f"Missing {len(missing_files)} required files", "ERROR")
            return False
    
    def check_environment_setup(self) -> bool:
        """Verify environment variables and configuration"""
        self.log("Checking environment setup...")
        
        required_env_vars = [
            "GITHUB_TOKEN",
            "GITHUB_REPO"
        ]
        
        # Check .env file
        env_file = Path(".env")
        if env_file.exists():
            self.log("Found .env file", "SUCCESS")
            
            # Read and validate env file
            with open(env_file, 'r') as f:
                env_content = f.read()
                
            for var in required_env_vars:
                if var not in env_content:
                    self.log(f"Missing environment variable in .env: {var}", "ERROR")
                else:
                    self.log(f"Found environment variable: {var}", "SUCCESS")
        else:
            self.log("No .env file found", "WARNING")
        
        # Check system environment variables
        for var in required_env_vars:
            if var in os.environ:
                self.log(f"System environment variable found: {var}", "SUCCESS")
            else:
                self.log(f"System environment variable missing: {var}", "WARNING")
        
        return True
    
    def check_data_files(self) -> bool:
        """Verify data files exist and are valid"""
        self.log("Checking data files...")
        
        data_files = [
            "data/pr_metrics_all_prs.csv",
            "data/last_update.json",
            "deployment/data/pr_metrics_all_prs.csv",
            "deployment/data/last_update.json"
        ]
        
        all_valid = True
        
        for file_path in data_files:
            if not os.path.exists(file_path):
                self.log(f"Missing data file: {file_path}", "ERROR")
                all_valid = False
                continue
            
            # Check file size
            file_size = os.path.getsize(file_path)
            if file_size == 0:
                self.log(f"Empty data file: {file_path}", "ERROR")
                all_valid = False
                continue
            
            self.log(f"Valid data file: {file_path} ({file_size:,} bytes)", "SUCCESS")
            
            # Validate CSV files
            if file_path.endswith('.csv'):
                try:
                    with open(file_path, 'r', encoding='utf-8') as f:
                        reader = csv.reader(f)
                        rows = list(reader)
                        if len(rows) < 2:  # At least header + 1 data row
                            self.log(f"CSV file has insufficient data: {file_path}", "ERROR")
                            all_valid = False
                        else:
                            self.log(f"CSV file has {len(rows)-1} data rows", "SUCCESS")
                except Exception as e:
                    self.log(f"Error reading CSV file {file_path}: {e}", "ERROR")
                    all_valid = False
            
            # Validate JSON files
            elif file_path.endswith('.json'):
                try:
                    with open(file_path, 'r', encoding='utf-8') as f:
                        data = json.load(f)
                        if not isinstance(data, dict):
                            self.log(f"JSON file is not a dictionary: {file_path}", "ERROR")
                            all_valid = False
                        else:
                            self.log(f"Valid JSON file with {len(data)} keys", "SUCCESS")
                except Exception as e:
                    self.log(f"Error reading JSON file {file_path}: {e}", "ERROR")
                    all_valid = False
        
        return all_valid
    
    def check_workflow_schedule(self) -> bool:
        """Verify GitHub Actions workflow schedule"""
        self.log("Checking workflow schedule...")
        
        workflow_file = ".github/workflows/daily-update.yml"
        if not os.path.exists(workflow_file):
            self.log(f"Workflow file not found: {workflow_file}", "ERROR")
            return False
        
        try:
            with open(workflow_file, 'r') as f:
                content = f.read()
            
            # Check for schedule configuration
            if "schedule:" in content and "cron:" in content:
                self.log("Found schedule configuration in workflow", "SUCCESS")
                
                # Extract cron expression
                lines = content.split('\n')
                for line in lines:
                    if "cron:" in line:
                        cron_expr = line.strip().split("'")[1]
                        self.log(f"Cron schedule: {cron_expr}", "SUCCESS")
                        
                        # Validate cron expression format
                        parts = cron_expr.split()
                        if len(parts) == 5:
                            self.log("Valid cron expression format", "SUCCESS")
                        else:
                            self.log("Invalid cron expression format", "ERROR")
                            return False
                        
                        # Check if it's set for Berlin time (7 AM UTC = 8 AM Berlin)
                        if parts[1] == "7":  # Hour field
                            self.log("Correctly scheduled for 8 AM Berlin time", "SUCCESS")
                        else:
                            self.log(f"Schedule might not be for 8 AM Berlin time (hour: {parts[1]})", "WARNING")
                        
                        break
            else:
                self.log("No schedule configuration found in workflow", "ERROR")
                return False
            
            # Check for required permissions
            if "permissions:" in content:
                self.log("Found permissions configuration", "SUCCESS")
            else:
                self.log("No permissions configuration found", "WARNING")
            
            return True
            
        except Exception as e:
            self.log(f"Error reading workflow file: {e}", "ERROR")
            return False
    
    def check_dashboard_files(self) -> bool:
        """Verify dashboard files are present and valid"""
        self.log("Checking dashboard files...")
        
        dashboard_files = [
            "deployment/index.html",
            "deployment/css/style.css",
            "deployment/js/dashboard.js"
        ]
        
        all_valid = True
        
        for file_path in dashboard_files:
            if not os.path.exists(file_path):
                self.log(f"Missing dashboard file: {file_path}", "ERROR")
                all_valid = False
                continue
            
            file_size = os.path.getsize(file_path)
            if file_size == 0:
                self.log(f"Empty dashboard file: {file_path}", "ERROR")
                all_valid = False
                continue
            
            self.log(f"Valid dashboard file: {file_path} ({file_size:,} bytes)", "SUCCESS")
            
            # Basic content validation
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            if file_path.endswith('.html'):
                if "<!DOCTYPE html>" in content and "<html" in content:
                    self.log("Valid HTML structure", "SUCCESS")
                else:
                    self.log("Invalid HTML structure", "ERROR")
                    all_valid = False
            
            elif file_path.endswith('.css'):
                if len(content.strip()) > 0:
                    self.log("CSS file has content", "SUCCESS")
                else:
                    self.log("Empty CSS file", "WARNING")
            
            elif file_path.endswith('.js'):
                if "function" in content or "const" in content or "let" in content:
                    self.log("JavaScript file has content", "SUCCESS")
                else:
                    self.log("JavaScript file might be empty", "WARNING")
        
        return all_valid
    
    def test_data_fetching(self) -> bool:
        """Test data fetching functionality"""
        self.log("Testing data fetching...")
        
        # Check if we can import the fetch module
        try:
            sys.path.insert(0, 'src')
            from fetch_pr_data import GitHubPRAnalytics
            self.log("Successfully imported fetch_pr_data module", "SUCCESS")
        except ImportError as e:
            self.log(f"Failed to import fetch_pr_data: {e}", "ERROR")
            return False
        
        # Test basic functionality (without actually fetching)
        try:
            # Check if environment variables are accessible
            github_token = os.getenv('GITHUB_TOKEN')
            github_repo = os.getenv('GITHUB_REPO')
            
            if not github_token:
                self.log("GITHUB_TOKEN not found in environment", "ERROR")
                return False
            
            if not github_repo:
                self.log("GITHUB_REPO not found in environment", "ERROR")
                return False
            
            self.log("Environment variables accessible", "SUCCESS")
            
            # Test GitHub API connection (without fetching data)
            headers = {
                'Authorization': f'token {github_token}',
                'Accept': 'application/vnd.github.v3+json'
            }
            
            # Test with a simple API call
            response = requests.get(
                f'https://api.github.com/repos/{github_repo}',
                headers=headers,
                timeout=10
            )
            
            if response.status_code == 200:
                self.log("GitHub API connection successful", "SUCCESS")
                repo_data = response.json()
                self.log(f"Repository: {repo_data['full_name']}", "SUCCESS")
                return True
            else:
                self.log(f"GitHub API connection failed: {response.status_code}", "ERROR")
                return False
                
        except Exception as e:
            self.log(f"Error testing data fetching: {e}", "ERROR")
            return False
    
    def check_deployment_status(self) -> bool:
        """Check if the dashboard is properly deployed"""
        self.log("Checking deployment status...")
        
        dashboard_url = "https://aviv-fathallahelmasri.github.io/pr-analytics-dashboard/"
        
        try:
            response = requests.get(dashboard_url, timeout=10)
            if response.status_code == 200:
                self.log("Dashboard is accessible online", "SUCCESS")
                
                # Check if data files are accessible
                data_urls = [
                    f"{dashboard_url}data/pr_metrics_all_prs.csv",
                    f"{dashboard_url}data/last_update.json"
                ]
                
                for url in data_urls:
                    try:
                        data_response = requests.get(url, timeout=10)
                        if data_response.status_code == 200:
                            self.log(f"Data file accessible: {url}", "SUCCESS")
                        else:
                            self.log(f"Data file not accessible: {url} (Status: {data_response.status_code})", "ERROR")
                    except Exception as e:
                        self.log(f"Error accessing data file {url}: {e}", "ERROR")
                
                return True
            else:
                self.log(f"Dashboard not accessible: {response.status_code}", "ERROR")
                return False
                
        except Exception as e:
            self.log(f"Error checking deployment: {e}", "ERROR")
            return False
    
    def check_git_status(self) -> bool:
        """Check git repository status"""
        self.log("Checking git status...")
        
        try:
            # Check if we're in a git repository
            result = subprocess.run(['git', 'status'], 
                                  capture_output=True, text=True)
            
            if result.returncode == 0:
                self.log("Git repository is valid", "SUCCESS")
                
                # Check remote origin
                result = subprocess.run(['git', 'remote', 'get-url', 'origin'], 
                                      capture_output=True, text=True)
                
                if result.returncode == 0:
                    remote_url = result.stdout.strip()
                    self.log(f"Remote origin: {remote_url}", "SUCCESS")
                    
                    if "pr-analytics-dashboard" in remote_url:
                        self.log("Correct remote repository", "SUCCESS")
                        return True
                    else:
                        self.log("Remote repository might be incorrect", "WARNING")
                else:
                    self.log("No remote origin configured", "ERROR")
                    return False
            else:
                self.log("Not a git repository", "ERROR")
                return False
                
        except Exception as e:
            self.log(f"Error checking git status: {e}", "ERROR")
            return False
    
    def run_comprehensive_check(self) -> Dict[str, bool]:
        """Run all verification checks"""
        self.log("Starting comprehensive system verification...")
        
        results = {
            "file_structure": self.check_file_structure(),
            "environment_setup": self.check_environment_setup(),
            "data_files": self.check_data_files(),
            "workflow_schedule": self.check_workflow_schedule(),
            "dashboard_files": self.check_dashboard_files(),
            "git_status": self.check_git_status(),
            "deployment_status": self.check_deployment_status()
        }
        
        return results
    
    def run_data_fetch_test(self) -> bool:
        """Run data fetching test"""
        self.log("Running data fetching test...")
        return self.test_data_fetching()
    
    def generate_report(self, results: Dict[str, bool], data_fetch_test: bool = False) -> str:
        """Generate a comprehensive verification report"""
        
        report = []
        report.append("=" * 60)
        report.append("GitHub PR Analytics - System Verification Report")
        report.append("=" * 60)
        report.append(f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        report.append("")
        
        # Summary
        passed = sum(results.values())
        total = len(results)
        
        report.append(f"Overall Status: {passed}/{total} checks passed")
        
        if passed == total:
            report.append("🎉 All system checks PASSED! Your PR Analytics system is working correctly.")
        else:
            report.append(f"⚠️ {total - passed} issues found that need attention.")
        
        report.append("")
        
        # Detailed results
        report.append("Detailed Results:")
        report.append("-" * 20)
        
        for check, passed in results.items():
            status = "✅ PASS" if passed else "❌ FAIL"
            report.append(f"{check.replace('_', ' ').title()}: {status}")
        
        if data_fetch_test:
            status = "✅ PASS" if data_fetch_test else "❌ FAIL"
            report.append(f"Data Fetch Test: {status}")
        
        report.append("")
        
        # Issues found
        if self.issues_found:
            report.append("Issues Found:")
            report.append("-" * 15)
            for issue in self.issues_found:
                report.append(f"• {issue}")
            report.append("")
        
        # Recommendations
        report.append("Recommendations:")
        report.append("-" * 15)
        
        if not results.get("data_files", True):
            report.append("• Run data fetch to generate missing data files")
        
        if not results.get("deployment_status", True):
            report.append("• Check GitHub Pages deployment settings")
            report.append("• Verify GitHub Actions workflow is enabled")
        
        if not results.get("environment_setup", True):
            report.append("• Set up required environment variables")
            report.append("• Create .env file with GITHUB_TOKEN and GITHUB_REPO")
        
        report.append("")
        
        # System information
        report.append("System Information:")
        report.append("-" * 20)
        report.append(f"Python Version: {sys.version}")
        report.append(f"Current Directory: {os.getcwd()}")
        report.append(f"Checks Passed: {len(self.checks_passed)}")
        report.append(f"Issues Found: {len(self.issues_found)}")
        
        return "\n".join(report)

def main():
    """Main execution function"""
    parser = argparse.ArgumentParser(
        description="Comprehensive verification of GitHub PR Analytics system"
    )
    parser.add_argument('--verbose', action='store_true',
                       help='Enable verbose logging')
    parser.add_argument('--fix', action='store_true',
                       help='Attempt to fix common issues')
    parser.add_argument('--test-fetch', action='store_true',
                       help='Test data fetching from GitHub API')
    
    args = parser.parse_args()
    
    # Create verifier instance
    verifier = PRAnalyticsVerifier(verbose=args.verbose, fix_issues=args.fix)
    
    print("🔍 GitHub PR Analytics System Verification")
    print("=" * 50)
    print()
    
    # Run comprehensive checks
    results = verifier.run_comprehensive_check()
    
    # Run data fetch test if requested
    data_fetch_test = False
    if args.test_fetch:
        data_fetch_test = verifier.run_data_fetch_test()
    
    # Generate and display report
    report = verifier.generate_report(results, data_fetch_test)
    print("\n" + report)
    
    # Save report to file
    with open("verification_report.txt", "w", encoding="utf-8") as f:
        f.write(report)
    
    verifier.log("Verification report saved to verification_report.txt", "SUCCESS")
    
    # Exit with appropriate code
    if all(results.values()) and (not args.test_fetch or data_fetch_test):
        print("\n🎉 All verifications passed! Your system is ready.")
        return 0
    else:
        print("\n⚠️ Some verifications failed. Please review the report above.")
        return 1

if __name__ == "__main__":
    sys.exit(main())
