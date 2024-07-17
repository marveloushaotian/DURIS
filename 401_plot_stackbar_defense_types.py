import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import argparse

def create_stacked_bar_chart(input_file, output_file, value_column):
    # Load the data
    df = pd.read_csv(input_file, sep='\t')

    # Calculate the total proportion of each Defense_Type across all groups
    total_proportion = df.groupby('Defense_Type')[value_column].sum()
    top_defense_types = total_proportion.nlargest(20).index

    # Filter the dataframe to retain only the top 20 defense types
    filtered_df = df[df['Defense_Type'].isin(top_defense_types)]

    # Create a combined column for grouping
    filtered_df['Group'] = filtered_df['Contig_Group'] + '_' + filtered_df['Location_BAF']

    # Pivot the data to have Defense_Type as columns and value_column as values
    pivot_df = filtered_df.pivot_table(index='Group', columns='Defense_Type', values=value_column, fill_value=0)

    # Sort columns by the sum of values to have the most common defense types at the bottom
    pivot_df = pivot_df[pivot_df.sum().sort_values(ascending=False).index]

    # Define a custom distinct color palette
    num_colors = pivot_df.shape[1]
    custom_colors = sns.color_palette('tab20', num_colors)  # Use the tab20 color palette for distinct colors

    # Plotting the stacked bar chart with distinct colors
    pivot_df.plot(kind='bar', stacked=True, figsize=(20, 10), color=custom_colors)

    # Customize plot
    plt.title('Stacked Bar Chart of {} by Contig Group and Location BAF (Top 20 Defense Types)'.format(value_column))
    plt.xlabel('Contig Group and Location BAF')
    plt.ylabel(value_column)
    plt.xticks(rotation=90)

    # Adjust the legend
    plt.legend(title='Defense Type', bbox_to_anchor=(1.05, 1), loc='upper left', ncol=2, fontsize='small')
    plt.tight_layout()

    # Save the plot to a file
    plt.savefig(output_file, format='pdf', bbox_inches='tight')
    plt.show()

if __name__ == '__main__':
    # Define and parse command-line arguments
    parser = argparse.ArgumentParser(description='Create a stacked bar chart by Contig Group and Location BAF for top 20 defense types.')
    parser.add_argument('-i', '--input', type=str, required=True, help='Path to input file')
    parser.add_argument('-o', '--output', type=str, required=True, help='Path to output file')
    parser.add_argument('-v', '--value', type=str, required=True, help='Name of the column to be used as value (e.g., GCGENOME)')
    args = parser.parse_args()

    # Call the function with provided arguments
    create_stacked_bar_chart(args.input, args.output, args.value)

