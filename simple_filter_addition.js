// Simple Data Contract Filter Addition
// Add this to the existing index.html file

// 1. In the HTML filters section, add this after the PR Status filter:
/*
<div class="filter-group">
    <label>PR Type</label>
    <select id="labelFilter">
        <option value="all">All PRs</option>
        <option value="data-contract">Data Contract PRs</option>
        <option value="non-data-contract">Non-Data Contract PRs</option>
    </select>
</div>
*/

// 2. In the applyFilters() function, add this filter logic:
/*
const labelFilter = document.getElementById('labelFilter').value;

// Inside the filter function, add:
if (labelFilter !== 'all') {
    const labels = pr.Labels ? pr.Labels.toLowerCase() : '';
    const hasDataContract = labels.includes('data_contract') || 
                           labels.includes('data contract') || 
                           labels.includes('data-contract');
    
    if (labelFilter === 'data-contract' && !hasDataContract) return false;
    if (labelFilter === 'non-data-contract' && hasDataContract) return false;
}
*/

// This is a minimal implementation that should work without breaking the dashboard