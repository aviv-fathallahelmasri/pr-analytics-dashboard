# Data Contract Filter Feature - Deployment Guide

## 📋 Overview

This guide provides step-by-step instructions for deploying the new data contract label filter feature to your GitHub PR Analytics Dashboard.

## 🚀 Deployment Steps

### Step 1: Pre-Deployment Analysis (15 minutes)

1. **Run the analysis script** to understand current data:
   ```bash
   cd C:\Users\FElmasri\Desktop\github-pr-analytics
   python src/analyze_data_contract_labels.py
   ```
   
   This will:
   - Count existing data contract PRs
   - Identify label variations
   - Generate analysis report in `data/data_contract_label_analysis.json`

2. **Review the analysis output** to understand:
   - How many PRs currently have data contract labels
   - What label formats are being used
   - Whether the feature will provide immediate value

### Step 2: Test the Implementation (20 minutes)

1. **Run the test suite**:
   ```bash
   python src/test_data_contract_filter.py
   ```
   
   This validates:
   - Label detection logic
   - Filter functionality
   - Metrics calculation
   - Edge case handling
   - Performance benchmarks

2. **Review test results** in `data/data_contract_filter_test_report.json`

3. **Fix any failing tests** before proceeding

### Step 3: Backup Current Dashboard (5 minutes)

1. **Create a backup** of the current index.html:
   ```bash
   copy index.html index_backup_20250116.html
   ```

2. **Verify backup** was created successfully

### Step 4: Deploy New Dashboard (10 minutes)

1. **Replace the current dashboard**:
   ```bash
   copy index_with_data_contract_filter.html index.html
   ```

2. **Test locally** by opening index.html in your browser:
   - Verify all existing features work
   - Test the new PR Type filter
   - Check that metrics update correctly
   - Ensure charts reflect filter changes

### Step 5: Push to GitHub (10 minutes)

1. **Stage changes**:
   ```bash
   git add index.html
   git add src/analyze_data_contract_labels.py
   git add src/test_data_contract_filter.py
   git add docs/feature-implementations/data-contract-filter-implementation.md
   git add docs/feature-implementations/data-contract-filter-deployment.md
   ```

2. **Commit with descriptive message**:
   ```bash
   git commit -m "feat: add data contract label filter to PR analytics dashboard

   - Added PR Type filter with options: All PRs, Data Contract PRs, Non-Data Contract PRs
   - Enhanced KPIs to show filter indicators when active
   - Added comparison section for data contract vs other PRs
   - Updated table to highlight data contract labels
   - Charts adapt colors when data contract filter is active
   - Comprehensive testing and documentation included"
   ```

3. **Push to remote**:
   ```bash
   git push origin main
   ```

### Step 6: Verify GitHub Pages Deployment (15 minutes)

1. **Wait for GitHub Actions** to complete the deployment (usually 2-5 minutes)

2. **Visit your live dashboard**: https://aviv-fathallahelmasri.github.io/pr-analytics-dashboard/

3. **Test the deployed version**:
   - [ ] Filter dropdown appears and works
   - [ ] KPIs update when filter is applied
   - [ ] Charts reflect filtered data
   - [ ] Comparison section shows when appropriate
   - [ ] Labels column shows in table with highlighting
   - [ ] Performance is acceptable

### Step 7: Post-Deployment Validation (10 minutes)

1. **Monitor for issues**:
   - Check browser console for errors
   - Verify data loads correctly
   - Test all filter combinations

2. **Document any issues** found and their resolutions

## 🔧 Rollback Procedure

If issues are discovered:

1. **Immediate rollback**:
   ```bash
   copy index_backup_20250116.html index.html
   git add index.html
   git commit -m "revert: rollback data contract filter due to [issue description]"
   git push origin main
   ```

2. **Investigate and fix** the issue in development

3. **Re-test thoroughly** before attempting deployment again

## 📊 Success Metrics

Monitor these metrics post-deployment:

1. **Usage Metrics**:
   - How often is the data contract filter used?
   - Which filter option is most popular?

2. **Performance Metrics**:
   - Page load time remains under 2 seconds
   - Filter application takes less than 100ms

3. **Data Quality**:
   - Correct count of data contract PRs
   - Accurate metric calculations

## 🎯 Feature Usage Guide

### For End Users:

1. **Using the Filter**:
   - Select "Data Contract PRs" to see only PRs with data contract labels
   - Select "Non-Data Contract PRs" to see all other PRs
   - Select "All PRs" to see everything (default)

2. **Understanding Indicators**:
   - Purple borders on KPI cards indicate data contract filter is active
   - "DC" or "Non-DC" badges show which filter is applied
   - Purple highlighting in tables shows data contract labels

3. **Comparison View**:
   - Available when viewing "All PRs"
   - Shows side-by-side metrics for data contract vs other PRs
   - Helps identify process differences

### For Developers:

1. **Adding Labels in GitHub**:
   - Use "data contract" label (case-insensitive)
   - Also matches "data-contract" format
   - Can be combined with other labels

2. **Label Best Practices**:
   - Apply consistently to all data contract related PRs
   - Use alongside other descriptive labels
   - Consider automation for label application

## 🐛 Troubleshooting

### Common Issues:

1. **Filter not showing**:
   - Clear browser cache
   - Check for JavaScript errors
   - Verify index.html was updated

2. **Incorrect counts**:
   - Run analysis script to verify data
   - Check label format consistency
   - Ensure CSV data is current

3. **Performance issues**:
   - Check dataset size
   - Monitor browser memory usage
   - Consider pagination for large datasets

## 📝 Maintenance

### Weekly:
- Monitor filter usage patterns
- Check for new label variations
- Verify metric accuracy

### Monthly:
- Review and update documentation
- Analyze feature adoption
- Gather user feedback

### Quarterly:
- Performance optimization review
- Feature enhancement planning
- Label standardization assessment

## 🎉 Deployment Complete!

Once all steps are verified, the data contract filter feature is live and ready for use. The dashboard now provides focused insights into data contract development velocity and quality metrics.

**Next Steps**:
1. Announce the new feature to the team
2. Provide training if needed
3. Collect feedback for improvements
4. Monitor adoption and usage patterns

---

**Support**: If you encounter any issues, please check the troubleshooting section or create an issue in the repository.
