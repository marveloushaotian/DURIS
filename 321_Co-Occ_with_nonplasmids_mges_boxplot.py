import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from scipy.stats import ttest_ind
import argparse

def main(input_file, output_image, output_table, element_column, group_column):
    # Predefined column names
    defense_column = 'Defense_Type'
    location_column = 'Location'
    sample_column = 'Sample'

    # Step 1: Read data
    df = pd.read_csv(input_file)

    # Step 2: Data filtering
    filtered_df = df[(df[element_column].notna()) & (df[element_column] != 'No') &
                     (df[defense_column].notna()) & (df[defense_column] != 'No')]
    
    # New step: Remove Defense_Type entries starting with PDC, HEC, DMS, and 'No'
    filtered_df = filtered_df[~filtered_df[defense_column].str.startswith(('PDC', 'HEC', 'DMS', 'No'))]

    # Step 3: Data grouping and counting
    grouped_df = filtered_df.groupby([group_column, location_column, sample_column]).size().reset_index(name='Count')

    # Step 4: Adjust Location order
    grouped_df[location_column] = pd.Categorical(grouped_df[location_column], categories=['HP', 'RS', 'MS', 'BTP'], ordered=True)

    # Step 5: Set colors
    palette = {"HP": "#b58db3", "RS": "#75b989", "MS": "#4a9ba7", "BTP": "#e1834e"}

    # Step 6: Draw Boxplot
    plt.figure(figsize=(6, 8))
    sns.boxplot(x=group_column, y='Count', hue=location_column, data=grouped_df, dodge=True, palette=palette)
    sns.stripplot(x=group_column, y='Count', hue=location_column, data=grouped_df, dodge=True, jitter=True, color='black', marker='o', alpha=0.5)

    # Step 7: Significance testing
    groups = grouped_df[group_column].unique()
    for group in groups:
        hp_data = grouped_df[(grouped_df[group_column] == group) & (grouped_df[location_column] == 'HP')]['Count']
        btp_data = grouped_df[(grouped_df[group_column] == group) & (grouped_df[location_column] == 'BTP')]['Count']
        if len(hp_data) > 0 and len(btp_data) > 0:
            stat, p_value = ttest_ind(hp_data, btp_data, equal_var=False)
            y_max = max(hp_data.max(), btp_data.max())
            plt.text(groups.tolist().index(group), y_max + 1, f'p={p_value:.3f}', ha='center')

    # Step 8: Graph beautification
    plt.xlabel('')
    plt.ylabel('')
    plt.xticks(rotation=0, ha='center')
    plt.legend(title=location_column, bbox_to_anchor=(0.99, 0.99), loc='upper left')
    plt.gca().spines['top'].set_visible(False)
    plt.gca().spines['right'].set_visible(False)
    plt.gca().spines['bottom'].set_visible(False)
    plt.gca().spines['left'].set_visible(False)
    plt.tight_layout()

    # Step 9: Save image
    plt.savefig(output_image, dpi=300)
    plt.show()

    # Step 10: Output statistical results table
    grouped_df.to_csv(output_table, index=False)
    print(f"Results saved to {output_table}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Analyze genomic elements and output a plot and table.')

    # Input and output file parameters
    parser.add_argument('-i', '--input', type=str, required=True, help='Input file path (CSV format).')
    parser.add_argument('-o', '--output_image', type=str, required=True, help='Output image file path.')
    parser.add_argument('-t', '--output_table', type=str, required=True, help='Output table file path (CSV format).')

    # Variable parameters
    parser.add_argument('-e', '--element_column', type=str, required=True, help='Column name for the element (e.g., Transposon, Integron).')
    parser.add_argument('-g', '--group_column', type=str, required=True, help='Column name for the group (e.g., Country).')

    args = parser.parse_args()

    # Call main function
    main(input_file=args.input, output_image=args.output_image, output_table=args.output_table,
         element_column=args.element_column, group_column=args.group_column)
