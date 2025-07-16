# 🔧 Troubleshooting Guide

**When things don't work as expected, this guide has got you covered!**

## 🚨 Common Issues & Solutions

### 1. Dashboard Not Updating

**Symptoms:**
- Dashboard shows old data after 8:00 AM
- "Last Updated" timestamp is from previous day

**Solutions:**

#### Check GitHub Actions
1. Go to: https://github.com/aviv-fathallahelmasri/pr-analytics-dashboard/actions
2. Look for "Daily PR Analytics Update"
3. Check if it ran today around 8:00 AM

**If workflow didn't run:**
```bash
# Manually trigger the workflow
# Go to Actions tab → Daily PR Analytics Update → Run workflow
```

**If workflow failed:**
- Click on the failed run
- Check error logs
- Common issues:
  - Token expired → Update `PRANALYTICS_TOKEN_PERSONAL` secret
  - API rate limit → Wait an hour or use different token

#### GitHub Pages Delay
GitHub Pages can take 5-15 minutes to update after deployment.

**Quick fix:**
1. Hard refresh browser: `Ctrl+F5` (Windows) or `Cmd+Shift+R` (Mac)
2. Open in incognito mode
3. Add cache buster: `?v=timestamp` to URL

### 2. Wrong PR Count

**Symptoms:**
- PR count doesn't match repository
- Missing recent PRs

**Solutions:**

#### Verify Token Permissions
```bash
# Test token access
curl -H "Authorization: token YOUR_TOKEN" \
     https://api.github.com/repos/YOUR_ORG/YOUR_REPO/pulls?state=all&per_page=1
```

#### Check Repository Access
Your token needs:
- `repo` scope for private repositories  
- `public_repo` scope for public repositories

#### Force Full Update
```bash
cd github-pr-analytics
python src/update_and_deploy.py --force --deploy
```

### 3. Deployment Failures

**Symptoms:**
- Git push errors
- "Failed to push some refs"
- Merge conflicts

**Solutions:**

#### Sync with Remote
```bash
# Reset to match remote
git fetch origin
git reset --hard origin/main
```

#### Clean Deployment Directory
```bash
# Remove problematic directories
rm -rf deployment/pr-analytics-dashboard
rm -rf temp-deploy

# Windows PowerShell
Remove-Item -Recurse -Force deployment/pr-analytics-dashboard
Remove-Item -Recurse -Force temp-deploy
```

#### Fix Diverged Branches
```bash
# If branches diverged
git pull origin main --rebase

# If conflicts occur
git rebase --abort
git reset --hard origin/main
```

### 4. Local Development Issues

**Symptoms:**
- Scripts won't run
- Import errors
- Missing dependencies

**Solutions:**

#### Reinstall Dependencies
```bash
# Clean install
rm -rf venv
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r config/requirements.txt
```

#### Python Version Issues
Ensure Python 3.12+:
```bash
python --version
# Should show Python 3.12.x or higher
```

#### Environment Variables
```bash
# Check .env file exists
cat .env

# Should contain:
# GITHUB_TOKEN=your_token_here
# GITHUB_REPO=org/repo
```

### 5. Data Quality Issues

**Symptoms:**
- Metrics seem incorrect
- Charts showing wrong data
- CSV file corrupted

**Solutions:**

#### Validate Data Files
```python
# Check CSV integrity
import pandas as pd
df = pd.read_csv('data/pr_metrics_all_prs.csv')
print(f"Total PRs: {len(df)}")
print(f"Columns: {df.columns.tolist()}")
print(f"Any nulls: {df.isnull().sum().sum()}")
```

#### Regenerate Data
```bash
# Delete existing data
rm data/pr_metrics_all_prs.csv
rm data/last_update.json

# Fetch fresh data
python src/fetch_pr_data.py
```

### 6. GitHub API Rate Limits

**Symptoms:**
- 403 errors in logs
- "API rate limit exceeded"

**Solutions:**

#### Check Rate Limit Status
```bash
curl -H "Authorization: token YOUR_TOKEN" \
     https://api.github.com/rate_limit
```

#### Wait It Out
- Rate limit resets every hour
- Authenticated requests: 5,000/hour
- Unauthenticated: 60/hour

