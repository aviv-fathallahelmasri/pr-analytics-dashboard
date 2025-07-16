# 🤝 Contributing Guidelines

**Want to make this project even better? You're in the right place!**

## 🎯 Welcome Contributors!

First off, thanks for considering contributing to this project! Whether you're fixing a typo, adding a feature, or suggesting improvements - every contribution matters!

## 🚀 Quick Start

1. **Fork** the repository
2. **Clone** your fork
3. **Create** a feature branch
4. **Make** your changes
5. **Test** everything
6. **Document** what you did
7. **Submit** a pull request

## 📋 What We're Looking For

### High Priority Contributions
- 🐛 **Bug fixes** - Found something broken? Fix it!
- 📊 **New metrics** - Have ideas for useful analytics?
- 🎨 **UI improvements** - Make the dashboard prettier
- 📚 **Documentation** - Help others understand better
- 🧪 **Tests** - We need more test coverage

### Ideas We Love
- Performance optimizations
- New visualization types
- Export capabilities
- Integration with other tools
- Accessibility improvements

## 🛠️ Development Setup

### Prerequisites
```bash
# You'll need
- Python 3.12+
- Git
- GitHub account
- Basic JavaScript knowledge (for dashboard)
- Enthusiasm!
```

### Local Development
```bash
# 1. Fork and clone
git clone https://github.com/YOUR_USERNAME/pr-analytics-dashboard.git
cd pr-analytics-dashboard

# 2. Create virtual environment
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# 3. Install dependencies
pip install -r config/requirements.txt
pip install -r config/requirements-dev.txt  # Dev tools

# 4. Set up pre-commit hooks
pre-commit install

# 5. Create feature branch
git checkout -b feature/amazing-new-feature
```

## 💻 Code Style

### Python Code
```python
# We follow PEP 8 with some preferences:

# Good function - descriptive, documented, typed
def calculate_merge_rate(prs: List[Dict[str, Any]]) -> float:
    """
    Calculate the percentage of PRs that were merged.
    
    Args:
        prs: List of PR dictionaries
        
    Returns:
        Merge rate as percentage (0-100)
        
    Why this matters:
    Merge rate indicates how much work actually ships vs gets abandoned
    """
    if not prs:
        return 0.0
    
    merged_count = sum(1 for pr in prs if pr.get('Is_Merged'))
    return (merged_count / len(prs)) * 100

# We love:
# - Descriptive names (no single letters except loops)
# - Type hints everywhere
# - Docstrings that explain the "why"
# - Early returns for clarity
# - Comments that add value
```

### JavaScript Code
```javascript
// Modern, clean, readable JavaScript

// Good example - clear, documented, purposeful
async function updateDashboard() {
    // Show loading state - users need feedback
    showLoadingIndicator();
    
    try {
        // Fetch data with proper error handling
        const data = await fetchPRData();
        
        // Process and validate
        const metrics = calculateMetrics(data);
        
        // Update UI components
        updateMetricCards(metrics);
        updateCharts(data);
        
        // Success! Let the user know
        showSuccessMessage('Dashboard updated!');
        
    } catch (error) {
        // Always handle errors gracefully
        console.error('Dashboard update failed:', error);
        showErrorMessage('Failed to update dashboard. Retrying...');
        
        // Retry logic or fallback
        setTimeout(updateDashboard, 5000);
    } finally {
        hideLoadingIndicator();
    }
}

// We prefer:
// - Async/await over callbacks
// - Descriptive function names
// - Proper error handling
// - User feedback for all actions
// - Modern ES6+ features
```

### Commit Messages
```bash
# Format: <type>: <description>

# Good examples:
feat: Add export to PDF functionality
fix: Correct merge time calculation for same-day PRs
docs: Update troubleshooting guide with new solutions
style: Improve dashboard color scheme for accessibility
refactor: Simplify PR data fetching logic
test: Add unit tests for metric calculations
chore: Update dependencies to latest versions

# Include "why" in commit body when needed:
fix: Handle Unicode in PR descriptions

Previously, PRs with emoji or special characters would cause
the fetch to fail. Now we properly encode/decode all text.

Fixes #42
```

