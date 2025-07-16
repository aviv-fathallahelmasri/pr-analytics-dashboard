# 📊 Metrics Guide

**Understanding every metric in your PR Analytics Dashboard - what they mean and why they matter!**

## 🎯 Overview

Every metric in this dashboard was chosen to give you actionable insights into your team's PR workflow. No vanity metrics - just stuff that actually helps you improve!

## 📈 Key Performance Indicators (KPIs)

### 1. **Total PRs** 
```
Current: 214
What it is: Total number of PRs analyzed from your repository
Why it matters: Shows project activity and growth over time
```

**What to look for:**
- Steady growth = healthy project
- Sudden spikes = major features or refactoring
- Declining numbers = might need attention

### 2. **Merge Rate** 
```
Current: 82.7%
Formula: (Merged PRs / Total PRs) × 100
What it is: Percentage of PRs that get merged vs closed/abandoned
Why it matters: Indicates code quality and review effectiveness
```

**Benchmarks:**
- 80%+ = Excellent (most work gets shipped)
- 60-80% = Good (healthy review process)
- Below 60% = Investigate (why are PRs being abandoned?)

### 3. **Average Merge Time**
```
Current: 76.1 hours (~3 days)
Formula: Average(merge_time - creation_time) for all merged PRs
What it is: How long PRs stay open before merging
Why it matters: Indicates review efficiency and deployment velocity
```

**Benchmarks:**
- < 24 hours = Excellent (fast iteration)
- 24-72 hours = Good (reasonable review time)
- > 72 hours = Could improve (bottlenecks?)

### 4. **Active Authors**
```
Current: 25
What it is: Unique contributors who have created PRs
Why it matters: Shows team size and contribution distribution
```

**Insights:**
- Growing number = expanding team or community
- Compare with total PRs for contribution density
- Look for bus factor risks (too few contributors)

### 5. **Review Coverage**
```
Current: 66.8%
Formula: (PRs with reviews / Total PRs) × 100
What it is: Percentage of PRs that received at least one review
Why it matters: Code quality and knowledge sharing indicator
```

**Targets:**
- 100% = Ideal (every PR reviewed)
- 80%+ = Good practice
- Below 50% = Risk (unreviewed code)

### 6. **Fast Merges (<24H)**
```
Current: 69.5%
Formula: (PRs merged within 24h / Total merged PRs) × 100
What it is: PRs that go from creation to merge in under a day
Why it matters: Indicates team agility and CI/CD effectiveness
```

**What it means:**
- High percentage = Efficient workflow
- Low percentage = Review bottlenecks
- Consider PR size correlation

## 📊 Visualizations Explained

### PR Activity Timeline
```javascript
// What it shows
{
  x: 'Time (months)',
  y: 'Number of PRs created',
  data: 'PRs grouped by creation month'
}
```

**How to read it:**
- Upward trend = Growing activity
- Seasonal patterns = Sprint cycles
- Sudden drops = Holidays or team changes

**Use it to:**
- Plan capacity
- Identify busy periods
- Track growth trends

### PR Status Distribution
```javascript
// Breakdown
{
  Merged: 'Successfully integrated PRs',
  Open: 'Currently active PRs',
  Closed: 'Abandoned or superseded PRs'
}
```

**Healthy distribution:**
- Merged: 70-85%
- Open: 5-15%
- Closed: 10-20%

**Red flags:**
- Too many open (>30%) = Review bottleneck
- Too many closed (>30%) = Quality issues

### Top Authors
```javascript
// What it tracks
{
  author: 'GitHub username',
  pr_count: 'Total PRs created',
  percentage: 'Share of total PRs'
}
```

**Insights to gain:**
- Contribution balance
- Key contributors
- Bus factor risks
- Onboarding success

### Merge Speed Distribution
```javascript
// Categories
{
  '<1 hour': 'Hot fixes or tiny changes',
  '1-6 hours': 'Small, quick reviews',
  '6-24 hours': 'Standard PRs',
  '1-3 days': 'Complex changes',
  '3-7 days': 'Major features',
  '>7 days': 'Needs investigation'
}
```

**What to optimize:**
- Reduce '>7 days' category
- Increase '<24 hours' for small PRs
- Balance speed with quality

## 🔍 Advanced Metrics (In the Data)

### Hidden Gems in the CSV

