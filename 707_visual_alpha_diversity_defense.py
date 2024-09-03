import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import argparse
from scipy.stats import entropy

def calculate_shannon_diversity(row):
    """Calculate Shannon diversity index for a row of abundance data."""
    proportions = row / row.sum()
    return entropy(proportions)

def create_alpha_diversity_boxplot(abundance_file, group_file, output_file, title=None):
    # Step 1: Load the data
    abundance_df = pd.read_csv(abundance_file, sep='\t', index_col=0)
    group_df = pd.read_csv(group_file, sep='\t')

    # Step 2: Calculate Shannon diversity for each Sample
    shannon_diversity = abundance_df.apply(calculate_shannon_diversity, axis=0)
    shannon_diversity = pd.DataFrame(shannon_diversity, columns=['Shannon_Diversity'])

    # Step 3: Merge the diversity data with the group information
    merged_df = pd.merge(shannon_diversity, group_df, left_index=True, right_on='Sample')

    # Step 4: Plot the boxplot for each Location_BAF group
    plt.figure(figsize=(4, 6))  # 调整图像大小
    sns.boxplot(x='Location_BAF', y='Shannon_Diversity', data=merged_df, palette=["#b58db3", "#428085"])
    sns.stripplot(x='Location_BAF', y='Shannon_Diversity', data=merged_df, color='black', size=3, jitter=True)

    # Step 5: Customize the plot
    plt.ylabel('Shannon Diversity Index')
    plt.xlabel('')  # Remove x-axis label
    plt.xticks(rotation=0, ha='center')  # x轴标签水平居中
    if title:
        plt.title(title)
    plt.tight_layout()

    # Step 6: Save the plot to a file
    plt.savefig(output_file, format='pdf', bbox_inches='tight')
    plt.close()

def main():
    # Argument parsing
    parser = argparse.ArgumentParser(description='Create a boxplot of Alpha diversity (Shannon index) by Location_BAF.')
    parser.add_argument('-a', '--abundance', type=str, required=True, help='Path to chromosome_to_metagenome_abundance.txt')
    parser.add_argument('-g', '--group', type=str, required=True, help='Path to Sample_Group_BAF.txt')
    parser.add_argument('-o', '--output', type=str, required=True, help='Path to output PDF file')
    parser.add_argument('-t', '--title', type=str, default=None, help='Title for the plot')

    args = parser.parse_args()

    # Call the function with provided arguments
    create_alpha_diversity_boxplot(args.abundance, args.group, args.output, args.title)

if __name__ == '__main__':
    main()

