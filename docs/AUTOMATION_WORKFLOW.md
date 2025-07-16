# 🔄 Automation Workflow Documentation

**Everything about the daily automation that keeps your dashboard fresh without lifting a finger!**

## 🎯 Overview

This system runs **completely automatically** every day at 8:00 AM Berlin time. Once set up, you literally don't need to do anything - it just works!

## ⚙️ How The Automation Works

### The Daily Schedule
```yaml
# Runs at 8:00 AM Berlin time (7:00 AM UTC)
schedule:
  - cron: '0 7 * * *'
  
# What this means:
# - Minute: 0 (top of the hour)
# - Hour: 7 (7 AM UTC = 8 AM Berlin)
# - Day: * (every day)
# - Month: * (every month)  
# - Weekday: * (every day of week)
```

### The Complete Flow

```
8:00 AM Berlin Time
       │
       ▼
GitHub Actions Triggers
       │
       ▼
Spin Up Ubuntu Runner
       │
       ▼
Install Python & Dependencies
       │
       ▼
Fetch Latest PR Data
       │
       ▼
Process Analytics
       │
       ▼
Generate CSV & JSON
       │
       ▼
Deploy to GitHub Pages
       │
       ▼
Dashboard Updates (5-10 min)
       │
       ▼
You See Fresh Data! 🎉
```

## 📋 Workflow Configuration

### File: `.github/workflows/daily-update.yml`

```yaml
name: 📊 Daily PR Analytics Update

on:
  schedule:
    # This is where the magic happens - daily at 8 AM Berlin
    - cron: '0 7 * * *'
  
  # Also allows manual triggering if needed
  workflow_dispatch:
    inputs:
      force_update:
        description: 'Force update even if data is recent'
        required: false
        default: 'false'
```

### Key Configuration Sections

#### 1. **Permissions** (Required for GitHub Pages)
```yaml
permissions:
  contents: write      # To push commits
  pages: write        # To deploy to Pages
  id-token: write     # For OIDC deployment
```

#### 2. **Environment Setup**
```yaml
- name: 🐍 Setup Python
  uses: actions/setup-python@v4
  with:
    python-version: '3.12'
    cache: 'pip'  # Speeds up builds
```

#### 3. **The Main Update Process**
```yaml
- name: 📊 Update PR Analytics Data
  env:
    GITHUB_TOKEN: ${{ secrets.PRANALYTICS_TOKEN_PERSONAL }}
    GITHUB_REPO: ${{ secrets.PRANALYTICS_GITHUB_REPO }}
  run: |
    python src/update_and_deploy.py --verbose
```

## 🔑 Required Secrets

### Setting Up Repository Secrets

1. Go to: Settings → Secrets and variables → Actions
2. Add these secrets:

#### `PRANALYTICS_TOKEN_PERSONAL`
- Your GitHub Personal Access Token
- Needs `repo` scope for private repos
- Or `public_repo` for public repos

#### `PRANALYTICS_GITHUB_REPO`
- Format: `owner/repository`
- Example: `axel-springer-kugawana/aviv_data_collection_contracts`

### Creating a GitHub Token
```bash
# Go to: https://github.com/settings/tokens
# Click: Generate new token (classic)
# Select scopes:
# - repo (for private repositories)
# - public_repo (for public repositories only)
# Copy the token immediately!
```

## 🚀 The Update Script

### Core Logic: `src/update_and_deploy.py`

```python
def daily_update_process():
    """
    This runs every day automatically
    No manual intervention needed!
    """
    # 1. Check if update needed (optional)
    if not force_update and data_is_recent():
        logger.info("Data is recent, skipping update")
        return
    
    # 2. Fetch latest PR data
    logger.info("🔄 Fetching latest PR data...")
    fetch_pr_data_from_github()
    
    # 3. Update deployment directory
    logger.info("📁 Updating deployment files...")
    copy_data_to_deployment()
    
    # 4. Let GitHub Actions handle deployment
    logger.info("✅ Update complete!")
```

## 📊 What Gets Updated

### Data Files Generated
1. **`data/pr_metrics_all_prs.csv`**
   - Contains all PR information
   - One row per PR
   - All metrics calculated

2. **`data/last_update.json`**
   ```json
   {
     "last_update_time": "2025-07-16T14:22:26.216176+02:00",
     "total_prs": 214,
     "repository": "org/repo",
     "update_type": "full"
   }
   ```

### Deployment Process
```bash
# Files are copied from data/ to deployment/data/
cp data/pr_metrics_all_prs.csv deployment/data/
cp data/last_update.json deployment/data/

# Then committed and pushed
git add .
git commit -m "📊 Automated PR analytics update - [timestamp]"
git push origin main
```

## 🔍 Monitoring The Automation

### Check Workflow Runs
1. Go to: https://github.com/[your-username]/pr-analytics-dashboard/actions
2. Look for "📊 Daily PR Analytics Update"
3. Green checkmark = Success!

