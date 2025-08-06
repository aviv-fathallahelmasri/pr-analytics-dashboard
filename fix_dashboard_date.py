#!/usr/bin/env python3
"""
Fix the hardcoded date in the dashboard HTML
"""

import os
import json
import re
from pathlib import Path
from datetime import datetime

def fix_dashboard_date():
    """Update the hardcoded date in the HTML to reflect latest data."""
    root = Path(__file__).parent
    
    # Read latest update info
    with open(root / "data" / "last_update.json", 'r') as f:
        data = json.load(f)
    
    # Parse the update time
    update_time = datetime.fromisoformat(data['last_update_time'].replace('+00:00', ''))
    formatted_date = update_time.strftime("%m/%d/%Y, %I:%M:%S %p")
    
    print(f"Latest update time: {formatted_date}")
    print(f"Total PRs: {data['total_prs']}")
    
    # Update the main deployment HTML
    html_path = root / "deployment" / "index.html"
    with open(html_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Find and replace the date - it's in the format "Last Updated: 7/24/2025, 12:36:34 PM"
    old_pattern = r'Last Updated: \d+/\d+/\d+, \d+:\d+:\d+ [AP]M'
    new_text = f'Last Updated: {formatted_date}'
    
    content = re.sub(old_pattern, new_text, content)
    
    # Also update the total PRs if it's showing 236
    content = re.sub(r'<span class="kpi-value" id="totalPRs">236</span>', 
                     f'<span class="kpi-value" id="totalPRs">{data["total_prs"]}</span>', 
                     content)
    
    # Write back
    with open(html_path, 'w', encoding='utf-8') as f:
        f.write(content)
    
    print(f"✓ Updated HTML with new date: {formatted_date}")
    
    # Now commit and push
    os.chdir(root / "deployment")
    
    os.system('git add index.html')
    os.system(f'git commit -m "Update dashboard date to {formatted_date} with {data["total_prs"]} PRs"')
    os.system('git push origin main:gh-pages --force')
    
    print("\n✅ Dashboard HTML updated and pushed!")
    print("🌐 Check: https://aviv-fathallahelmasri.github.io/pr-analytics-dashboard/")

if __name__ == "__main__":
    fix_dashboard_date()
