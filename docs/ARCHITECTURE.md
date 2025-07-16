# 🏛️ Architecture & Technical Decisions

**Understanding the what, why, and how of every technical choice in this project.**

## 🎯 Design Philosophy

### Core Principles
1. **Complete Automation**: Zero manual intervention after initial setup
2. **Simplicity Over Complexity**: Use proven tools, avoid over-engineering
3. **Data Transparency**: All data publicly accessible, no hidden metrics
4. **Performance First**: Optimize for fast loading and responsiveness
5. **Maintainability**: Clear code, comprehensive docs, easy debugging

### Why These Choices?
- **GitHub Actions**: Free, integrated, reliable - no external CI/CD needed
- **Static Site**: No backend, no database, no hosting costs
- **CSV Storage**: Human-readable, version-controlled, simple to process
- **Chart.js**: Lightweight, responsive, beautiful visualizations

## 🔧 Technical Architecture

### System Components

```
┌─────────────────────────────────────────────────────────────────┐
│                        GitHub Repository                         │
├─────────────────┬──────────────────┬───────────────────────────┤
│   Source Code   │  GitHub Actions  │     GitHub Pages          │
│                 │                  │                           │
│  - Python ETL   │  - Cron Schedule │  - Static Hosting        │
│  - Dashboard    │  - Automated Run │  - CDN Distribution      │
│  - Configs      │  - Deployment    │  - HTTPS by Default      │
└─────────────────┴──────────────────┴───────────────────────────┘
                           │
                           ▼
                  ┌─────────────────┐
                  │   Data Flow     │
                  │                 │
                  │ API → Process → │
                  │ CSV → Deploy →  │
                  │ Live Dashboard  │
                  └─────────────────┘
```

### Data Pipeline Architecture

```python
# Simplified flow representation
def daily_analytics_pipeline():
    """
    Runs every day at 8:00 AM Berlin time
    Complete automation - no manual steps
    """
    # 1. Fetch Data
    pr_data = github_api.fetch_all_prs(
        repo=CONFIGURED_REPO,
        token=GITHUB_TOKEN
    )
    
    # 2. Process Analytics
    metrics = calculate_metrics(pr_data)
    
    # 3. Generate Files
    save_to_csv(metrics, 'data/pr_metrics_all_prs.csv')
    save_metadata(last_update_info, 'data/last_update.json')
    
    # 4. Deploy
    copy_to_deployment_directory()
    git_commit_and_push()
    
    # 5. GitHub Pages automatically serves updated content
```

## 📊 Design Decisions & Rationale

### 1. Why Python for Backend Processing?

**Decision**: Use Python with pandas for data processing

**Rationale**:
- **Rich ecosystem**: pandas, requests, built-in CSV support
- **Fast development**: Less boilerplate, more productivity
- **GitHub Actions support**: First-class Python support in Actions
- **Easy maintenance**: Readable code, great debugging tools

**Alternatives considered**:
- Node.js: Would work, but Python better for data analysis
- Go: Overkill for our needs, longer development time
- Bash: Too limited for complex data processing

### 2. Why CSV Instead of Database?

**Decision**: Store data in CSV files

**Rationale**:
- **Simplicity**: No database setup or maintenance
- **Version control**: Git tracks all changes beautifully  
- **Transparency**: Anyone can open and understand the data
- **Portability**: Works everywhere, no dependencies
- **Good enough**: 200-1000 PRs fit easily in a CSV