## 🧪 Testing

### Running Tests
```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=src --cov-report=html

# Run specific test file
pytest tests/test_fetch_pr_data.py

# Run in watch mode
pytest-watch
```

### Writing Tests
```python
# Good test example - clear, isolated, meaningful
def test_calculate_merge_rate_with_mixed_prs():
    """Test merge rate calculation with realistic data."""
    # Arrange - set up test data
    prs = [
        {'Is_Merged': True},
        {'Is_Merged': True},
        {'Is_Merged': False},
        {'Is_Merged': True},
    ]
    
    # Act - run the function
    result = calculate_merge_rate(prs)
    
    # Assert - check the result
    assert result == 75.0  # 3 out of 4 merged = 75%
    
    # Why this test matters:
    # Ensures our core metric calculation is accurate

# Test edge cases
def test_calculate_merge_rate_with_empty_list():
    """Ensure we handle empty data gracefully."""
    assert calculate_merge_rate([]) == 0.0

# Test error conditions
def test_fetch_with_invalid_token():
    """Verify proper error handling for auth failures."""
    with pytest.raises(GithubException):
        fetcher = PRAnalyticsFetcher('invalid_token', 'org/repo')
```

## 📝 Documentation

### When to Add Documentation
- New features need explanation
- Complex logic needs clarification  
- Setup steps change
- Common questions arise
- You struggled to understand something

### Documentation Style
```markdown
# Clear, Helpful, Friendly

## Feature Name

**What it does**: One-line summary

**Why it exists**: The problem it solves

**How to use it**:
1. Step one with example
2. Step two with explanation
3. Step three with result

**Example**:
```code
Real, working example
```

**Common issues**:
- Issue 1: Solution
- Issue 2: Solution

**Pro tips**:
- Tip that makes life easier
- Another helpful hint
```

## 🔄 Pull Request Process

### Before Submitting
- [ ] Code follows style guidelines
- [ ] Tests pass locally
- [ ] Documentation updated if needed
- [ ] Commit messages are clear
- [ ] Branch is up to date with main

### PR Template
```markdown
## Description
Brief description of what this PR does

## Why
The problem this solves or value it adds

## Changes
- Change 1
- Change 2
- Change 3

## Testing
How I tested this:
- [ ] Manual testing steps
- [ ] Automated tests added
- [ ] Edge cases considered

## Screenshots (if UI changes)
Before: [screenshot]
After: [screenshot]

## Questions/Notes
Any concerns or discussion points
```

### Review Process
1. **Automated checks** run (tests, linting)
2. **Code review** by maintainer
3. **Discussion** if needed
4. **Updates** based on feedback
5. **Merge** when ready!

## 🌟 Recognition

### Contributors Hall of Fame
We recognize all contributors in our README! Your contributions, no matter how small, are valued and appreciated.

### Types of Contributions
- 💻 Code
- 📖 Documentation
- 🐛 Bug reports
- 💡 Ideas
- 🎨 Design
- 🧪 Testing
- 📢 Promotion

## ❓ Questions?

### Getting Help
- **Check documentation** first
- **Search existing issues**
- **Ask in discussions**
- **Open an issue** if still stuck

### Good Questions Include
- What you're trying to do
- What you've already tried
- Error messages (if any)
- Your environment details

## 🚫 What NOT to Do

Please don't:
- Submit PRs with broken tests
- Change code style without discussion
- Add dependencies without good reason
- Remove features without discussion
- Be mean to other contributors

## 💡 Final Tips

1. **Start small** - First PR doesn't need to be huge
2. **Ask questions** - We're here to help
3. **Be patient** - Reviews take time
4. **Have fun** - This should be enjoyable!

---

**Thank you for contributing! Together we're making PR analytics better for everyone!** 🎉

*These guidelines are living documents - suggest improvements!*