The raw data contains more metrics you can analyze:

#### 1. **Changed Files per PR**
```python
# Why it matters
Small PRs (1-5 files) = Easier reviews = Faster merges
Large PRs (20+ files) = Harder reviews = Slower merges
```

#### 2. **Additions vs Deletions**
```python
# Code health indicator
More deletions than additions = Good (removing debt)
Only additions = Watch out (growing complexity)
```

#### 3. **Review Comments**
```python
# Collaboration quality
0 comments = Rubber stamp?
1-5 comments = Healthy discussion
20+ comments = Might be too complex
```

#### 4. **Label Usage**
```python
# Process maturity
Labels used = Organized workflow
No labels = Opportunity to improve
```

## 📏 Custom Metrics You Can Add

### 1. **Velocity Trends**
```python
def calculate_velocity(prs_by_week):
    """PRs merged per week - shows team productivity"""
    return {
        week: len([pr for pr in prs if pr['merged']])
        for week, prs in prs_by_week.items()
    }
```

### 2. **Review Depth**
```python
def review_depth_score(pr):
    """Quality of review based on multiple factors"""
    score = 0
    score += min(pr['review_comments'] * 2, 10)
    score += min(pr['approvals'] * 5, 10)
    score += 5 if pr['changes_requested'] > 0 else 0
    return score / 25  # Normalize to 0-1
```

### 3. **Contributor Growth**
```python
def new_contributors_per_month(prs):
    """Track onboarding success"""
    seen_authors = set()
    new_by_month = defaultdict(int)
    
    for pr in sorted(prs, key=lambda x: x['created_at']):
        if pr['author'] not in seen_authors:
            month = pr['created_at'].strftime('%Y-%m')
            new_by_month[month] += 1
            seen_authors.add(pr['author'])
    
    return new_by_month
```

## 🎯 Using Metrics for Improvement

### Weekly Team Review Questions

1. **Merge Rate Check**
   - Why did PRs get closed instead of merged?
   - Can we salvage abandoned work?

2. **Speed Analysis**
   - Which PRs took longest? Why?
   - Can we break down large PRs?

3. **Review Coverage**
   - Who's not getting reviews?
   - Do we need more reviewers?

4. **Author Balance**
   - Is work distributed fairly?
   - Who needs support?

### Monthly Strategic Questions

1. **Trend Analysis**
   - Is velocity increasing?
   - Are we getting faster at reviews?

2. **Quality Indicators**
   - Is review coverage improving?
   - Are PR sizes getting smaller?

3. **Team Health**
   - Are new contributors sticking?
   - Is knowledge spreading?

## 📈 Metric Targets by Team Maturity

### Startup/Early Stage
- Focus on: Velocity (ship fast)
- Merge Rate: 70%+ 
- Merge Time: <48 hours
- Review Coverage: 50%+

### Growth Stage
- Focus on: Quality + Speed
- Merge Rate: 80%+
- Merge Time: <36 hours
- Review Coverage: 80%+

### Mature/Enterprise
- Focus on: Consistency
- Merge Rate: 85%+
- Merge Time: <24 hours
- Review Coverage: 95%+

## 🔮 Future Metrics Ideas

### Coming Soon™
1. **MTTR** (Mean Time To Review)
2. **Cycle Time** (Commit to Deploy)
3. **Review Rounds** (Back-and-forth count)
4. **PR Size Trends** (Getting smaller?)
5. **Weekend Warriors** (Work-life balance)

### Community Requested
1. **Language Breakdown** (What code changes most?)
2. **File Hotspots** (Which files change together?)
3. **Review Buddies** (Who reviews whom?)
4. **Deploy Correlation** (PRs vs incidents)

## 💡 Pro Tips

### 1. **Context Matters**
Don't optimize metrics in isolation. Fast isn't always better if quality suffers.

### 2. **Team Discussions**
Use metrics to start conversations, not blame games.

### 3. **Set Realistic Goals**
Improve gradually. 10% better each month compounds quickly.

### 4. **Automate Tracking**
This dashboard updates daily - check it weekly for trends.

### 5. **Share Success**
Celebrate when metrics improve. Recognition drives behavior.

---

**Remember**: Metrics are meant to help, not hurt. Use them to understand your workflow and make it better for everyone!

*Metrics guide last updated: July 16, 2025*