**Trade-offs accepted**:
- No real-time queries (don't need them)
- Limited to data that fits in memory (not an issue)
- No complex relationships (PR data is flat anyway)

### 3. Why Static Site Instead of Dynamic?

**Decision**: Pure HTML/CSS/JS with no backend

**Rationale**:
- **Free hosting**: GitHub Pages costs nothing
- **Fast loading**: No server round trips
- **High reliability**: CDN-served, always available
- **Security**: No backend = no vulnerabilities
- **Simple deployment**: Just push files

**Implementation details**:
```javascript
// Dashboard loads data client-side
fetch('data/pr_metrics_all_prs.csv')
    .then(response => response.text())
    .then(csv => {
        const data = parseCSV(csv);
        renderDashboard(data);
    });
```

### 4. Why GitHub Actions for Automation?

**Decision**: Use GitHub Actions with cron schedule

**Rationale**:
- **Free tier generous**: 2000 minutes/month more than enough
- **Integrated**: No external services needed
- **Reliable**: GitHub's infrastructure is solid
- **Easy secrets management**: Built-in secret storage
- **Great debugging**: Clear logs, easy troubleshooting

**Configuration approach**:
```yaml
# Simple, readable, maintainable
on:
  schedule:
    - cron: '0 7 * * *'  # 8 AM Berlin = 7 AM UTC
```

### 5. Why Chart.js for Visualizations?

**Decision**: Use Chart.js library for all charts

**Rationale**:
- **Lightweight**: Only 60KB minified
- **Responsive**: Works great on all devices
- **Beautiful defaults**: Looks professional out of the box
- **Easy to customize**: Simple API, good documentation
- **No dependencies**: Standalone library

**Alternative considered**:
- D3.js: Too complex for our needs
- Google Charts: Requires internet connection
- Plotly: Larger size, overkill for simple charts

## 🔐 Security Architecture

### Token Management
```
GitHub Secrets (Encrypted)
    ↓
GitHub Actions (Runtime)
    ↓
Environment Variable
    ↓
Python Script (Memory only)
    ↓
API Calls (HTTPS)
```

### Security Decisions:
1. **Read-only token**: Principle of least privilege
2. **No token in code**: Only in GitHub secrets
3. **HTTPS everywhere**: All API calls encrypted
4. **Public data only**: No sensitive info in dashboard
5. **No user input**: Static site, no attack vectors

## 📁 File Structure Decisions

### Why This Structure?
```
github-pr-analytics/
├── src/                 # Source code separation
├── deployment/          # Ready-to-deploy files
├── data/               # Generated data files
├── config/             # Configuration files
├── docs/               # Comprehensive documentation
└── tests/              # Test organization
```

**Rationale**:
- **Clear separation**: Source vs deployment vs data
- **Easy deployment**: Just copy deployment/ folder
- **Git-friendly**: Large CSVs in specific folders
- **Discoverable**: Obvious where everything lives

## 🚀 Performance Optimizations

### Data Loading Strategy
```javascript
// Load data once, process in memory
let cachedData = null;

async function loadData() {
    if (cachedData) return cachedData;
    
    const response = await fetch('data/pr_metrics_all_prs.csv');
    const csv = await response.text();
    cachedData = parseCSV(csv);
    
    return cachedData;
}
```

### Dashboard Optimizations:
1. **Lazy loading**: Charts render only when visible
2. **Debounced filters**: Prevent excessive re-renders
3. **Minimal dependencies**: Only load what we need
4. **CDN assets**: Libraries served from fast CDNs
5. **Compressed assets**: Minified CSS/JS in production

## 🔄 Scalability Considerations

### Current Limits:
- **PRs**: Tested up to 1000 PRs
- **Update frequency**: Daily is optimal
- **API rate limit**: 5000 requests/hour plenty

### Future Scaling:
```python
# Easy to add pagination for large repos
def fetch_all_prs_paginated(repo, token):
    all_prs = []
    page = 1
    
    while True:
        prs = fetch_page(repo, token, page)
        if not prs:
            break
        all_prs.extend(prs)
        page += 1
    
    return all_prs
```

### If We Need to Scale:
1. **Multiple repos**: Add repo selection dropdown
2. **Historical data**: Store yearly archives
3. **Team views**: Add author filtering
4. **Real-time**: Consider webhooks + serverless
5. **Large datasets**: Switch to Parquet files

## 🎨 Frontend Architecture

### Component Structure
```javascript
// Modular, maintainable dashboard
const Dashboard = {
    // Data management
    data: {
        prs: [],
        metrics: {}
    },
    
    // UI components
    charts: {
        timeline: null,
        distribution: null,
        authors: null,
        speed: null
    },
    
    // Core methods
    async init() {
        await this.loadData();
        this.calculateMetrics();
        this.renderDashboard();
        this.attachEventListeners();
    }
};
```

### CSS Architecture
```css
/* Utility-first approach with custom properties */
:root {
    /* Consistent design tokens */
    --primary-color: #6366f1;
    --background: #0f172a;
    --surface: #1e293b;
    
    /* Responsive spacing */
    --space-sm: 0.5rem;
    --space-md: 1rem;
    --space-lg: 2rem;
}
```

## 🧪 Testing Strategy

### Current Approach:
1. **Manual testing**: Run locally before deploying
2. **Automated checks**: GitHub Actions validates on push
3. **Visual regression**: Screenshot comparisons
4. **Data validation**: Check CSV integrity

### Future Testing:
```python
# Unit tests for metrics
def test_merge_rate_calculation():
    prs = [
        {'state': 'merged'},
        {'state': 'closed'},
        {'state': 'open'}
    ]
    assert calculate_merge_rate(prs) == 33.33

# Integration tests for pipeline
def test_full_pipeline():
    data = fetch_test_data()
    metrics = process_metrics(data)
    assert metrics['total_prs'] > 0
```

## 💭 Lessons Learned

### What Worked Well:
1. **Simplicity pays off**: Easy to understand and maintain
2. **Static sites rock**: Fast, free, reliable
3. **CSV is underrated**: Perfect for this use case
4. **GitHub Actions reliable**: Never had issues
5. **Documentation crucial**: Helps future me

### What I'd Do Differently:
1. **Add tests earlier**: Would catch edge cases
2. **Use TypeScript**: Better for larger dashboard code
3. **Consider SQLite**: If data grows beyond 10k PRs
4. **Add monitoring**: Track if automation fails
5. **Build API**: If multiple consumers needed

## 🔮 Future Architecture

### Potential Enhancements:
```
Current:  GitHub API → CSV → Static Site
Future:   GitHub API → Processing → Database → API → Multiple Frontends
                          ↓
                    Notifications
                          ↓
                  Analytics Engine
```

### But remember: **YAGNI** (You Aren't Gonna Need It)
Current architecture serves the need perfectly!

---

**Architecture documented**: July 16, 2025  
**Decisions by**: Aviv  
**Status**: Production-ready and proven