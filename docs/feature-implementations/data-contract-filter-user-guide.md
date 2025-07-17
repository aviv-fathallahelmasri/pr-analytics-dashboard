# Data Contract Filter - User Guide

## 🎯 What's New?

The GitHub PR Analytics Dashboard now includes a **Data Contract Filter** that allows you to focus specifically on pull requests related to data contracts. This powerful feature helps you:

- 📊 Track data contract development velocity
- 🎯 Monitor quality metrics for data contract work
- 📈 Compare data contract PRs with other development work
- 🔍 Identify patterns and bottlenecks in data contract processes

## 🚀 How to Use the Filter

### Basic Usage

1. **Locate the PR Type Filter**
   - Find the "PR Type" dropdown in the filters section
   - It's positioned between "PR Status" and "Author" filters

2. **Select Your View**:
   - **All PRs** (default): Shows all pull requests
   - **Data Contract PRs**: Shows only PRs with "data contract" labels
   - **Non-Data Contract PRs**: Shows all other PRs

3. **Apply the Filter**
   - Click the green "Apply Filters" button
   - All metrics and charts will instantly update

### Visual Indicators

When a data contract filter is active, you'll see:

1. **Purple Highlights**:
   - Filter dropdown gets a purple border
   - KPI cards show purple accents
   - Charts use purple color scheme

2. **Filter Badges**:
   - KPI cards display "DC" (Data Contract) or "Non-DC" badges
   - Indicates which filter is currently active

3. **Label Highlighting**:
   - Data contract labels in the PR table are highlighted in purple
   - Makes it easy to spot data contract PRs at a glance

## 📊 Understanding the Metrics

### When "Data Contract PRs" is Selected

All metrics show values for data contract PRs only:

- **Total PRs**: Count of all data contract PRs
- **Merge Rate**: Percentage of data contract PRs that were merged
- **Avg Merge Time**: How quickly data contract PRs get merged
- **Review Coverage**: Percentage of data contract PRs that received reviews
- **Fast Merges**: Percentage merged within 24 hours

### Comparison View

When viewing "All PRs", a comparison section appears showing:

1. **Data Contract PRs**:
   - Total count
   - Merge rate
   - Average merge time
   - Review coverage

2. **Other PRs**:
   - Same metrics for non-data contract PRs
   - Allows direct comparison

## 🏷️ Label Requirements

For PRs to be recognized as data contract related:

### Supported Formats
- ✅ `data_contract` (underscore - **most common**)
- ✅ `data contract` (space)
- ✅ `Data Contract` (any capitalization)
- ✅ `data-contract` (hyphenated)
- ✅ Multiple labels: `data_contract, enhancement, bugfix`

### Not Supported
- ❌ `datacontract` (no space/hyphen/underscore)
- ❌ `contract data` (reversed order)
- ❌ `contract_data` (reversed with underscore)

## 💡 Best Practices

### For Developers

1. **Consistent Labeling**:
   - Always add "data_contract" label to relevant PRs (underscore format is standard)
   - Add the label when creating the PR
   - Use GitHub's label templates for consistency

2. **Combine with Other Labels**:
   - Use descriptive labels alongside "data_contract"
   - Examples: `data_contract, feature`, `data_contract, bugfix`

### For Managers

1. **Track Trends**:
   - Monitor data contract PR velocity over time
   - Compare merge rates between data contract and other PRs
   - Identify if data contract PRs need different processes

2. **Quality Metrics**:
   - Ensure high review coverage for data contract changes
   - Track merge times to identify bottlenecks
   - Use fast merge rate to measure team efficiency

## 🔍 Use Cases

### 1. Sprint Planning
- Filter by "Data Contract PRs" to see work in progress
- Check open vs merged ratios
- Identify authors working on data contracts

### 2. Quality Assurance
- Verify all data contract PRs have reviews
- Check merge times against SLAs
- Monitor for PRs missing reviews

### 3. Performance Analysis
- Compare data contract vs other PR metrics
- Identify if data contracts need special attention
- Track improvement over time

### 4. Team Insights
- See which team members work on data contracts
- Identify knowledge gaps or training needs
- Balance workload across the team

## ❓ Frequently Asked Questions

### Q: Why don't I see any data contract PRs?

**A**: Check that:
- PRs are properly labeled with "data_contract" (with underscore)
- The label spelling matches supported formats
- The data has been refreshed (check last update time)

### Q: Can I combine filters?

**A**: Yes! You can use multiple filters together:
- Date range + Data contract filter
- Author + Data contract filter
- Status + Data contract filter

### Q: How often is the data updated?

**A**: The dashboard updates automatically every day at 8:00 AM Berlin time. Check the "Last Updated" timestamp at the top of the page.

### Q: Can I export filtered data?

**A**: Currently, you can:
- Take screenshots of filtered views
- Copy data from the table
- Future enhancement: CSV export planned

## 🐛 Troubleshooting

### Filter Not Working
1. Refresh the page (Ctrl+F5)
2. Clear browser cache
3. Check browser console for errors
4. Verify you clicked "Apply Filters"

### Incorrect Counts
1. Check PR labels in GitHub
2. Ensure labels match supported formats
3. Wait for next data refresh
4. Report persistent issues

### Performance Issues
1. Try a smaller date range
2. Clear other filters first
3. Use a modern browser (Chrome, Firefox, Edge)
4. Check your internet connection

## 🚀 Tips & Tricks

1. **Quick Comparison**: 
   - Apply "Data Contract PRs" filter
   - Note the metrics
   - Switch to "Non-Data Contract PRs"
   - Compare the differences

2. **Find Missing Labels**:
   - Look at the PR table
   - PRs about data contracts without purple labels need labeling
   - Add labels in GitHub for future tracking

3. **Trend Analysis**:
   - Use date range filters with PR type filter
   - Compare this month's data contract metrics to last month
   - Identify improvement areas

## 📧 Getting Help

If you need assistance:

1. **Check Documentation**: Review this guide and FAQ
2. **Ask Team Members**: Someone may have encountered the same issue
3. **Report Issues**: Create a GitHub issue with:
   - What you were trying to do
   - What happened instead
   - Browser and OS information
   - Screenshots if applicable

## 🎉 Start Exploring!

The data contract filter is a powerful tool for understanding your team's data contract development patterns. Start by selecting "Data Contract PRs" from the filter dropdown and discover insights about your data contract workflow!

---

**Remember**: Good data leads to good decisions. Use the filter to focus on what matters most to your team's success!