#### Use Different Token
Create a new token or use one from different account

### 7. Dashboard Display Issues

**Symptoms:**
- Charts not rendering
- JavaScript errors
- Broken layout

**Solutions:**

#### Browser Console Check
1. Open Developer Tools (F12)
2. Check Console tab for errors
3. Common issues:
   - CORS errors → Check file paths
   - 404 errors → Files not deployed
   - JS errors → Check data format

#### Clear Browser Cache
```
Chrome: Ctrl+Shift+Del → Cached images and files
Firefox: Ctrl+Shift+Del → Cache
Safari: Cmd+Shift+Del → Empty Caches
```

#### Verify File Structure
```bash
# Check deployment directory
ls -la deployment/
# Should show: index.html, css/, js/, data/

ls -la deployment/data/
# Should show: pr_metrics_all_prs.csv, last_update.json
```

## 🔍 Debugging Commands

### Check System Status
```bash
# See what's in data directory
ls -la data/

# Check last update time
cat data/last_update.json

# Count PRs in CSV
wc -l data/pr_metrics_all_prs.csv

# Check git status
git status

# View recent commits
git log --oneline -10
```

### Test Components Individually
```bash
# Test data fetching only
python src/fetch_pr_data.py

# Test deployment without fetching
python src/update_and_deploy.py --deploy

# Run with verbose output
python src/update_and_deploy.py --verbose
```

### Manual GitHub Actions Trigger
1. Go to: Actions tab in your repository
2. Click "Daily PR Analytics Update"
3. Click "Run workflow"
4. Select branch: main
5. Click "Run workflow" button

## 🚑 Emergency Fixes

### Complete Reset
```bash
# Nuclear option - start fresh
git fetch origin
git reset --hard origin/main
rm -rf venv deployment/pr-analytics-dashboard temp-deploy
python -m venv venv
source venv/bin/activate
pip install -r config/requirements.txt
python src/update_and_deploy.py --force --deploy
```

### Manual Dashboard Update
If automation completely fails:
```bash
# 1. Fetch data
python src/fetch_pr_data.py

# 2. Copy to deployment
cp data/pr_metrics_all_prs.csv deployment/data/
cp data/last_update.json deployment/data/

# 3. Commit and push
cd deployment
git add .
git commit -m "Manual dashboard update"
git push origin main
```

## 📞 Still Stuck?

### Check These Resources:
1. **GitHub Actions Logs**: Detailed error messages
2. **Browser Console**: JavaScript errors
3. **Git History**: Recent changes that might have broken things
4. **GitHub Status**: https://githubstatus.com

### Debug Mode Script
```python
# Save as debug_analytics.py
import os
import json
import requests
from datetime import datetime

print("🔍 PR Analytics Debug Report")
print("=" * 50)

# Check environment
print("\n📋 Environment Check:")
print(f"Python: {sys.version}")
print(f"Current Dir: {os.getcwd()}")
print(f"Env File Exists: {os.path.exists('.env')}")

# Check data files
print("\n📊 Data Files:")
for file in ['data/pr_metrics_all_prs.csv', 'data/last_update.json']:
    if os.path.exists(file):
        stat = os.stat(file)
        print(f"✅ {file}: {stat.st_size} bytes, modified {datetime.fromtimestamp(stat.st_mtime)}")
    else:
        print(f"❌ {file}: NOT FOUND")

# Check GitHub token
if os.getenv('GITHUB_TOKEN'):
    print("\n🔑 GitHub Token: Set (first 10 chars: {})".format(os.getenv('GITHUB_TOKEN')[:10]))
else:
    print("\n❌ GitHub Token: NOT SET")

print("\n" + "=" * 50)
```

## 🎯 Prevention Tips

1. **Monitor Actions**: Check workflow runs weekly
2. **Update Token**: Rotate token every 90 days
3. **Check Logs**: Review automation logs for warnings
4. **Test Locally**: Run manual update monthly
5. **Backup Data**: Keep CSV backups if needed

---

**Remember**: Most issues are temporary and resolve themselves. The automation is robust and self-healing in most cases!

*Last updated: July 16, 2025*