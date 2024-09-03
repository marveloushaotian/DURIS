import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import argparse
from scipy.stats import f_oneway
import numpy as np

def create_stacked_bar_chart(input_file, output_file, value_column):
    # Step 1: Load the data
    df = pd.read_csv(input_file, sep='\t')

    # Step 2: Calculate the total proportion of each Defense_Type across all groups
    total_proportion = df.groupby('Defense_Type')[value_column].sum()
    top_defense_types = total_proportion.nlargest(20).index

    # Step 3: Filter the dataframe to retain only the top 20 defense types
    filtered_df = df[df['Defense_Type'].isin(top_defense_types)]

    # Step 4: Create a combined column for grouping
    filtered_df['Group'] = filtered_df['Contig_Group'] + '_' + filtered_df['Location_BAF']

    # Step 5: Pivot the data to have Defense_Type as columns and value_column as values
    pivot_df = filtered_df.pivot_table(index='Group', columns='Defense_Type', values=value_column, fill_value=0)

    # Step 6: Sort columns by the sum of values to have the most common defense types at the bottom
    pivot_df = pivot_df[pivot_df.sum().sort_values(ascending=False).index]

    # Step 7: Define a custom distinct color palette
    num_colors = pivot_df.shape[1]
    # custom_colors = sns.color_palette('tab20', num_colors)  # Use the tab20 color palette for distinct colors
    custom_colors = ["#c0dbe6","#2b526f","#4a9ba7","#a3cbd6","#c0cfbd","#9bb88a","#7b9b64","#d0cab7","#c6a4c5","#9b7baa","#7a7aaf","#434d91","#5284a2","#82b4c8","#9d795d","#d1b49a","#fff08c","#e1834e","#cd6073","#ffc7c9"]
    
    # Step 8: Split the data by Contig_Group and order each group
    contig_groups = filtered_df['Contig_Group'].unique()
    fig, axes = plt.subplots(1, len(contig_groups), figsize=(2.5 * len(contig_groups), 8), sharey=False)

    for i, contig_group in enumerate(contig_groups):
        ax = axes[i]
        group_df = pivot_df.filter(like=contig_group, axis=0)
        ordered_index = sorted(group_df.index, key=lambda x: ('BF' not in x, x))
        group_df = group_df.loc[ordered_index]

        # Plotting the stacked bar chart for the current Contig_Group
        group_df.plot(kind='bar', stacked=True, ax=ax, color=custom_colors, legend=False)

        # Add ANOVA test and annotate p-values for adjacent groups
        for j in range(0, len(group_df) - 1, 2):
            g1, g2 = group_df.index[j], group_df.index[j + 1]
            data1 = group_df.loc[g1]
            data2 = group_df.loc[g2]
            stat, p_value = f_oneway(data1, data2)
            if p_value < 0.05:
                y_max = max(data1.sum(), data2.sum())
                x1, x2 = j, j + 1
                y, h, col = y_max + 0.1, 0.02, 'k'
                ax.plot([x1, x1, x2, x2], [y, y+h, y+h, y], lw=1.5, c=col)
                ax.text((x1 + x2) * .5, y + h, f"p={p_value:.3e}", ha='center', va='bottom', color=col, fontsize=8)

        if i == 0:
            ax.set_ylabel("Defense Number per GB")
        ax.set_xlabel(None)
        ax.set_xticklabels(['BF', 'AF'][:len(group_df.index)], rotation=0, ha='center')
        ax.grid(axis='y', linestyle='--')
        ax.set_title(contig_group)

    # Step 9: Adjust layout, add a single legend, and save the plot to a file
    handles, labels = ax.get_legend_handles_labels()
    fig.legend(handles, labels, title='Defense Type', bbox_to_anchor=(1.05, 0.5), loc='center', ncol=1, fontsize='large')
    plt.subplots_adjust(wspace=0.4)  # Adjust space between subplots
    plt.tight_layout(rect=[0, 0, 1, 1])
    plt.savefig(output_file, format='pdf', bbox_inches='tight')
    plt.show()

def main():
    # Argument parsing
    parser = argparse.ArgumentParser(description='Create a stacked bar chart by Contig Group and Location BAF for top 20 defense types.')
    parser.add_argument('-i', '--input', type=str, required=True, help='Path to input file')
    parser.add_argument('-o', '--output', type=str, required=True, help='Path to output file')
    parser.add_argument('-v', '--value', type=str, required=True, help='Name of the column to be used as value (e.g., GCGENOME)')
    
    args = parser.parse_args()

    # Call the function with provided arguments
    create_stacked_bar_chart(args.input, args.output, args.value)

if __name__ == '__main__':
    main()

