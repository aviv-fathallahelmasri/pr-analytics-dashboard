# 📖 Complete Setup Guide

**Getting your PR Analytics Dashboard up and running from scratch - the right way!**

## 📋 Prerequisites

Before we start, make sure you have:

- **Python 3.12+** installed (check with `python --version`)
- **Git** installed and configured
- **GitHub account** with access to the repository you want to analyze
- **GitHub Personal Access Token** (I'll show you how to create one)
- **Basic terminal knowledge** (but I'll guide you through everything)

## 🚀 Step-by-Step Setup

### Step 1: Clone the Repository

```bash
# Clone the repository
git clone https://github.com/aviv-fathallahelmasri/pr-analytics-dashboard.git

# Navigate into the directory
cd pr-analytics-dashboard

# Check you're in the right place
ls
# Should see: README.md, src/, deployment/, etc.
```

### Step 2: Set Up Python Environment

```bash
# Create a virtual environment (keeps things clean)
python -m venv venv

# Activate it
# On Windows:
venv\Scripts\activate
# On Mac/Linux:
source venv/bin/activate

# You should see (venv) in your terminal now

# Install all dependencies
pip install -r config/requirements.txt
```

**Why virtual environment?**  
Keeps your project dependencies isolated. No conflicts with other Python projects!

### Step 3: Create Your GitHub Token

1. Go to: https://github.com/settings/tokens
2. Click "Generate new token" → "Generate new token (classic)"
3. Give it a name: "PR Analytics Dashboard"
4. Select expiration: 90 days (or longer)
5. Select scopes:
   - `repo` (if analyzing private repositories)
   - `public_repo` (if only public repositories)
6. Click "Generate token"
7. **COPY IT NOW!** You won't see it again!

### Step 4: Configure Environment

```bash
# Create your environment file
cp .env.example .env

# Edit the file (use any text editor)
# Windows:
notepad .env
# Mac/Linux:
nano .env
```

Add your configuration:
```env
# Your GitHub token from Step 3
GITHUB_TOKEN=ghp_YourTokenHereFromStep3

# Repository to analyze (format: owner/repo)
GITHUB_REPO=axel-springer-kugawana/aviv_data_collection_contracts

# Optional: Custom update interval (minutes)
UPDATE_INTERVAL=1440  # 24 hours
```

### Step 5: Test Data Fetching

Let's make sure everything works:

```bash
# Run the fetch script
python src/fetch_pr_data.py

# You should see output like:
# 🚀 Starting PR data fetch...
# 🔑 Using GitHub token: ghp_ABC...
# 📂 Fetching from: axel-springer-kugawana/aviv_data_collection_contracts
# 📊 Found 214 PRs
# ✅ Data saved to data/pr_metrics_all_prs.csv
```

If this works, you're golden! 🎉

### Step 6: Set Up GitHub Repository

#### If Using Existing Repository:
```bash
# Add remote if not already added
git remote add origin https://github.com/YOUR_USERNAME/pr-analytics-dashboard.git

# Push your code
git push -u origin main
```

#### If Creating New Repository:
1. Go to: https://github.com/new
2. Name: `pr-analytics-dashboard`
3. Public repository (for free GitHub Pages)
4. Don't initialize with README
5. Create repository
6. Follow the instructions shown

### Step 7: Configure Repository Secrets

1. Go to your repository on GitHub
2. Click: Settings → Secrets and variables → Actions
3. Click: "New repository secret"

Add these secrets:

**Secret 1: `PRANALYTICS_TOKEN_PERSONAL`**
- Value: Your GitHub token from Step 3

**Secret 2: `PRANALYTICS_GITHUB_REPO`**
- Value: The repository you're analyzing (e.g., `owner/repo`)

### Step 8: Enable GitHub Pages

1. In your repository, go to: Settings → Pages
2. Source: Deploy from a branch
3. Branch: `main`
4. Folder: `/ (root)`
5. Click Save

**Note**: Your site will be available at:  
`https://YOUR_USERNAME.github.io/pr-analytics-dashboard/`

### Step 9: Initial Deployment

```bash
# Make sure you're in the project directory
cd pr-analytics-dashboard

# Deploy for the first time
python src/update_and_deploy.py --deploy

# This will:
# 1. Copy data files to deployment directory
# 2. Commit changes
# 3. Push to GitHub
# 4. Trigger GitHub Pages build
```

### Step 10: Verify Everything Works

1. **Check GitHub Actions**:
   - Go to: Actions tab in your repository
   - You should see workflows listed

2. **Check your dashboard**:
   - Wait 5-10 minutes for GitHub Pages
   - Visit: `https://YOUR_USERNAME.github.io/pr-analytics-dashboard/`
   - You should see your PR analytics!

3. **Check automation**:
   - The workflow will run tomorrow at 8:00 AM Berlin time
   - Or trigger manually: Actions → Daily PR Analytics Update → Run workflow

## 🔧 Configuration Options

### Customize Update Schedule

Edit `.github/workflows/daily-update.yml`:
```yaml
schedule:
  # Default: 8 AM Berlin (7 UTC)
  - cron: '0 7 * * *'
  
  # Examples:
  # 6 AM Eastern: '0 11 * * *'
  # 9 AM Pacific: '0 17 * * *'
  # Twice daily: Add another cron line
```

### Customize Dashboard

Edit `deployment/index.html`:
- Change title, colors, layout
- Add your logo
- Modify chart types
- Add new metrics

### Add Multiple Repositories

Edit `src/fetch_pr_data.py`:
```python
REPOSITORIES = [
    "org/repo1",
    "org/repo2",
    "org/repo3"
]
```

## 🐛 Common Setup Issues

### "Permission denied" on Git push
```bash
# Make sure you're authenticated
git config --global user.name "Your Name"
git config --global user.email "your.email@example.com"
```

### "Module not found" errors
```bash
# Make sure virtual environment is activated
# Should see (venv) in terminal

# Reinstall dependencies
pip install -r config/requirements.txt
```

### GitHub Pages not showing
- Wait 10 minutes (initial deployment takes time)
- Check repository is public
- Check GitHub Pages is enabled
- Try hard refresh: Ctrl+F5

### API rate limit errors
- Make sure token has correct permissions
- Wait an hour if limit exceeded
- Use different token if needed

## ✅ Setup Checklist

Make sure you've completed everything:

- [ ] Python 3.12+ installed
- [ ] Repository cloned
- [ ] Virtual environment created
- [ ] Dependencies installed
- [ ] GitHub token created
- [ ] `.env` file configured
- [ ] Test fetch successful
- [ ] Repository pushed to GitHub
- [ ] Secrets configured
- [ ] GitHub Pages enabled
- [ ] Initial deployment done
- [ ] Dashboard accessible
- [ ] Automation scheduled

## 🎉 Success!

If you've completed all steps, your PR Analytics Dashboard is now:
- ✅ Live on GitHub Pages
- ✅ Showing current PR data
- ✅ Set to update automatically daily
- ✅ Completely hands-off from now on!

## 📚 Next Steps

1. **Customize your dashboard**: See [Dashboard Customization Guide](DASHBOARD_CUSTOMIZATION.md)
2. **Add more metrics**: See [Metrics Guide](METRICS_GUIDE.md)
3. **Set up monitoring**: See [Monitoring Guide](MONITORING.md)
4. **Contribute back**: See [Contributing Guidelines](CONTRIBUTING.md)

## 💡 Pro Tips

1. **Bookmark your dashboard** for easy access
2. **Star the repository** to track updates
3. **Watch the repository** for new features
4. **Share with your team** - knowledge is power!

---

**Need help?** Check the [Troubleshooting Guide](TROUBLESHOOTING.md) or open an issue!

*Setup guide last updated: July 16, 2025*