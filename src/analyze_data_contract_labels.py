"""
Data Contract Label Analysis Script
==================================

This script analyzes the current PR data to understand:
1. How many PRs have the "data contract" label
2. What variations of the label exist
3. Statistics about data contract PRs

Author: Aviv Support
Created: 2025-01-16
Purpose: Pre-implementation analysis for data contract filter feature
"""

import pandas as pd
import json
from pathlib import Path
import logging

# Set up logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


def analyze_data_contract_labels(csv_path: str = 'data/pr_metrics_all_prs.csv'):
    """
    Analyze data contract label usage in PR data.
    
    Args:
        csv_path: Path to the PR metrics CSV file
        
    Returns:
        Dictionary containing analysis results
    """
    logger.info("🔍 Starting Data Contract Label Analysis")
    
    try:
        # Load the data
        df = pd.read_csv(csv_path)
        logger.info(f"📊 Loaded {len(df)} PRs from {csv_path}")
        
        # Basic statistics
        total_prs = len(df)
        prs_with_labels = df[df['Labels'].notna() & (df['Labels'] != '')].shape[0]
        
        # Find all unique labels
        all_labels = []
        for labels in df['Labels'].dropna():
            if labels:
                all_labels.extend([label.strip() for label in labels.split(',')])
        
        unique_labels = sorted(set(all_labels))
        
        # Find data contract related labels (case-insensitive)
        data_contract_variations = []
        for label in unique_labels:
            if 'data' in label.lower() and 'contract' in label.lower():
                data_contract_variations.append(label)
        
        # Count PRs with data contract label
        data_contract_mask = df['Labels'].fillna('').str.contains(
            'data.*contract|contract.*data', 
            case=False, 
            regex=True
        )
        data_contract_prs = df[data_contract_mask]
        
        # Calculate statistics for data contract PRs
        dc_stats = {
            'total': len(data_contract_prs),
            'merged': len(data_contract_prs[data_contract_prs['Is_Merged'] == True]),
            'open': len(data_contract_prs[data_contract_prs['State'] == 'open']),
            'authors': data_contract_prs['Author'].nunique(),
            'avg_merge_time': data_contract_prs[data_contract_prs['Time_To_Merge_Hours'] != '']['Time_To_Merge_Hours'].astype(float).mean() if len(data_contract_prs[data_contract_prs['Time_To_Merge_Hours'] != '']) > 0 else 0
        }
        
        # Create analysis report
        analysis = {
            'summary': {
                'total_prs': total_prs,
                'prs_with_labels': prs_with_labels,
                'unique_labels_count': len(unique_labels),
                'data_contract_prs': dc_stats['total'],
                'data_contract_percentage': round((dc_stats['total'] / total_prs) * 100, 2)
            },
            'data_contract_stats': dc_stats,
            'label_variations': {
                'data_contract_variations': data_contract_variations,
                'all_unique_labels': unique_labels[:20]  # First 20 labels
            },
            'sample_data_contract_prs': []
        }
        
        # Add sample PRs
        if len(data_contract_prs) > 0:
            sample_prs = data_contract_prs.head(5)[['PR_Number', 'Title', 'Author', 'Labels', 'State', 'Is_Merged']]
            analysis['sample_data_contract_prs'] = sample_prs.to_dict('records')
        
        # Print analysis results
        logger.info("\n" + "="*60)
        logger.info("📊 ANALYSIS RESULTS")
        logger.info("="*60)
        
        logger.info(f"\n🔢 Summary:")
        logger.info(f"  - Total PRs: {analysis['summary']['total_prs']}")
        logger.info(f"  - PRs with labels: {analysis['summary']['prs_with_labels']}")
        logger.info(f"  - Unique labels: {analysis['summary']['unique_labels_count']}")
        logger.info(f"  - Data Contract PRs: {analysis['summary']['data_contract_prs']} ({analysis['summary']['data_contract_percentage']}%)")
        
        logger.info(f"\n📈 Data Contract PR Statistics:")
        logger.info(f"  - Total: {dc_stats['total']}")
        logger.info(f"  - Merged: {dc_stats['merged']} ({round(dc_stats['merged']/dc_stats['total']*100, 1)}%)" if dc_stats['total'] > 0 else "  - Merged: 0")
        logger.info(f"  - Currently Open: {dc_stats['open']}")
        logger.info(f"  - Unique Authors: {dc_stats['authors']}")
        logger.info(f"  - Avg Merge Time: {dc_stats['avg_merge_time']:.1f} hours" if dc_stats['avg_merge_time'] > 0 else "  - Avg Merge Time: N/A")
        
        if data_contract_variations:
            logger.info(f"\n🏷️ Data Contract Label Variations Found:")
            for label in data_contract_variations:
                logger.info(f"  - '{label}'")
        else:
            logger.info(f"\n⚠️ No 'data contract' label variations found!")
            logger.info("  This might mean:")
            logger.info("  1. The label hasn't been used yet")
            logger.info("  2. It's named differently (check all labels below)")
            
        logger.info(f"\n🏷️ Most Common Labels (first 10):")
        label_counts = pd.Series(all_labels).value_counts().head(10)
        for label, count in label_counts.items():
            logger.info(f"  - '{label}': {count} occurrences")
        
        # Save analysis results
        output_path = 'data/data_contract_label_analysis.json'
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(analysis, f, indent=2, default=str)
        logger.info(f"\n💾 Full analysis saved to: {output_path}")
        
        return analysis
        
    except Exception as e:
        logger.error(f"❌ Error during analysis: {str(e)}")
        raise


