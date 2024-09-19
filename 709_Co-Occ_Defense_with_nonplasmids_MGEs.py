import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from scipy.stats import ttest_ind
import argparse

def main(input_file, output_image, output_table, elements, group_column):
    # Predefined column names
    defense_column = 'Defense_Type'
    location_column = 'Location'
    sample_column = 'Sample'
    
    # Initialize an empty DataFrame to store results for all elements
    combined_df = pd.DataFrame()

    for element_column in elements:
        # Step 2: Data filtering
        filtered_df = df[(df[element_column].notna()) & (df[element_column] != 'No') &
                         (df[defense_column].notna()) & (df[defense_column] != 'No')]

        # Step 3: Data grouping and counting
        grouped_df = filtered_df.groupby([group_column, location_column, sample_column]).size().reset_index(name='Count')
        grouped_df['Element'] = element_column  # Add a column to mark element type
        
        # Ensure no duplicate indices
        grouped_df = grouped_df.reset_index(drop=True)
        
        # Append current element's data to the total DataFrame
        combined_df = pd.concat([combined_df, grouped_df])

    # Step 4: Adjust Location order
    combined_df[location_column] = pd.Categorical(combined_df[location_column], categories=['HP', 'RS', 'MS', 'BTP'], ordered=True)

    # Step 5: Set colors
    palette = {"HP": "#b58db3", "RS": "#75b989", "MS": "#4a9ba7", "BTP": "#e1834e"}

    # Step 6: Draw FacetGrid plot
    g = sns.catplot(
        x=group_column, y='Count', hue=location_column, col='Element',
        data=combined_df, kind='box', palette=palette, dodge=True,
        height=5, aspect=1.2
    )
    # Set stripplot for each subplot, explicitly specify order
    for ax in g.axes.flat:
        sns.stripplot(
            x=group_column, y='Count', hue=location_column, data=combined_df, 
            dodge=True, jitter=True, color='black', marker='o', alpha=0.5, order=sorted(combined_df[group_column].unique()), ax=ax
        )

    # Step 7: Significance testing and annotation
    for ax, element_column in zip(g.axes.flat, elements):
        element_df = combined_df[combined_df['Element'] == element_column]
        groups = element_df[group_column].unique()
        for group in groups:
            hp_data = element_df[(element_df[group_column] == group) & (element_df[location_column] == 'HP')]['Count']
            btp_data = element_df[(element_df[group_column] == group) & (element_df[location_column] == 'BTP')]['Count']
            if len(hp_data) > 0 and len(btp_data) > 0:
                stat, p_value = ttest_ind(hp_data, btp_data, equal_var=False)
                y_max = max(hp_data.max(), btp_data.max())
                ax.text(groups.tolist().index(group), y_max + 1, f'p={p_value:.3f}', ha='center')

    # Step 8: Graph beautification
    g.set_axis_labels("", "Count")
    g.set_titles(col_template="{col_name}")
    g.despine(left=True)
    plt.tight_layout()

    # Step 9: Save image
    plt.savefig(output_image, dpi=300)
    plt.show()

    # Step 10: Output statistical results table
    combined_df.to_csv(output_table, index=False)
    print(f"Results saved to {output_table}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Analyze multiple genomic elements and output a plot and table.')

    # Input and output file parameters
    parser.add_argument('-i', '--input', type=str, required=True, help='Input file path (CSV format).')
    parser.add_argument('-o', '--output_image', type=str, required=True, help='Output image file path.')
    parser.add_argument('-t', '--output_table', type=str, required=True, help='Output table file path (CSV format).')

    # Variable parameters
    parser.add_argument('-e', '--elements', type=str, required=True, help='Comma-separated list of column names for the elements (e.g., Transposon, Integron, Insertion_Sequence_Type).')
    parser.add_argument('-g', '--group_column', type=str, required=True, help='Column name for the group (e.g., Country).')

    args = parser.parse_args()

    # Process element parameters, convert comma-separated string to list
    elements_list = args.elements.split(',')

    # Read input file
    df = pd.read_csv(args.input)

    # Call main function
    main(input_file=args.input, output_image=args.output_image, output_table=args.output_table,
         elements=elements_list, group_column=args.group_column)
