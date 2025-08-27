# GitHub PR Analytics Dashboard

**End-to-end automated system for tracking and analyzing GitHub Pull Request metrics with zero manual intervention.**

[![Dashboard Status](https://img.shields.io/badge/Dashboard-Live-success)](https://aviv-fathallahelmasri.github.io/pr-analytics-dashboard/)
[![Automation](https://img.shields.io/badge/Updates-Daily%20@%208AM%20Berlin-blue)](https://github.com/aviv-fathallahelmasri/pr-analytics-dashboard/actions)
[![PRs Analyzed](https://img.shields.io/badge/PRs%20Analyzed-214-brightgreen)](https://aviv-fathallahelmasri.github.io/pr-analytics-dashboard/)

## What This Does

This project provides **complete automation** for PR analytics - from data collection to live dashboard updates. Once configured, it runs daily at 8:00 AM Berlin time without any manual work needed.

### Key Features:
- **Fully Automated**: Daily updates at 8:00 AM Berlin time
- **Comprehensive Analytics**: Merge rates, review coverage, author stats, and more
- **Interactive Dashboard**: Live visualizations with Chart.js
- **Zero Maintenance**: Self-updating system
- **Professional UI**: Modern, responsive design

## Live Dashboard

**Check it out**: https://aviv-fathallahelmasri.github.io/pr-analytics-dashboard/

### Current Metrics (Auto-Updated Daily):
- Total PRs Analyzed: 214
- Average Merge Rate: 82.7%
- Active Contributors: 25
- Average Merge Time: 76.1 hours

## Architecture Overview

```
┌─────────────────┐     ┌──────────────────┐     ┌─────────────────┐
│  GitHub Actions │────▶│ Python Analytics │────▶│  GitHub Pages   │
│  (Daily 8AM)    │     │    Engine        │     │   Dashboard     │
└─────────────────┘     └──────────────────┘     └─────────────────┘
        │                        │                         │
        ▼                        ▼                         ▼
   Scheduled             Fetch & Process              Live Website
   Automation            PR Data                   Updated Metrics
```

## Quick Start

### Prerequisites
- Python 3.12+
- GitHub Personal Access Token
- GitHub repository with PRs to analyze

### Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/aviv-fathallahelmasri/pr-analytics-dashboard.git
   cd pr-analytics-dashboard
   ```

2. **Set up Python environment**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   pip install -r config/requirements.txt
   ```

3. **Configure environment**
   ```bash
   cp .env.example .env
   # Edit .env with your GitHub token and target repository
   ```

4. **Run initial data fetch**
   ```bash
   python src/fetch_pr_data.py
   ```

5. **Deploy to GitHub Pages**
   ```bash
   python src/update_and_deploy.py --deploy
   ```

## Documentation

### Core Documentation
- [Complete Setup Guide](docs/SETUP_GUIDE.md) - Detailed installation and configuration
- [Troubleshooting Guide](docs/TROUBLESHOOTING.md) - Common issues and solutions
- [Architecture Details](docs/ARCHITECTURE.md) - System design and components
- [Contributing Guidelines](docs/CONTRIBUTING.md) - How to contribute

### Technical Documentation
- [Automation Workflow](docs/AUTOMATION_WORKFLOW.md) - How the daily automation works
- [Metrics Explained](docs/METRICS_GUIDE.md) - Understanding all analytics
- [Dashboard Customization](docs/DASHBOARD_CUSTOMIZATION.md) - Modifying the UI
- [Security Best Practices](docs/SECURITY.md) - Token management and security

### Development Documentation
- [Development Workflow](docs/DEVELOPMENT.md) - Local development setup
- [Testing Guide](docs/TESTING.md) - Running and writing tests
- [Code Style Guide](docs/CODE_STYLE.md) - Coding standards and conventions
- [Deployment Guide](docs/DEPLOYMENT.md) - Manual and automated deployment

## Project Structure

```
github-pr-analytics/
├── .github/
│   └── workflows/
│       └── daily-update.yml      # Automated daily workflow
├── config/
│   ├── requirements.txt          # Python dependencies
│   └── settings.py              # Configuration settings
├── src/
│   ├── fetch_pr_data.py         # Core data fetching logic
│   ├── update_and_deploy.py     # Deployment automation
│   └── utils/                   # Utility functions
├── deployment/
│   ├── index.html               # Dashboard HTML
│   ├── css/                     # Styling
│   ├── js/                      # Dashboard JavaScript
│   └── data/                    # Generated data files
├── data/
│   ├── pr_metrics_all_prs.csv  # Raw PR data
│   └── last_update.json         # Update metadata
├── docs/                        # All documentation
├── tests/                       # Test suite
└── README.md                    # This file
```

## How It Works

### Daily Automation Flow (8:00 AM Berlin Time)
1. **GitHub Actions triggers** the workflow
2. **Fetches PR data** from configured repository
3. **Processes metrics** (merge rate, review coverage, etc.)
4. **Generates files** (CSV data, JSON metadata)
5. **Deploys to GitHub Pages** automatically
6. **Dashboard updates** with fresh data

### Manual Update (When Needed)
```bash
# Fetch latest data and deploy
python src/update_and_deploy.py --deploy

# Force update even if recent
python src/update_and_deploy.py --force --deploy
```

## Metrics Tracked

- **Total PRs**: All pull requests analyzed
- **Merge Rate**: Percentage of PRs merged
- **Average Merge Time**: Hours from creation to merge
- **Active Authors**: Unique contributors
- **Review Coverage**: PRs with at least one review
- **Fast Merges**: PRs merged within 24 hours
- **PR Status Distribution**: Open, Merged, Closed
- **Activity Timeline**: PR creation trends
- **Top Authors**: Most active contributors
- **Merge Speed Distribution**: Time to merge analysis

## Security & Best Practices

- **Token Security**: GitHub token stored as repository secret
- **Minimal Permissions**: Read-only access to PR data
- **Automated Updates**: No manual token handling
- **Public Dashboard**: No sensitive data exposed
- **Git Best Practices**: Conventional commits, clear history

## Contributing

I welcome contributions! Please see our [Contributing Guidelines](docs/CONTRIBUTING.md) for details.

### Areas for Contribution:
- New metrics and visualizations
- Performance optimizations
- Documentation improvements
- Bug fixes and enhancements
- UI/UX improvements

## Future Enhancements

- [ ] Historical trend analysis
- [ ] Team performance metrics
- [ ] Custom date range selection
- [ ] Export functionality
- [ ] Email notifications
- [ ] Slack integration
- [ ] Multiple repository support
- [ ] Advanced filtering options

## Troubleshooting

Common issues and solutions are documented in our [Troubleshooting Guide](docs/TROUBLESHOOTING.md).

Quick fixes:
- **Dashboard not updating?** Check GitHub Actions logs
- **Wrong PR count?** Verify repository access and token permissions
- **Deployment failed?** Ensure GitHub Pages is enabled

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Acknowledgments

- Built with Python, GitHub Actions, and Chart.js
- Deployed on GitHub Pages
- Inspired by the need for better PR insights

---

*Last README Update: July 16, 2025*
