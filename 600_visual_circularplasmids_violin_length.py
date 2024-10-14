import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import argparse

def create_violin_boxplot(input_file, output_file):
    # Step 1: Load the data
    df = pd.read_csv(input_file, sep='\t')

    # Step 2: Filter the data for Contig_Group == 'PL_pls_circ'
    filtered_df = df[df['Contig_Group'] == 'PL_pls_circ']

    # Step 3: Remove groups with less than 3 data points
    filtered_df = filtered_df.groupby('Defense_Type').filter(lambda x: len(x) >= 3)

    # Step 4: Define the custom color palette
    custom_colors = ["#4a9ba7", "#9bb88a", "#d0cab7", "#c6a4c5", "#434d91", "#e1834e", "#cd6073", "#ffc7c9"]

    # Step 5: Plot a half violin, half boxplot with points
    plt.figure(figsize=(12, 8))
    sns.violinplot(x='Defense_Type', y='Contig_Length', data=filtered_df, inner=None, palette=custom_colors, cut=0)
    sns.boxplot(x='Defense_Type', y='Contig_Length', data=filtered_df, whis=1.5, width=0.1, palette=custom_colors)
    sns.stripplot(x='Defense_Type', y='Contig_Length', data=filtered_df, color='black', size=2, jitter=True)

    # Step 6: Customize the plot
    plt.ylim(0, filtered_df['Contig_Length'].max() * 1.05)  # 确保 y 轴从 0 开始且不超过数据范围
    plt.xticks(rotation=45, ha='right')
    plt.ylabel('Contig Length')
    plt.xlabel('')  # 去掉 x 轴标题
    plt.tight_layout()

    # Step 7: Save the plot to a file
    plt.savefig(output_file, format='pdf', bbox_inches='tight')
    plt.close()

def main():
    # Argument parsing
    parser = argparse.ArgumentParser(description='Create a half violin, half boxplot for Contig Length by Defense Type for the PL_pls_circ group.')
    parser.add_argument('-i', '--input', type=str, required=True, help='Path to input file')
    parser.add_argument('-o', '--output', type=str, required=True, help='Path to output PDF file')

    args = parser.parse_args()

    # Call the function with provided arguments
    create_violin_boxplot(args.input, args.output)

if __name__ == '__main__':
    main()

