# Data Contract Label Filter - Implementation Plan

## 📋 Feature Overview

**Objective**: Add filtering capability to show only PRs labeled as "data contract" in the dashboard

**Business Value**: 
- Focus on data contract-related PRs for specialized analysis
- Quick insights into data contract development velocity
- Separate metrics for data contract vs. other PRs

## 🔍 Current State Analysis

### Data Structure
- **Labels Field**: Already exists in `pr_metrics_all_prs.csv` as comma-separated values
- **Example**: `"dependencies, python"` or `"data contract, enhancement"`
- **Current PRs**: 210 total (need to identify how many have "data contract" label)

### Dashboard Architecture
1. **Data Loading**: JavaScript reads CSV and parses into objects
2. **Filtering**: Currently supports date range and author filtering
3. **Visualization**: Charts update dynamically based on filtered data

## 🎯 Implementation Strategy

### Phase 1: Backend Data Enhancement ✅
**No changes needed** - The label data is already being collected in `fetch_pr_data.py`

### Phase 2: Frontend Filter Addition 🔧

#### 2.1 UI Components
```html
<!-- Add to filters section in index.html -->
<div class="filter-group">
    <label for="labelFilter">PR Type:</label>
    <select id="labelFilter">
        <option value="all">All PRs</option>
        <option value="data-contract">Data Contract PRs</option>
        <option value="non-data-contract">Non-Data Contract PRs</option>
    </select>
</div>
```

#### 2.2 JavaScript Filter Logic
```javascript
// Add to existing filter function
function applyFilters() {
    const labelFilter = document.getElementById('labelFilter').value;
    
    filteredData = allData.filter(pr => {
        // Existing filters...
        
        // Label filter
        if (labelFilter !== 'all') {
            const hasDataContractLabel = pr.Labels && 
                pr.Labels.toLowerCase().includes('data contract');
            
            if (labelFilter === 'data-contract' && !hasDataContractLabel) {
                return false;
            }
            if (labelFilter === 'non-data-contract' && hasDataContractLabel) {
                return false;
            }
        }
        
        return true;
    });
    
    updateDashboard(filteredData);
}
```

### Phase 3: Enhanced Analytics 📊

#### 3.1 New KPI Cards
- **Data Contract PR Count**: Total PRs with data contract label
- **Data Contract Merge Rate**: Merge rate specifically for data contract PRs
- **Data Contract Review Time**: Average review time for data contract PRs

#### 3.2 Comparison Visualizations
- **Side-by-side comparison**: Data contract vs. other PRs
- **Trend analysis**: Data contract PR velocity over time

## 📝 Implementation Steps

### Step 1: Analyze Current Data
```python
# Quick analysis script to understand data contract label usage
import pandas as pd

df = pd.read_csv('data/pr_metrics_all_prs.csv')
data_contract_prs = df[df['Labels'].str.contains('data contract', case=False, na=False)]
print(f"Total PRs with 'data contract' label: {len(data_contract_prs)}")
print(f"Percentage of data contract PRs: {len(data_contract_prs)/len(df)*100:.1f}%")
```

### Step 2: Update HTML Structure
1. Add filter dropdown to existing filters section
2. Add new KPI cards for data contract metrics
3. Add comparison chart container

### Step 3: Enhance JavaScript
1. Update data loading to parse labels properly
2. Add filter logic for data contract label
3. Create specialized calculations for data contract metrics
4. Update all charts to respect the new filter

### Step 4: Testing
1. Verify filter works with edge cases (no labels, multiple labels)
2. Ensure performance remains optimal with additional filtering
3. Test filter persistence across page reloads
4. Validate metrics accuracy

### Step 5: Documentation
1. Update user guide with new filter instructions
2. Document the label format expectations
3. Add troubleshooting for common issues

## 🔧 Technical Considerations

### Label Matching Strategy
- **Case-insensitive**: Match "data contract", "Data Contract", "DATA CONTRACT"
- **Partial matching**: Also match "data-contract", "datacontract"
- **Flexible**: Handle PRs with multiple labels gracefully

### Performance Optimization
- **Client-side filtering**: No server calls needed
- **Efficient string matching**: Use optimized JavaScript methods
- **Caching**: Store parsed label arrays to avoid repeated splitting

### Edge Cases
1. **No labels**: PRs without any labels
2. **Multiple labels**: PRs with many labels including "data contract"
3. **Label variations**: Different formats of the data contract label
4. **Empty data**: Handle case where no data contract PRs exist

## 📊 Expected Outcome

### User Experience
1. **Single click filtering**: Easy toggle between all PRs and data contract PRs
2. **Instant updates**: All metrics and charts update immediately
3. **Clear indicators**: Visual cues showing active filter

### Analytics Value
1. **Focused insights**: Dedicated metrics for data contract work
2. **Trend identification**: Track data contract PR velocity
3. **Quality metrics**: Review and merge patterns for data contracts

## 🚀 Future Enhancements

1. **Multiple label filters**: Filter by any label, not just data contract
2. **Label statistics**: Show distribution of all labels
3. **Custom label groups**: Define custom groupings of labels
4. **Export filtered data**: Download CSV of filtered results

## ⏱️ Implementation Timeline

- **Step 1**: 15 minutes - Data analysis
- **Step 2**: 30 minutes - HTML updates
- **Step 3**: 45 minutes - JavaScript enhancements
- **Step 4**: 30 minutes - Testing
- **Step 5**: 20 minutes - Documentation
- **Total**: ~2.5 hours

## 🎯 Success Criteria

1. ✅ Filter dropdown visible and functional
2. ✅ All metrics update correctly when filtered
3. ✅ Performance remains fast (< 100ms filter application)
4. ✅ No breaking changes to existing functionality
5. ✅ Clear documentation for users

## 🔍 Validation Queries

```sql
-- If this were SQL, these would be our test queries
-- Total data contract PRs
SELECT COUNT(*) FROM prs WHERE labels LIKE '%data contract%';

-- Data contract merge rate
SELECT 
    COUNT(CASE WHEN is_merged = true THEN 1 END) * 100.0 / COUNT(*) as merge_rate
FROM prs 
WHERE labels LIKE '%data contract%';

-- Average merge time for data contract PRs
SELECT AVG(time_to_merge_hours) 
FROM prs 
WHERE labels LIKE '%data contract%' AND is_merged = true;
```

---

**Ready to implement?** This plan provides a complete roadmap for adding the data contract filter feature while maintaining the high quality and performance standards of your dashboard.
