import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import argparse
from scipy.stats import entropy
from itertools import combinations
from scipy.stats import mannwhitneyu
from statannot import add_stat_annotation

def calculate_shannon_diversity(row):
    """Calculate Shannon diversity index for a row of abundance data."""
    proportions = row / row.sum()
    return entropy(proportions)

def perform_pairwise_permanova(data, group_col, value_col):
    """Perform pairwise PERMANOVA (Mann-Whitney U test) between groups."""
    groups = data[group_col].unique()
    results = {}
    for g1, g2 in combinations(groups, 2):
        group1 = data[data[group_col] == g1][value_col]
        group2 = data[data[group_col] == g2][value_col]
        statistic, p_value = mannwhitneyu(group1, group2)
        results[(g1, g2)] = p_value
    return results

def create_alpha_diversity_boxplot(abundance_file, group_file, output_file, title=None):
    # Step 1: Load the data
    abundance_df = pd.read_csv(abundance_file, index_col=0)
    group_df = pd.read_csv(group_file)

    # Step 2: Calculate Shannon diversity for each Sample
    shannon_diversity = abundance_df.apply(calculate_shannon_diversity, axis=0)
    shannon_diversity = pd.DataFrame(shannon_diversity, columns=['Shannon_Diversity'])

    # Step 3: Merge the diversity data with the group information
    merged_df = pd.merge(shannon_diversity, group_df, left_index=True, right_on='Sample')

    # Step 4: Plot the boxplot for each Location group
    plt.figure(figsize=(3, 8))  # Increased figure size for better visibility
    ax = sns.boxplot(x='Location', y='Shannon_Diversity', data=merged_df, palette=["#6566aa", "#8fced1", "#f07e40", "#dc5772"])
    sns.stripplot(x='Location', y='Shannon_Diversity', data=merged_df, color='black', size=3, jitter=True, alpha=0.5)

    # Adjust y-axis limits to leave space for annotations within the plot
    y_min, y_max = ax.get_ylim()
    y_range = y_max - y_min
    ax.set_ylim(y_min, y_max + 0.15 * y_range)

    # Step 5: Add significance annotations using statannot, but only for significant pairs
    box_pairs = list(combinations(merged_df['Location'].unique(), 2))
    pvalues = [perform_pairwise_permanova(merged_df, 'Location', 'Shannon_Diversity')[pair] for pair in box_pairs]
    
    # Filter out non-significant pairs
    significant_pairs = [(pair, pvalue) for pair, pvalue in zip(box_pairs, pvalues) if pvalue < 0.05]
    
    if significant_pairs:
        add_stat_annotation(ax, data=merged_df, x='Location', y='Shannon_Diversity',
                            box_pairs=[pair for pair, _ in significant_pairs],
                            perform_stat_test=False,  # Disable automatic statistical testing
                            pvalues=[pvalue for _, pvalue in significant_pairs],
                            text_format='star', loc='inside', verbose=2,
                            comparisons_correction=None,  # No correction for multiple comparisons
                            show_test_name=False,  # Don't show test name
                            pvalue_thresholds=[[1e-4, "****"], [1e-3, "***"], [1e-2, "**"], [0.05, "*"]],
                            line_height=0.02,  # Reduce the line height between annotations
                            text_offset=0.01)  # Reduce the text offset

    # Step 6: Customize the plot
    plt.ylabel('Shannon Diversity Index', fontsize=14, fontweight='bold')
    plt.xlabel('')  # Remove x-axis label
    plt.xticks(rotation=0, ha='center', fontsize=14, fontweight='bold')  # Center x-axis labels horizontally
    plt.yticks(rotation=0, ha='right', fontsize=12, fontweight='bold')
    if title:
        plt.title(title, fontsize=16, fontweight='bold')
    
    plt.tight_layout()

    # Step 7: Save the plot to a file
    plt.savefig(output_file, format='pdf', bbox_inches='tight', dpi=300)
    plt.close()

def main():
    # Argument parsing
    parser = argparse.ArgumentParser(description='Create a boxplot of Alpha diversity (Shannon index) by Location with significant pairwise comparisons.')
    parser.add_argument('-a', '--abundance', type=str, required=True, help='Path to chromosome_to_metagenome_abundance.csv')
    parser.add_argument('-g', '--group', type=str, required=True, help='Path to Sample_Group_BAF.csv')
    parser.add_argument('-o', '--output', type=str, required=True, help='Path to output PDF file')
    parser.add_argument('-t', '--title', type=str, default=None, help='Title for the plot')

    args = parser.parse_args()

    # Call the function with provided arguments
    create_alpha_diversity_boxplot(args.abundance, args.group, args.output, args.title)

if __name__ == '__main__':
    main()
