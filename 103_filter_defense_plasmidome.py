import pandas as pd
import re
import argparse
from tqdm import tqdm

def extract_sample_name(seqid):
    """Extract the sample name from seqid using regular expressions."""
    match = re.search(r'(DP-Sample\d+)', seqid)
    return match.group(1) if match else None

def filter_data(input_file_path, filtered_file_path):
    """Filters out specific rows from the input CSV file."""
    df = pd.read_csv(input_file_path)
    # Filter operations
    filtered_df = df[df['system.number'] != 'system.number']  # Removes duplicate headers
    filtered_df = filtered_df[filtered_df['system'] != 'DMS_other']  # Excludes rows with 'system' column equal to 'DMS_other'
    filtered_df.to_csv(filtered_file_path, index=False)

def transform_data(input_file_path, output_file_path):
    """Transforms the filtered CSV data."""
    df = pd.read_csv(input_file_path)
    # Data transformation operations
    df['Unique_ID'] = df['system.number'].astype(str) + "_" + df['seqid']
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
    grouped_df['Sample'] = grouped_df['seqid'].apply(extract_sample_name)
    final_columns_order = ['Sample'] + [col for col in grouped_df.columns if col != 'Sample']
    grouped_df = grouped_df[final_columns_order]
    grouped_df.to_csv(output_file_path, index=False)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="""This script takes a CSV file as input and performs two main operations: filtering and transformation. During the filtering step, it removes rows with duplicate headers and rows where the 'system' column equals 'DMS_other', indicating unwanted data. The filtered data is saved to a specified intermediate file. In the transformation step, the script aggregates data by creating a unique identifier from 'system.number' and 'seqid', calculates the range for 'start' and 'end' columns, and counts the occurrences of each unique identifier. It also extracts a sample name from 'seqid' using regular expressions. The final transformed data, which provides a summarized view of the gene counts along with sample information, is then saved to another specified output file.""",
        epilog='Example usage: python script.py --input raw_data.csv --filtered intermediate_data.csv --output final_data.csv'
    )
    parser.add_argument('--input', type=str, required=True, help='Path to the input CSV file.')
    parser.add_argument('--filtered', type=str, required=True, help='Path to save the filtered CSV file. This file contains data after removing duplicates and non-relevant entries.')
    parser.add_argument('--output', type=str, required=True, help='Path to save the transformed CSV file. This file includes aggregated data with gene counts and extracted sample names, providing a structured summary for analysis.')
    args = parser.parse_args()

    print("Filtering data...")
    filter_data(args.input, args.filtered)

    print("Transforming data...")
    transform_data(args.filtered, args.output)

