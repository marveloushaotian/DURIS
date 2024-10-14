import os
import sys
import argparse
import pandas as pd
from tqdm import tqdm

def process_file(file_path, output_path):
    """
    Process a single CSV file, removing rows where the first column starts with 'PDC-' or 'HEC-', or equals 'DMS_other'.
    Save the modified DataFrame to the specified output file.
    """
    df = pd.read_csv(file_path)
    original_size = len(df)
    
    # Remove rows where the first column starts with 'PDC-' or 'HEC-', or equals 'DMS_other'
    df = df[~(df.iloc[:, 0].str.startswith('PDC-') | 
              df.iloc[:, 0].str.startswith('HEC-') | 
              (df.iloc[:, 0] == 'DMS_other'))]
    
    # Save the modified DataFrame to the output file
    df.to_csv(output_path, index=False)
    
    return original_size - len(df), output_path

def process_directory(directory, output_directory):
    """
    Process all CSV files in a directory, removing rows where the first column starts with 'PDC-' or 'HEC-', or equals 'DMS_other'.
    Save the modified DataFrames to the specified output directory.
    """
    total_rows_removed = 0
    for file in tqdm(os.listdir(directory)):
        if file.endswith(".csv"):
            file_path = os.path.join(directory, file)
            output_path = os.path.join(output_directory, file)
            rows_removed, _ = process_file(file_path, output_path)
            total_rows_removed += rows_removed
            print(f"Removed {rows_removed} rows from {file_path} and saved to {output_path}")
    return total_rows_removed

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Remove rows from CSV files where the first column starts with "PDC-" or "HEC-", or equals "DMS_other".')
    parser.add_argument('-i', '--input', required=True, help='Input file or directory path')
    parser.add_argument('-o', '--output', required=True, help='Output file or directory path')
    args = parser.parse_args()

    input_path = args.input
    output_path = args.output

    if os.path.isfile(input_path):
        rows_removed, file_path = process_file(input_path, output_path)
        print(f"Removed {rows_removed} rows from {input_path} and saved to {output_path}")
    elif os.path.isdir(input_path):
        os.makedirs(output_path, exist_ok=True)
        total_rows_removed = process_directory(input_path, output_path)
        print(f"Removed a total of {total_rows_removed} rows from all CSV files in {input_path} and saved to {output_path}")
    else:
        print("Invalid input path. Please provide a valid file or directory path.")
        sys.exit(1)
