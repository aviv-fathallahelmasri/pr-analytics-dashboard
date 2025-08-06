#!/usr/bin/env python3
"""
Comprehensive PR Analytics Dashboard System Review
==================================================
This script performs a complete end-to-end review of your GitHub PR Analytics system
to ensure everything is working correctly and can catch the latest changes.

Author: Assistant for Aviv
Date: 2025-08-06
Purpose: Complete system validation and health check
"""

import os
import sys
import json
import subprocess
from datetime import datetime, timedelta
from pathlib import Path
import requests
import pandas as pd
from typing import Dict, List, Tuple, Optional

# Add colors for terminal output
class Colors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

def print_section(title: str, color=Colors.HEADER):
    """Print a formatted section header"""
    print(f"\n{color}{Colors.BOLD}{'='*70}{Colors.ENDC}")
    print(f"{color}{Colors.BOLD}{title.center(70)}{Colors.ENDC}")
    print(f"{color}{Colors.BOLD}{'='*70}{Colors.ENDC}\n")

def print_status(message: str, status: str = "info"):
    """Print a formatted status message"""
    icons = {
        "success": f"{Colors.OKGREEN}✓{Colors.ENDC}",
        "error": f"{Colors.FAIL}✗{Colors.ENDC}",
        "warning": f"{Colors.WARNING}⚠{Colors.ENDC}",
        "info": f"{Colors.OKCYAN}ℹ{Colors.ENDC}",
        "check": f"{Colors.OKBLUE}🔍{Colors.ENDC}"
    }
    print(f"{icons.get(status, icons['info'])} {message}")

