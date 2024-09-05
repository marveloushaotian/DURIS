import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import argparse
from scipy.stats import f_oneway
import numpy as np

def create_boxplot(input_file, output_file, final_result_column):
    # Step 1: Load the data
    df = pd.read_csv(input_file)

    # Step 2: Create new columns for combined grouping
    df['Group'] = df['Contig_Classification'] + '_' + df['Country'] + '_' + df['Location']

    # Step 3: Create the boxplot
    plt.figure(figsize=(30, 10))  # Increased figure width
    ax = sns.boxplot(x='Group', y=final_result_column, data=df, showfliers=False,
                     order=sorted(df['Group'].unique(), key=lambda x: (x.split('_')[0], x.split('_')[1], x.split('_')[2])))
    sns.stripplot(x='Group', y=final_result_column, data=df, color='#1E2040', alpha=0.5, jitter=True,
                  order=sorted(df['Group'].unique(), key=lambda x: (x.split('_')[0], x.split('_')[1], x.split('_')[2])))

    # Step 4: Customize plot
    ax.set(xlabel=None)  # Remove the x-axis label
    plt.ylabel('Defense Number per GB')
    plt.xticks(rotation=90, ha='right')
    plt.grid(True, axis='y')

    # Adjust x-axis labels
    plt.xticks(fontsize=8)  # Reduce font size of x-axis labels
    plt.gcf().subplots_adjust(bottom=0.2)  # Add more space at the bottom

    # Add vertical lines to separate Contig_Classification groups
    contig_classes = df['Contig_Classification'].unique()
    current_tick = -0.5
    for i, cc in enumerate(contig_classes):
        if i > 0:
            plt.axvline(x=current_tick, color='red', linestyle='--')
        current_tick += sum(df['Contig_Classification'] == cc)

    # ANOVA test and annotate p-values for Location groups within each Country and Contig_Classification
    groups = sorted(df['Group'].unique(), key=lambda x: (x.split('_')[0], x.split('_')[1], x.split('_')[2]))
    y_max = df[final_result_column].max()

    for i in range(0, len(groups) - 1):
        g1_parts = groups[i].split('_')
        g2_parts = groups[i+1].split('_')
        
        if g1_parts[0] == g2_parts[0] and g1_parts[1] == g2_parts[1]:  # Same Contig_Classification and Country
            data1 = df[df['Group'] == groups[i]][final_result_column]
            data2 = df[df['Group'] == groups[i+1]][final_result_column]
            
            stat, p_value = f_oneway(data1, data2)
            if p_value < 0.05:
                x1, x2 = i, i + 1
                y, h, col = y_max + 0.05 * y_max, 0.02 * y_max, 'k'
                plt.plot([x1, x1, x2, x2], [y, y+h, y+h, y], lw=1.5, c=col)
                plt.text((x1 + x2) * .5, y + h, f"p={p_value:.3e}", ha='center', va='bottom', color=col, fontsize=6)

    # Step 5: Save and show plot
    plt.tight_layout()
    plt.savefig(output_file, format='pdf', bbox_inches='tight', dpi=300)  # Increased DPI for better resolution
    plt.show()

def main():
    # Argument parsing
    parser = argparse.ArgumentParser(description='Generate boxplot for Final Results by Contig Classification, Country, and Location.')
    parser.add_argument('-i', '--input', required=True, help='Path to the input file (CSV format)')
    parser.add_argument('-o', '--output', required=True, help='Path to save the output plot (PDF format)')
    parser.add_argument('-c', '--column', required=True, help='Name of the column representing Final Result')

    args = parser.parse_args()

    # Call the function with provided arguments
    create_boxplot(args.input, args.output, args.column)

if __name__ == '__main__':
    main()
