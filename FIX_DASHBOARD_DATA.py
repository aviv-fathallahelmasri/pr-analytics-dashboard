#!/usr/bin/env python3
"""
Emergency Dashboard Fix - Copy fresh data to all necessary locations
"""
import shutil
from pathlib import Path
from datetime import datetime

print("=" * 60)
print("EMERGENCY DASHBOARD FIX - UPDATING DATA FILES")
print("=" * 60)

# Define paths
project_root = Path(r"C:\Users\FElmasri\Desktop\github-pr-analytics")
data_dir = project_root / "data"
deployment_dir = project_root / "deployment"
deployment_data_dir = deployment_dir / "data"

# Ensure deployment/data directory exists
deployment_data_dir.mkdir(parents=True, exist_ok=True)

# Files to copy
files_to_copy = [
    "pr_metrics_all_prs.csv",
    "metadata.json", 
    "last_update.json"
]

print("\n📋 Copying fresh data files...")
print("-" * 40)

for filename in files_to_copy:
    src = data_dir / filename
    
    # Copy to deployment root
    dst1 = deployment_dir / filename
    if src.exists():
        shutil.copy2(src, dst1)
        print(f"✅ Copied to deployment/: {filename}")
    
    # Copy to deployment/data
    dst2 = deployment_data_dir / filename
    if src.exists():
        shutil.copy2(src, dst2)
        print(f"✅ Copied to deployment/data/: {filename}")

# Also update the index.html timestamp
print("\n🔄 Updating dashboard timestamp...")
index_file = deployment_dir / "index.html"
if index_file.exists():
    with open(index_file, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Update timestamp
    current_time = datetime.now().strftime('%-m/%-d/%Y, %-I:%M:%S %p')
    import re
    
    # Multiple patterns to catch different formats
    patterns = [
        r'Last Updated: [^<]+',
        r'last updated: [^<]+',
        r'Updated: [^<]+',
    ]
    
    replacement = f'Last Updated: {current_time}'
    
    for pattern in patterns:
        if re.search(pattern, content, re.IGNORECASE):
            content = re.sub(pattern, replacement, content, flags=re.IGNORECASE)
            break
    
    with open(index_file, 'w', encoding='utf-8') as f:
        f.write(content)
    
    print(f"✅ Updated timestamp to: {current_time}")

# Verify the update
print("\n✔️ Verification...")
print("-" * 40)

csv_file = deployment_data_dir / "pr_metrics_all_prs.csv"
if csv_file.exists():
    import pandas as pd
    df = pd.read_csv(csv_file)
    print(f"📊 PR count in deployment/data/: {len(df)} PRs")
    
    # Check file sizes
    import os
    size_kb = os.path.getsize(csv_file) / 1024
    print(f"📁 File size: {size_kb:.2f} KB")
    
    if len(df) == 359:
        print("✅ SUCCESS: Dashboard data is now updated with 359 PRs!")
    else:
        print(f"⚠️  Warning: Expected 359 PRs but found {len(df)}")

print("\n" + "=" * 60)
print("✅ DATA FILES UPDATED IN ALL LOCATIONS")
print("=" * 60)
print("\n📌 Now push these changes to GitHub:")
print("   git add -A")
print('   git commit -m "Fix: Update dashboard data files with 359 PRs"')
print("   git push origin main")
print("=" * 60)