class PRAnalyticsReview:
    """Main class for reviewing the PR Analytics system"""
    
    def __init__(self):
        self.project_root = Path("C:/Users/FElmasri/Desktop/github-pr-analytics")
        self.github_repo = "aviv-fathallahelmasri/pr-analytics-dashboard"
        self.target_repo = "axel-springer-kugawana/aviv_data_collection_contracts"
        self.dashboard_url = "https://aviv-fathallahelmasri.github.io/pr-analytics-dashboard/"
        self.issues_found = []
        self.recommendations = []
        
    def run_complete_review(self) -> Dict:
        """Run a complete system review"""
        print_section("PR ANALYTICS DASHBOARD - COMPLETE SYSTEM REVIEW")
        print(f"Review Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print(f"Project Root: {self.project_root}")
        
        review_results = {
            "timestamp": datetime.now().isoformat(),
            "checks": {},
            "issues": [],
            "recommendations": []
        }
        
        # 1. Check project structure
        print_section("1. PROJECT STRUCTURE CHECK", Colors.OKCYAN)
        review_results["checks"]["structure"] = self.check_project_structure()
        
        # 2. Check data freshness
        print_section("2. DATA FRESHNESS CHECK", Colors.OKCYAN)
        review_results["checks"]["data"] = self.check_data_freshness()
        
        # 3. Check GitHub Actions
        print_section("3. GITHUB ACTIONS CHECK", Colors.OKCYAN)
        review_results["checks"]["actions"] = self.check_github_actions()
        
        # 4. Check dashboard deployment
        print_section("4. DASHBOARD DEPLOYMENT CHECK", Colors.OKCYAN)
        review_results["checks"]["deployment"] = self.check_dashboard_deployment()
        
        # 5. Check environment configuration
        print_section("5. ENVIRONMENT CONFIGURATION CHECK", Colors.OKCYAN)
        review_results["checks"]["environment"] = self.check_environment()
        
        # 6. Check data pipeline
        print_section("6. DATA PIPELINE CHECK", Colors.OKCYAN)
        review_results["checks"]["pipeline"] = self.check_data_pipeline()
        
        # 7. Generate report and recommendations
        print_section("REVIEW SUMMARY", Colors.HEADER)
        self.generate_summary(review_results)
        
        review_results["issues"] = self.issues_found
        review_results["recommendations"] = self.recommendations
        
        # Save review results
        self.save_review_results(review_results)
        
        return review_results
    
    def check_project_structure(self) -> Dict:
        """Check if all required files and directories exist"""
        result = {"status": "pass", "details": {}}
        
        required_items = {
            "directories": [
                "src",
                "data", 
                "deployment",
                ".github/workflows",
                "docs",
                "config"
            ],
            "files": [
                "src/fetch_pr_data.py",
                "deployment/index.html",
                ".github/workflows/daily-update.yml",
                "requirements.txt",
                "README.md"
            ]
        }
        
        for item_type, items in required_items.items():
            print(f"\nChecking {item_type}:")
            for item in items:
                path = self.project_root / item
                exists = path.exists()
                
                if exists:
                    print_status(f"{item}", "success")
                    result["details"][item] = "exists"
                else:
                    print_status(f"{item} - MISSING", "error")
                    result["details"][item] = "missing"
                    result["status"] = "fail"
                    self.issues_found.append(f"Missing {item_type[:-1]}: {item}")
        
        return result
    
    def check_data_freshness(self) -> Dict:
        """Check how fresh the data is"""
        result = {"status": "pass", "details": {}}
        
        data_dir = self.project_root / "data"
        
        # Check CSV file
        csv_file = data_dir / "pr_metrics_all_prs.csv"
        if csv_file.exists():
            mod_time = datetime.fromtimestamp(csv_file.stat().st_mtime)
            age = datetime.now() - mod_time
            
            print_status(f"CSV last modified: {mod_time.strftime('%Y-%m-%d %H:%M:%S')}", "info")
            print_status(f"Data age: {age.days} days, {age.seconds//3600} hours", "info")
            
            result["details"]["csv_age_hours"] = age.total_seconds() / 3600
            
            if age.days > 1:
                print_status("Data is older than 24 hours", "warning")
                result["status"] = "warning"
                self.issues_found.append(f"Data is {age.days} days old")
                self.recommendations.append("Run manual update or wait for next scheduled run")
            else:
                print_status("Data is fresh (< 24 hours old)", "success")
        else:
            print_status("CSV file not found!", "error")
            result["status"] = "fail"
            self.issues_found.append("Missing CSV data file")
        
        # Check metadata
        metadata_file = data_dir / "metadata.json"
        if metadata_file.exists():
            with open(metadata_file) as f:
                metadata = json.load(f)
            print_status(f"Metadata last updated: {metadata.get('last_updated', 'Unknown')}", "info")
            result["details"]["metadata"] = metadata
        
        return result
    
    def check_github_actions(self) -> Dict:
        """Check GitHub Actions workflow configuration"""
        result = {"status": "pass", "details": {}}
        
        workflow_file = self.project_root / ".github/workflows/daily-update.yml"
        
        if workflow_file.exists():
            with open(workflow_file, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # Check for essential components
            checks = {
                "Schedule (cron)": "cron: '0 7 * * *'" in content,
                "Manual trigger": "workflow_dispatch:" in content,
                "Python setup": "uses: actions/setup-python" in content,
                "Data fetch": "python src/fetch_pr_data.py" in content,
                "GitHub Pages deploy": "actions/deploy-pages" in content,
                "Permissions": "contents: write" in content
            }
            
            for check_name, passed in checks.items():
                if passed:
                    print_status(f"{check_name}", "success")
                else:
                    print_status(f"{check_name} - NOT FOUND", "error")
                    result["status"] = "fail"
                    self.issues_found.append(f"Workflow missing: {check_name}")
                
                result["details"][check_name] = passed
        else:
            print_status("Workflow file not found!", "error")
            result["status"] = "fail"
            self.issues_found.append("Missing workflow file")
        
        # Provide GitHub Actions URL
        actions_url = f"https://github.com/{self.github_repo}/actions"
        print_status(f"Check recent runs at: {actions_url}", "info")
        
        return result
    
    def check_dashboard_deployment(self) -> Dict:
        """Check if the dashboard is accessible and working"""
        result = {"status": "pass", "details": {}}
        
        try:
            response = requests.get(self.dashboard_url, timeout=10)
            
            if response.status_code == 200:
                print_status(f"Dashboard is LIVE (status: {response.status_code})", "success")
                result["details"]["accessible"] = True
                
                # Check if it contains expected elements
                content = response.text
                checks = {
                    "Has Chart.js": "chart.js" in content.lower(),
                    "Has title": "GitHub PR Analytics Dashboard" in content,
                    "Has data loading": "loadData" in content or "fetchData" in content
                }
                
                for check_name, passed in checks.items():
                    if passed:
                        print_status(f"{check_name}", "success")
                    else:
                        print_status(f"{check_name} - NOT FOUND", "warning")
                    result["details"][check_name] = passed
            else:
                print_status(f"Dashboard returned status: {response.status_code}", "error")
                result["status"] = "fail"
                self.issues_found.append(f"Dashboard HTTP status: {response.status_code}")
        
        except Exception as e:
            print_status(f"Error accessing dashboard: {e}", "error")
            result["status"] = "fail"
            self.issues_found.append(f"Dashboard not accessible: {str(e)}")
        
        return result
    
    def check_environment(self) -> Dict:
        """Check environment configuration"""
        result = {"status": "pass", "details": {}}
        
        # Check Python version
        print_status(f"Python version: {sys.version.split()[0]}", "info")
        result["details"]["python_version"] = sys.version.split()[0]
        
        # Check for GitHub token in environment
        has_token = bool(os.environ.get('GITHUB_TOKEN'))
        if has_token:
            print_status("GITHUB_TOKEN is set", "success")
        else:
            print_status("GITHUB_TOKEN not set (needed for local testing)", "warning")
            self.recommendations.append("Set GITHUB_TOKEN environment variable for local testing")
        result["details"]["has_github_token"] = has_token
        
        # Check if requirements are installed
        try:
            import github
            import pandas
            import requests
            print_status("Required packages installed", "success")
            result["details"]["packages_installed"] = True
        except ImportError as e:
            print_status(f"Missing package: {e}", "error")
            result["status"] = "fail"
            result["details"]["packages_installed"] = False
            self.recommendations.append("Run: pip install -r requirements.txt")
        
        return result
    
    def check_data_pipeline(self) -> Dict:
        """Check the data pipeline components"""
        result = {"status": "pass", "details": {}}
        
        # Check if fetch script exists and is valid
        fetch_script = self.project_root / "src/fetch_pr_data.py"
        if fetch_script.exists():
            print_status("Fetch script exists", "success")
            
            # Check script imports
            with open(fetch_script, 'r') as f:
                content = f.read()
            
            required_imports = ["github", "pandas", "json", "datetime"]
            for imp in required_imports:
                if f"import {imp}" in content or f"from {imp}" in content:
                    print_status(f"Has {imp} import", "success")
                else:
                    print_status(f"Missing {imp} import", "warning")
        else:
            print_status("Fetch script not found", "error")
            result["status"] = "fail"
        
        # Check deployment data sync
        deployment_data = self.project_root / "deployment/data"
        if deployment_data.exists():
            print_status("Deployment data directory exists", "success")
            
            # Check if data is synced
            csv_files = list(deployment_data.glob("*.csv"))
            json_files = list(deployment_data.glob("*.json"))
            
            print_status(f"Found {len(csv_files)} CSV files in deployment", "info")
            print_status(f"Found {len(json_files)} JSON files in deployment", "info")
            
            result["details"]["deployment_csv_count"] = len(csv_files)
            result["details"]["deployment_json_count"] = len(json_files)
        else:
            print_status("Deployment data directory missing", "warning")
            self.recommendations.append("Create deployment/data directory and sync data files")
        
        return result
    
    def generate_summary(self, results: Dict):
        """Generate and display summary of the review"""
        all_passed = True
        
        print("\n" + "="*70)
        print("CHECK RESULTS:")
        print("="*70)
        
        for check_name, check_result in results["checks"].items():
            status = check_result.get("status", "unknown")
            icon = {
                "pass": f"{Colors.OKGREEN}✓ PASS{Colors.ENDC}",
                "fail": f"{Colors.FAIL}✗ FAIL{Colors.ENDC}",
                "warning": f"{Colors.WARNING}⚠ WARNING{Colors.ENDC}"
            }.get(status, "? UNKNOWN")
            
            print(f"{check_name.upper():30} {icon}")
            
            if status != "pass":
                all_passed = False
        
        print("\n" + "="*70)
        
        if self.issues_found:
            print(f"\n{Colors.FAIL}ISSUES FOUND ({len(self.issues_found)}):{Colors.ENDC}")
            for i, issue in enumerate(self.issues_found, 1):
                print(f"  {i}. {issue}")
        
        if self.recommendations:
            print(f"\n{Colors.WARNING}RECOMMENDATIONS ({len(self.recommendations)}):{Colors.ENDC}")
            for i, rec in enumerate(self.recommendations, 1):
                print(f"  {i}. {rec}")
        
        print("\n" + "="*70)
        
        if all_passed and not self.issues_found:
            print(f"{Colors.OKGREEN}{Colors.BOLD}✅ SYSTEM IS HEALTHY!{Colors.ENDC}")
            print("Your PR Analytics Dashboard is working correctly.")
        else:
            print(f"{Colors.WARNING}{Colors.BOLD}⚠️  ATTENTION NEEDED{Colors.ENDC}")
            print("Some issues need to be addressed for optimal performance.")
        
        print("\n" + "="*70)
    
    def save_review_results(self, results: Dict):
        """Save review results to a file"""
        output_file = self.project_root / "system_review_results.json"
        
        with open(output_file, 'w') as f:
            json.dump(results, f, indent=2, default=str)
        
        print(f"\n{Colors.OKCYAN}Review results saved to: {output_file}{Colors.ENDC}")

def main():
    """Main execution function"""
    try:
        # Change to project directory
        os.chdir("C:/Users/FElmasri/Desktop/github-pr-analytics")
        
        # Run the review
        reviewer = PRAnalyticsReview()
        results = reviewer.run_complete_review()
        
        # Provide next steps
        print_section("NEXT STEPS", Colors.OKCYAN)
        print("1. Review the GitHub Actions page for recent runs:")
        print("   https://github.com/aviv-fathallahelmasri/pr-analytics-dashboard/actions")
        print("\n2. If data is stale, trigger a manual update:")
        print("   - Go to Actions tab → 'PR Analytics Auto-Update Production'")
        print("   - Click 'Run workflow' → Select 'main' branch → Run")
        print("\n3. Check the live dashboard after update completes:")
        print("   https://aviv-fathallahelmasri.github.io/pr-analytics-dashboard/")
        print("\n4. For local testing, run:")
        print("   python src/fetch_pr_data.py")
        print("\n5. To force immediate dashboard update:")
        print("   python force_update_dashboard.py")
        
        return 0
        
    except Exception as e:
        print(f"\n{Colors.FAIL}Error during review: {e}{Colors.ENDC}")
        return 1

if __name__ == "__main__":
    sys.exit(main())
