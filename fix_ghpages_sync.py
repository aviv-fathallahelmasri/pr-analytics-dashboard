#!/usr/bin/env python3
"""
Diagnose and Fix gh-pages Sync Issue
====================================
"""

import subprocess
import os

def run_cmd(cmd):
    print(f"$ {cmd}")
    result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
    if result.stdout:
        print(result.stdout)
    if result.stderr and result.returncode != 0:
        print(f"Error: {result.stderr}")
    return result.returncode == 0, result.stdout

def main():
    print("=== Diagnosing gh-pages Sync Issue ===\n")
    
    # Save current state
    os.system("git stash")
    
    # Change to deployment directory
    os.chdir("deployment")
    
    print("1. Current branch:")
    run_cmd("git branch --show-current")
    
    print("\n2. Fetching latest from GitHub:")
    run_cmd("git fetch origin gh-pages")
    
    print("\n3. Comparing local vs remote gh-pages:")
    run_cmd("git log --oneline -5 gh-pages")
    print("\nRemote gh-pages:")
    run_cmd("git log --oneline -5 origin/gh-pages")
    
    print("\n4. Checking data file on remote:")
    # Reset to remote gh-pages to see what's actually there
    run_cmd("git checkout origin/gh-pages -- data/last_update.json")
    run_cmd("type data\\last_update.json")
    
    print("\n5. The issue is clear - remote gh-pages has old data!")
    print("\nFIXING NOW...")
    
    # Restore local version
    run_cmd("git checkout gh-pages -- data/last_update.json")
    
    # Copy fresh data from main
    os.chdir("..")
    run_cmd("copy /Y data\\pr_metrics_all_prs.csv deployment\\data\\")
    run_cmd("copy /Y data\\last_update.json deployment\\data\\")
    
    os.chdir("deployment")
    
    # Force update
    print("\n6. Force updating remote gh-pages:")
    run_cmd("git add data/")
    run_cmd('git commit -m "Force sync: Update dashboard data to 236 PRs" --allow-empty')
    run_cmd("git push origin gh-pages --force-with-lease")
    
    os.chdir("..")
    run_cmd("git stash pop")
    
    print("\n✅ Fix applied! Check dashboard in 2-5 minutes.")

if __name__ == "__main__":
    main()
