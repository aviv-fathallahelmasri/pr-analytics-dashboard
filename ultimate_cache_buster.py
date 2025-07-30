#!/usr/bin/env python3
"""
Ultimate GitHub Pages Cache Buster
==================================
Forces GitHub Pages to serve fresh content by making significant changes.
"""

import os
import subprocess
from datetime import datetime
import time

def run_cmd(cmd):
    print(f"$ {cmd}")
    result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
    if result.stdout:
        print(result.stdout.strip())
    return result.returncode == 0

print("=== Ultimate GitHub Pages Cache Buster ===\n")

# Work in deployment directory
os.chdir("deployment")

# Ensure on gh-pages
run_cmd("git checkout gh-pages")

# Method 1: Add version parameter to index.html
print("\n1. Adding cache buster to HTML...")
with open("index.html", "r", encoding="utf-8") as f:
    html = f.read()

# Add timestamp to force reload of data files
timestamp = str(int(time.time()))
old_pattern = 'fetch("data/pr_metrics_all_prs.csv")'
new_pattern = f'fetch("data/pr_metrics_all_prs.csv?v={timestamp}")'
html = html.replace(old_pattern, new_pattern)

old_pattern2 = 'fetch("data/last_update.json")'
new_pattern2 = f'fetch("data/last_update.json?v={timestamp}")'
html = html.replace(old_pattern2, new_pattern2)

with open("index.html", "w", encoding="utf-8") as f:
    f.write(html)

# Method 2: Create a .nojekyll file to bypass Jekyll processing
print("\n2. Creating .nojekyll file...")
with open(".nojekyll", "w") as f:
    f.write("")

# Method 3: Add cache control meta tag
print("\n3. Adding cache control to HTML...")
if '<meta http-equiv="cache-control"' not in html:
    cache_meta = '<meta http-equiv="cache-control" content="no-cache, no-store, must-revalidate">\n    '
    html = html.replace('<title>', cache_meta + '<title>')
    with open("index.html", "w", encoding="utf-8") as f:
        f.write(html)

# Commit all changes
print("\n4. Committing cache buster changes...")
run_cmd("git add -A")
run_cmd(f'git commit -m "Force cache refresh with timestamp {timestamp}"')
run_cmd("git push origin gh-pages --force")

print("\n✅ Cache buster applied!")
print("\n📊 Dashboard: https://aviv-fathallahelmasri.github.io/pr-analytics-dashboard/")
print(f"🔄 Direct link with cache buster: https://aviv-fathallahelmasri.github.io/pr-analytics-dashboard/?v={timestamp}")
print("\n⚡ This should force GitHub Pages to serve fresh content!")

os.chdir("..")