def check_label_formats(csv_path: str = 'data/pr_metrics_all_prs.csv'):
    """
    Check all label formats to understand naming conventions.
    
    This helps us implement robust label matching.
    """
    logger.info("\n🔍 Checking Label Formats")
    
    df = pd.read_csv(csv_path)
    
    # Get all non-empty label entries
    label_entries = df[df['Labels'].notna() & (df['Labels'] != '')]['Labels'].tolist()
    
    logger.info(f"\n📝 Sample Label Formats (first 10):")
    for i, labels in enumerate(label_entries[:10]):
        logger.info(f"  {i+1}. '{labels}'")
    
    # Check for common patterns
    patterns = {
        'hyphenated': 0,
        'spaced': 0,
        'underscored': 0,
        'camelCase': 0
    }
    
    all_labels = []
    for labels in label_entries:
        for label in labels.split(','):
            label = label.strip()
            all_labels.append(label)
            
            if '-' in label:
                patterns['hyphenated'] += 1
            if ' ' in label:
                patterns['spaced'] += 1
            if '_' in label:
                patterns['underscored'] += 1
            if any(c.isupper() for c in label[1:]):
                patterns['camelCase'] += 1
    
    logger.info(f"\n📊 Label Format Patterns:")
    for pattern, count in patterns.items():
        logger.info(f"  - {pattern}: {count} occurrences")
    
    return patterns


if __name__ == "__main__":
    # Run the analysis
    logger.info("🚀 Data Contract Label Analysis Tool")
    logger.info("="*60)
    
    try:
        # Main analysis
        analysis_results = analyze_data_contract_labels()
        
        # Format analysis
        label_patterns = check_label_formats()
        
        logger.info("\n✅ Analysis complete!")
        logger.info("\n💡 Implementation Recommendations:")
        
        if analysis_results['summary']['data_contract_prs'] > 0:
            logger.info("  1. ✅ Data contract labels exist - proceed with filter implementation")
            logger.info("  2. 🔍 Use case-insensitive matching for robustness")
            logger.info("  3. 📊 Consider showing data contract metrics separately")
        else:
            logger.info("  1. ⚠️ No data contract labels found yet")
            logger.info("  2. 💡 Implement filter anyway for future use")
            logger.info("  3. 📝 Document the expected label format for teams")
            logger.info("  4. 🏷️ Consider which existing labels might be data contract related")
        
    except Exception as e:
        logger.error(f"❌ Analysis failed: {str(e)}")
        exit(1)
