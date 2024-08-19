import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import argparse
import logging
from tqdm import tqdm
from scipy.stats import f_oneway
import numpy as np

# Set up logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def create_boxplot(input_file, output_file, final_result_column):
    # Step 1: Load the data
    logging.info(f"Loading data from {input_file}")
    df = pd.read_csv(input_file, sep='\t')
    
    # Step 2: Create a new column for combined grouping
    logging.info("Creating combined grouping column")
    df['Group'] = df['Contig_Group'] + '_' + df['Location_BAF']
    
    sns.set_palette(["#BF7EA2"])
    
    # Step 3: Create the boxplot
    plt.figure(figsize=(10, 8))
    ax = sns.boxplot(x='Group', y=final_result_column, data=df, showfliers=False)
    sns.stripplot(x='Group', y=final_result_column, data=df, color='#1E2040', alpha=0.5, jitter=True)
    
    # Step 4: Customize plot
    ax.set(xlabel=None)  # Remove the x-axis label
    plt.ylabel('Defense Number per GB')
    plt.xticks(rotation=45, ha='right')
    plt.grid(True, axis='y')
    
    # Center x-axis labels
    ax.set_xticklabels(ax.get_xticklabels(), rotation=45, ha='right')
    
    # ANOVA test and annotate p-values for adjacent groups
    groups = df['Group'].unique()
    y_max = df[final_result_column].max()
    
    for i in range(0, len(groups) - 1, 2):
        g1, g2 = groups[i], groups[i + 1]
        data1 = df[df['Group'] == g1][final_result_column]
        data2 = df[df['Group'] == g2][final_result_column]
        stat, p_value = f_oneway(data1, data2)
        if p_value < 0.05:
            x1, x2 = i, i + 1
            y, h, col = y_max + (i // 2) * 0.1, 0.02, 'k'
            plt.plot([x1, x1, x2, x2], [y, y+h, y+h, y], lw=1.5, c=col)
            plt.text((x1 + x2) * .5, y + h, f"p={p_value:.3e}", ha='center', va='bottom', color=col, fontsize=8)
    
    # Step 5: Save and show plot
    plt.tight_layout()
    logging.info(f"Saving plot to {output_file}")
    plt.savefig(output_file, format='pdf')
    plt.show()

def main():
    # Argument parsing
    parser = argparse.ArgumentParser(description='Generate a boxplot for Final Results by Contig Group and Location BAF.')
    parser.add_argument('-i', '--input', required=True, help='Path to the input file (Grouped_Statistics.txt)')
    parser.add_argument('-o', '--output', required=True, help='Path to save the output plot (PDF format)')
    parser.add_argument('-c', '--column', required=True, help='Name of the column representing Final Result')
    
    args = parser.parse_args()
    
    # Call the function with provided arguments
    create_boxplot(args.input, args.output, args.column)

if __name__ == '__main__':
    main()