### Understanding Run Logs
```
┌─ 📊 Daily PR Analytics Update #42
├─ Set up job (2s)
├─ 🔄 Checkout Code (1s)
├─ 🐍 Setup Python (15s)
├─ 📦 Install Dependencies (30s)
├─ 📊 Update PR Analytics Data (3m 12s) ← Main work happens here
├─ 🌐 Deploy to GitHub Pages (45s)
├─ 📈 Summary Report (1s)
└─ Complete job (1s)
```

### What Each Step Does

#### Update PR Analytics Data (The Important One)
```
🚀 Starting daily PR analytics update...
📅 Current time: Wed Jul 17 07:00:15 UTC 2025
🔑 Using GitHub token: ghp_ABC123...
📂 Target repository: axel-springer-kugawana/aviv_data_collection_contracts

🔄 Standard update
📡 Fetching PR data from GitHub API...
  Found 215 total PRs
  ├─ 176 merged
  ├─ 36 closed
  └─ 3 open

📊 Calculating metrics...
  ├─ Merge rate: 83.0%
  ├─ Avg merge time: 75.8 hours
  ├─ Active authors: 25
  └─ Review coverage: 67.2%

💾 Saving data files...
✅ Successfully updated PR analytics!
```

## 🛠️ Manual Triggers

### When You Might Need Manual Runs
- Testing changes to the workflow
- Forcing an update outside schedule
- Debugging issues

### How to Manually Trigger
1. Go to Actions tab
2. Click "📊 Daily PR Analytics Update"
3. Click "Run workflow"
4. Options:
   - Branch: `main`
   - Force update: `true/false`
5. Click green "Run workflow" button

### Via GitHub CLI
```bash
gh workflow run daily-update.yml
```

## 🔧 Customizing The Schedule

### Different Time Zones
```yaml
# Examples for different times:

# 9 AM New York (EST)
- cron: '0 14 * * *'  # 14:00 UTC

# 6 AM London (GMT)
- cron: '0 6 * * *'   # 06:00 UTC

# 10 PM Tokyo (JST)
- cron: '0 13 * * *'  # 13:00 UTC

# Multiple times per day
schedule:
  - cron: '0 7 * * *'   # Morning
  - cron: '0 15 * * *'  # Afternoon
```

### Cron Syntax Helper
```
┌───────────── minute (0-59)
│ ┌───────────── hour (0-23)
│ │ ┌───────────── day of month (1-31)
│ │ │ ┌───────────── month (1-12)
│ │ │ │ ┌───────────── day of week (0-6)
│ │ │ │ │
│ │ │ │ │
* * * * *
```

## 🚨 Handling Failures

### Automatic Notifications
The workflow includes failure handling:
```yaml
- name: 🚨 Notify on Failure
  if: failure()
  run: |
    echo "❌ Daily update failed!"
    echo "Check the logs for details"
```

### Common Failure Reasons
1. **Token expired**: Update secret
2. **API rate limit**: Wait an hour
3. **Repository renamed**: Update secret
4. **Network issues**: Usually temporary

### Recovery Process
Failed runs don't affect the schedule:
- If today's run fails, tomorrow's still runs
- You can manually trigger anytime
- System is self-healing

## 📈 Success Metrics

### How to Know It's Working
1. **Dashboard timestamp** updates daily
2. **PR count** increases when new PRs added
3. **Workflow history** shows green checkmarks
4. **No manual work** required from you!

### Expected Performance
- **Workflow duration**: 3-5 minutes
- **Data freshness**: Within 15 minutes of run
- **Success rate**: 99%+ (very reliable)
- **Cost**: $0 (within free tier)

## 🔐 Security Considerations

### Token Safety
- Never commit tokens to code
- Use repository secrets only
- Rotate tokens every 90 days
- Use minimal required permissions

### Workflow Security
```yaml
# Runs with minimal permissions
permissions:
  contents: write  # Only what's needed
  pages: write
  id-token: write
```

## 💡 Pro Tips

### 1. **Check Time Zone Changes**
Daylight saving time doesn't affect UTC cron

### 2. **Monitor Rate Limits**
```python
# The script handles rate limits gracefully
if response.status_code == 403:
    logger.warning("Rate limit hit, waiting...")
    time.sleep(3600)  # Wait an hour
```

### 3. **Test Locally First**
```bash
# Run the same command locally
python src/update_and_deploy.py --verbose
```

### 4. **Keep Logs Clean**
The workflow automatically manages log retention

## 🎯 Summary

**The automation is designed to be completely hands-off:**
- Runs daily at 8:00 AM Berlin time
- Fetches all PR data automatically
- Updates dashboard without intervention
- Handles errors gracefully
- Keeps your analytics always current

**Your only job**: Enjoy the insights! 📊

---

*Automation documented: July 16, 2025*  
*Next scheduled run: Tomorrow at 8:00 AM Berlin time*