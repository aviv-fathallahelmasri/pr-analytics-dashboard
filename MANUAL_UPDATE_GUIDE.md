# Manual Dashboard Update Guide

## 🚀 Quick Start

To manually update your GitHub PR Analytics Dashboard with the latest data:

### Option 1: Double-Click (Easiest)
1. Navigate to your project folder: `C:\Users\FElmasri\Desktop\github-pr-analytics`
2. Double-click `run_manual_update.bat`
3. Wait for the process to complete
4. Check your dashboard at: https://aviv-fathallahelmasri.github.io/pr-analytics-dashboard/

### Option 2: PowerShell
1. Right-click `run_manual_update.ps1`
2. Select "Run with PowerShell"
3. Follow the on-screen progress

### Option 3: PyCharm Terminal
1. Open PyCharm
2. Open the integrated terminal
3. Run: `python manual_dashboard_update.py`

---

## 📋 What the Manual Update Does

The manual update process performs these steps automatically:

1. **Fetches Latest PR Data** 📊
   - Connects to GitHub API
   - Downloads all PR information from `axel-springer-kugawana/aviv_data_collection_contracts`
   - Processes and analyzes the data
   - Saves updated metrics to CSV files

2. **Prepares Deployment Files** 📁
   - Copies updated data files to deployment directory
   - Ensures all dashboard files are in sync
   - Validates file integrity

3. **Commits Data Updates** 💾
   - Commits new data to the main branch
   - Pushes changes to GitHub repository
   - Maintains version history

4. **Deploys to GitHub Pages** 🌐
   - Updates the gh-pages branch
   - Deploys new dashboard version
   - Makes it live at your GitHub Pages URL

---

## 🔍 Monitoring the Update

### During Update
The script provides real-time feedback:
- ✅ Green checkmarks for successful steps
- ❌ Red X marks for failures
- 📊 Current statistics (total PRs, update time)
- ⏰ Progress indicators

### After Update
- **Log File**: Check `manual_update.log` for detailed information
- **GitHub Actions**: View deployment status at https://github.com/aviv-fathallahelmasri/pr-analytics-dashboard/actions
- **Live Dashboard**: Visit https://aviv-fathallahelmasri.github.io/pr-analytics-dashboard/

---

## 🛠️ Troubleshooting

### Common Issues and Solutions

#### 1. Virtual Environment Not Found
**Error**: "Failed to activate virtual environment"
**Solution**: 
```bash
# In PyCharm terminal:
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
```

#### 2. GitHub Token Issues
**Error**: "401 Unauthorized" or "403 Forbidden"
**Solution**: 
- Check your `.env` file in the `config` directory
- Ensure `GITHUB_TOKEN` is set correctly
- Verify token has necessary permissions

#### 3. Push Failed
**Error**: "Failed to push to main branch"
**Solution**:
```bash
# Check git status
git status
# Pull latest changes
git pull origin main
# Retry the update
python manual_dashboard_update.py
```

#### 4. Deployment Not Updating
**Issue**: Dashboard shows old data after update
**Solutions**:
- Wait 2-5 minutes (GitHub Pages cache)
- Hard refresh browser (Ctrl+F5)
- Check GitHub Pages settings in repository

---

## 📊 Verifying Success

### Check These Indicators:

1. **Update Log Shows Success**
   ```
   ✅ Manual update completed successfully!
   ```

2. **Last Update Time is Current**
   - Open `data/last_update.json`
   - Verify timestamp matches current time

3. **Dashboard Shows New Data**
   - Visit dashboard URL
   - Check "Last Updated" timestamp
   - Verify PR count increased (if new PRs exist)

---

## 🔧 Advanced Options

### Custom Update with Specific Parameters

If you need more control, use the Python script directly:

```python
# In PyCharm terminal:
from manual_dashboard_update import DashboardUpdater

updater = DashboardUpdater()

# Run individual steps:
updater.fetch_latest_data()      # Only fetch data
updater.prepare_deployment_files() # Only prepare files
updater.commit_data_updates()     # Only commit
updater.deploy_to_github_pages()  # Only deploy
```

### Scheduling Manual Updates

To schedule regular manual updates (Windows Task Scheduler):
1. Open Task Scheduler
2. Create Basic Task
3. Set trigger (daily, weekly, etc.)
4. Action: Start `run_manual_update.bat`
5. Set path to project directory

---

## 📈 Best Practices

1. **Regular Updates**: Run manual updates when:
   - You need immediate data refresh
   - Automated updates seem delayed
   - Testing new features

2. **Monitor Logs**: Always check `manual_update.log` for:
   - Performance metrics
   - Error patterns
   - Update history

3. **Backup Before Major Changes**: 
   ```bash
   # Create backup
   git checkout -b backup-branch
   git push origin backup-branch
   ```

4. **Verify Token Permissions**: Ensure your GitHub token has:
   - `repo` scope (full repository access)
   - `workflow` scope (if updating workflows)

---

## 🆘 Getting Help

If you encounter issues:

1. **Check Logs First**: `manual_update.log` contains detailed error information
2. **Verify Environment**: Ensure all dependencies are installed
3. **Test Components**: Run individual scripts to isolate issues
4. **GitHub Status**: Check https://www.githubstatus.com/ for API issues

---

## 🎯 Quick Commands Reference

```bash
# Full manual update
python manual_dashboard_update.py

# Only fetch new data
python src/fetch_pr_data.py

# Check current data status
python check_status.py

# Verify deployment
python check_deployment.py

# View update history
git log --oneline -n 10 data/
```

---

**Last Updated**: January 24, 2025
**Dashboard URL**: https://aviv-fathallahelmasri.github.io/pr-analytics-dashboard/
