import os
import pandas as pd
import argparse
from tqdm import tqdm

def parse_arguments():
    parser = argparse.ArgumentParser(description='Merge columns in files from directory B based on groupings from file A, calculating the average.')
    parser.add_argument('-a', '--file_a', required=True, help='Path to CSV file A with Sample, Location, and Country columns')
    parser.add_argument('-b', '--dir_b', required=True, help='Path to directory containing CSV files to be merged')
    parser.add_argument('-o', '--output_dir', required=True, help='Path to directory to save the output merged CSV files')
    return parser.parse_args()

def merge_columns(file_a, input_file, output_file):
    # Read file A
    df_a = pd.read_csv(file_a)
    
    # Read input file
    df_b = pd.read_csv(input_file, index_col=0)
    
    # Create a dictionary to map Sample to Location-Country group
    sample_to_group = df_a.set_index('Sample').apply(lambda row: f"{row['Location']}_{row['Country']}", axis=1).to_dict()
    
    # Group columns in df_b
    grouped_df = df_b.groupby(sample_to_group, axis=1)
    
    # Merge columns by calculating the average of values
    merged_df = grouped_df.mean()
    
    # Save the merged dataframe
    merged_df.to_csv(output_file)
    print(f"Merged file saved to {output_file}")

def main():
    args = parse_arguments()
    
    # Create output directory if it doesn't exist
    os.makedirs(args.output_dir, exist_ok=True)
    
    print("Starting column merging process...")
    for filename in tqdm(os.listdir(args.dir_b), desc="Processing files"):
        if filename.endswith('.csv'):
            input_file = os.path.join(args.dir_b, filename)
            output_file = os.path.join(args.output_dir, f"merged_{filename}")
            merge_columns(args.file_a, input_file, output_file)
    print("Column merging completed successfully.")

if __name__ == "__main__":
    main()

# Usage example:
# python script_name.py -a path/to/file_a.csv -b path/to/input_directory -o path/to/output_directory
#
# This script reads file A (containing Sample, Location, and Country columns) and all CSV files in the input directory,
# then merges columns in each file based on the Location-Country groupings from file A.
# The merged results (average values) are saved to the specified output directory.
