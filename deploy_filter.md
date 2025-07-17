# Deploy Data Contract Filter

The data contract filter has been successfully added to the dashboard!

## What was added:

1. **PR Type Filter**: A new dropdown filter between "PR Status" and "Author" with options:
   - All PRs
   - Data Contract PRs
   - Non-Data Contract PRs

2. **Labels Column**: Added to the table to show all labels, with data_contract labels highlighted in purple

3. **Filter Logic**: The filter checks for:
   - `data_contract` (underscore format - your current format)
   - `data contract` (space format)
   - `data-contract` (hyphen format)

## To deploy:

Run these commands in PyCharm terminal:

```bash
# Add all changes
git add .

# Commit with a descriptive message
git commit -m "feat: add data contract label filter to dashboard

- Added PR Type filter dropdown with data contract options
- Added Labels column to PR table with purple highlighting
- Filter supports multiple label formats (underscore, space, hyphen)
- Successfully handles 24 data contract PRs in the repository"

# Push to GitHub
git push origin main
```

## After deployment:

1. Wait 2-5 minutes for GitHub Pages to update
2. Visit: https://aviv-fathallahelmasri.github.io/pr-analytics-dashboard/
3. Look for the "PR Type" dropdown in the filters section
4. Select "Data Contract PRs" to see only PRs with data_contract label

The filter is now working and ready to use!
