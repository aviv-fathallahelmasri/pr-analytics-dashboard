"""
Simple Health Check for PR Analytics Dashboard
Save this as workflow_health_check.py in your project directory
"""
import os
import json
import requests
from datetime import datetime
from pathlib import Path

def check_data_freshness():
    """Check if data files are recent"""
    print("\n🔍 Checking data freshness...")
    
    # Check for metadata.json
    if os.path.exists("data/metadata.json"):
        try:
            with open("data/metadata.json", encoding='utf-8') as f:
                metadata = json.load(f)
            
            last_updated = metadata.get('last_updated', 'Unknown')
            print(f"✓ Last update recorded: {last_updated}")
            
            # Check CSV files
            csv_count = len(list(Path("data").glob("*.csv")))
            print(f"✓ Found {csv_count} CSV files in data directory")
            
            return True
        except Exception as e:
            print(f"✗ Error reading metadata: {e}")
            return False
    else:
        print("✗ metadata.json not found - creating it...")
        
        # Create metadata file
        os.makedirs("data", exist_ok=True)
        metadata = {
            'last_updated': datetime.now().isoformat(),
            'created_by': 'health_check'
        }
        
        with open("data/metadata.json", 'w', encoding='utf-8') as f:
            json.dump(metadata, f, indent=2)
        
        print("✓ Created metadata.json")
        return False

def check_github_pages():
    """Check if GitHub Pages is accessible"""
    print("\n🔍 Checking GitHub Pages...")
    
    url = "https://aviv-fathallahelmasri.github.io/pr-analytics-dashboard/"
    
    try:
        response = requests.get(url, timeout=10)
        if response.status_code == 200:
            print(f"✓ GitHub Pages is live (status: {response.status_code})")
            return True
        else:
            print(f"✗ GitHub Pages returned status: {response.status_code}")
            return False
    except Exception as e:
        print(f"✗ Error accessing GitHub Pages: {e}")
        return False

def check_workflow_file():
    """Check if workflow file exists"""
    print("\n🔍 Checking workflow configuration...")
    
    workflow_path = ".github/workflows/daily-update.yml"
    
    if os.path.exists(workflow_path):
        print(f"✓ Workflow file exists: {workflow_path}")
        
        try:
            # Check workflow content with proper encoding
            with open(workflow_path, 'r', encoding='utf-8') as f:
                content = f.read()
        except UnicodeDecodeError:
            # Try with different encoding if UTF-8 fails
            try:
                with open(workflow_path, 'r', encoding='latin-1') as f:
                    content = f.read()
            except Exception as e:
                print(f"  ✗ Error reading workflow file: {e}")
                return False
        
        # Check for key elements
        checks = {
            "Cron schedule": "cron:" in content,
            "Manual trigger": "workflow_dispatch:" in content,
            "Fetch script": "fetch_pr_data.py" in content,
            "Permissions": "permissions:" in content
        }
        
        for check, result in checks.items():
            if result:
                print(f"  ✓ {check}: Found")
            else:
                print(f"  ✗ {check}: Missing")
        
        return True
    else:
        print(f"✗ Workflow file not found: {workflow_path}")
        return False

def check_environment():
    """Check environment setup"""
    print("\n🔍 Checking environment...")
    
    # Check Python version
    import sys
    print(f"✓ Python version: {sys.version.split()[0]}")
    
    # Check for GitHub token
    if os.environ.get('GITHUB_TOKEN'):
        print("✓ GITHUB_TOKEN is set in environment")
    else:
        print("⚠️  GITHUB_TOKEN not set (needed for local testing)")
        print("   Set with: set GITHUB_TOKEN=your_token_here")
    
    # Check required directories
    dirs = ['data', 'deployment', 'src', '.github/workflows']
    for dir_name in dirs:
        if os.path.exists(dir_name):
            print(f"✓ Directory exists: {dir_name}/")
        else:
            print(f"✗ Directory missing: {dir_name}/")
    
    return True

def check_recent_actions():
    """Provide link to check recent GitHub Actions"""
    print("\n📋 GitHub Actions Status:")
    print("Check your recent workflow runs at:")
    print("https://github.com/aviv-fathallahelmasri/pr-analytics-dashboard/actions")
    print("\nLook for:")
    print("- ✓ Green checkmarks = successful runs")
    print("- ✗ Red X marks = failed runs")
    print("- Click on any run to see detailed logs")

def main():
    print("=" * 60)
    print("PR Analytics Dashboard - Health Check")
    print("=" * 60)
    print(f"Current time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"Working directory: {os.getcwd()}")
    
    # Run all checks
    results = []
    results.append(("Environment", check_environment()))
    results.append(("Data Freshness", check_data_freshness()))
    results.append(("Workflow Config", check_workflow_file()))
    results.append(("GitHub Pages", check_github_pages()))
    
    # Summary
    print("\n" + "=" * 60)
    print("SUMMARY")
    print("=" * 60)
    
    all_good = True
    for name, result in results:
        status = "✓ PASS" if result else "✗ FAIL"
        print(f"{name}: {status}")
        if not result:
            all_good = False
    
    print("\n" + "=" * 60)
    
    if all_good:
        print("✅ Basic checks passed!")
    else:
        print("❌ Some checks failed - see details above")
    
    # Always show GitHub Actions link
    check_recent_actions()
    
    print("\n💡 Next steps:")
    print("1. Check GitHub Actions for any failed runs")
    print("2. Ensure PERSONAL_ACCESS_TOKEN secret is set in repository")
    print("3. Manually trigger the workflow to test")
    print("4. Check the deployment folder has correct file paths")

if __name__ == "__main__":
    main()
