import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import argparse

def main(input_file, output_image):
    # Step 1: Read data
    df = pd.read_csv(input_file)

    # Step 2: Data filtering
    filtered_df = df[(df['Defense_Type'].notna()) & (df['Defense_Type'] != 'No')]
    filtered_df = filtered_df[~filtered_df['Defense_Type'].str.startswith(('PDC', 'HEC', 'DMS'))]
    filtered_df = filtered_df[(filtered_df['Insertion_Sequence_Type'].notna()) & (filtered_df['Insertion_Sequence_Type'] != 'No')]

    # Step 3: Data grouping and counting
    grouped_df = filtered_df.groupby('Defense_Type').size().reset_index(name='Count')

    # Step 4: Sort data by Count in descending order
    grouped_df = grouped_df.sort_values('Count', ascending=False)

    # Step 5: Draw Barplot
    plt.figure(figsize=(15, 8))
    sns.barplot(x='Defense_Type', y='Count', data=grouped_df, palette="Set2", order=grouped_df['Defense_Type'])

    # Step 6: Graph beautification
    plt.title('Total Count of Insertion Sequence Types by Defense Type')
    plt.ylabel('Count')
    plt.xlabel('Defense Type')
    plt.xticks(rotation=45, ha='right')
    plt.tight_layout()

    # Step 7: Save image
    plt.savefig(output_image, dpi=300)
    plt.show()

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Analyze defense types and insertion sequences.')
    parser.add_argument('-i', '--input', type=str, required=True, help='Input file path (CSV format).')
    parser.add_argument('-o', '--output', type=str, required=True, help='Output image file path.')
    args = parser.parse_args()

    main(args.input, args.output)
