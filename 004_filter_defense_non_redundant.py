import pandas as pd
import re
import argparse
from tqdm import tqdm

def extract_sample_name(seqid):
    """Extract the sample name from seqid using regular expressions."""
    match = re.search(r'(.*)_NODE_.*', seqid)
    return match.group(1) if match else None

def filter_data(input_file_path, filtered_file_path):
    # Reading the CSV file into a Pandas DataFrame
    df = pd.read_csv(input_file_path)
    # Filtering out rows
    filtered_df = df[df['system.number'] != 'system.number']
    filtered_df = filtered_df[filtered_df['system'] != 'DMS_other']
    # Saving the filtered DataFrame to a new CSV file
    filtered_df.to_csv(filtered_file_path, index=False)

def transform_data(input_file_path, output_file_path):
    # Load the CSV file into a Pandas DataFrame
    df = pd.read_csv(input_file_path)

    # Create the 'Unique_ID' column
    df['Unique_ID'] = df['system.number'].astype(str) + "_" + df['seqid']

    # Group by 'Unique_ID' and aggregate the columns
    agg_dict = {
        'system.number': 'first',
        'seqid': 'first',
        'system': 'first',
        'start': 'min',
        'end': 'max',
        'strand': 'first',
        'Unique_ID': 'count'
    }
    grouped_df = df.groupby('Unique_ID').agg(agg_dict).reset_index(drop=True)
    grouped_df.rename(columns={'Unique_ID': 'gene_counts'}, inplace=True)

    # Extract the sample name to create the 'Sample' column
    grouped_df['Sample'] = grouped_df['seqid'].apply(extract_sample_name)

    # Reorder the columns to put 'Sample' at the front
    final_columns_order = ['Sample'] + [col for col in grouped_df.columns if col != 'Sample']
    grouped_df = grouped_df[final_columns_order]

    # Save the transformed DataFrame to a new CSV file
    grouped_df.to_csv(output_file_path, index=False)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Process and transform CSV data.')
    parser.add_argument('--input', type=str, required=True, help='Path to the input CSV file.')
    parser.add_argument('--filtered', type=str, required=True, help='Path to save the filtered CSV file.')
    parser.add_argument('--output', type=str, required=True, help='Path to save the transformed CSV file.')
    args = parser.parse_args()

    print("Filtering data...")
    filter_data(args.input, args.filtered)

    print("Transforming data...")
    transform_data(args.filtered, args.output)

