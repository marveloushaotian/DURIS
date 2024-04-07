import pandas as pd
import re
import argparse
from tqdm import tqdm

def extract_sample_name(seqid):
    """
    Extract the sample name from seqid using regular expressions.
    Specifically, it captures everything before '_NODE_' in the seqid,
    which is assumed to be the sample name.
    """
    match = re.search(r'(.*)_NODE_.*', seqid)
    return match.group(1) if match else None

def filter_data(input_file_path, filtered_file_path):
    """
    Reads the CSV file, filters out rows where 'system.number' equals 'system.number' (likely headers repeated in data)
    and rows where 'system' equals 'DMS_other' (indicating data to exclude),
    and saves the filtered data to a new CSV file.
    """
    df = pd.read_csv(input_file_path)
    filtered_df = df[df['system.number'] != 'system.number']
    filtered_df = filtered_df[filtered_df['system'] != 'DMS_other']
    filtered_df.to_csv(filtered_file_path, index=False)

def transform_data(input_file_path, output_file_path):
    """
    Transforms the filtered data by:
    - Creating a 'Unique_ID' combining 'system.number' and 'seqid'.
    - Aggregating data by 'Unique_ID', calculating min/max for 'start'/'end',
      and counting occurrences.
    - Extracting the sample name from 'seqid'.
    - Reordering columns to place 'Sample' at the front.
    - Saving the transformed data to a new CSV file.
    """
    df = pd.read_csv(input_file_path)
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
        description="""This script processes a CSV file by first filtering out unnecessary rows, such as duplicates or irrelevant data, then transforming the data for analysis. Specifically, it removes rows where 'system.number' equals header labels or 'system' equals 'DMS_other'. Post filtering, it aggregates data based on a unique identifier constructed from 'system.number' and 'seqid', calculates min/max for start/end positions, and counts occurrences. Additionally, it extracts sample names from 'seqid' and reorganizes columns, placing the 'Sample' column at the forefront. The final dataset provides a summarized, analytical-ready format.""",
        epilog='Example usage: python script.py --input your_input.csv --filtered filtered_output.csv --output transformed_output.csv'
    )
    parser.add_argument('--input', type=str, required=True, help='Path to the input CSV file.')
    parser.add_argument('--filtered', type=str, required=True, help='Path to save the filtered CSV file. This intermediate file removes specific undesired rows based on pre-defined criteria.')
    parser.add_argument('--output', type=str, required=True, help='Path to save the transformed CSV file. This file presents the data aggregated and restructured for further analysis, including gene counts and extracted sample names.')
    args = parser.parse_args()

    print("Filtering data...")
    filter_data(args.input, args.filtered)

    print("Transforming data...")
    transform_data(args.filtered, args.output)

