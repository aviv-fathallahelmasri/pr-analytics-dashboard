#!/usr/bin/env python3
"""
Diagnose GitHub Pages deployment issues
"""

import requests
import json

def diagnose_deployment():
    """Check various URLs to diagnose the deployment"""
    
    print("🔍 Diagnosing GitHub Pages deployment...\n")
    
    # Test different possible URLs
    urls_to_test = [
        # Root level
        "https://aviv-fathallahelmasri.github.io/pr-analytics-dashboard/",
        "https://aviv-fathallahelmasri.github.io/pr-analytics-dashboard/index.html",
        "https://aviv-fathallahelmasri.github.io/pr-analytics-dashboard/data/pr_metrics_all_prs.csv",
        "https://aviv-fathallahelmasri.github.io/pr-analytics-dashboard/data/last_update.json",
        
        # Check if it's in a subdirectory
        "https://aviv-fathallahelmasri.github.io/pr-analytics-dashboard/pr-analytics-dashboard/",
        "https://aviv-fathallahelmasri.github.io/pr-analytics-dashboard/deployment/",
    ]
    
    for url in urls_to_test:
        try:
            response = requests.head(url, allow_redirects=True, timeout=5)
            if response.status_code == 200:
                print(f"✅ {response.status_code} - {url}")
                
                # If it's the JSON file, get the content
                if url.endswith('last_update.json'):
                    response = requests.get(url)
                    data = response.json()
                    print(f"    Total PRs: {data['total_prs']}")
                    print(f"    Last Update: {data['last_update_time']}")
            else:
                print(f"❌ {response.status_code} - {url}")
        except Exception as e:
            print(f"❌ Error - {url}: {str(e)}")
    
    print("\n💡 Recommendations:")
    print("1. Go to: https://github.com/aviv-fathallahelmasri/pr-analytics-dashboard/settings/pages")
    print("2. Check the 'Source' setting - should be 'Deploy from a branch'")
    print("3. Check the 'Branch' - should be 'main' and '/ (root)'")
    print("4. Look for any error messages on that page")
    print("5. Check the Actions tab for deployment status")

if __name__ == "__main__":
    diagnose_deployment()
